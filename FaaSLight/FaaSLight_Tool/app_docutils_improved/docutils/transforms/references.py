"""
Transforms for resolving references.
"""

from __future__ import annotations
__docformat__ = 'reStructuredText'
from docutils import nodes, utils
from docutils.transforms import Transform


class SectionIDs(Transform):
    """
    Add identifiers to sections.

    If the "legacy_ids" configuration setting is False, the rST parser
    does not generate identifiers for implicit targets (e.g. sections)
    in order to give explicit targets preferential access to identifiers
    matching their reference name.

    However, the `parts.Contents` transform and most writers
    expect sections to have an identifier, so this transform adds them.
    """
    default_priority = 240
    
    def apply(self) -> None:
        if getattr(self.document.settings, 'legacy_ids', True):
            return
        for node in self.document.findall(nodes.section):
            self.document.set_id(node)



class PropagateTargets(Transform):
    """
    Propagate empty internal targets to the next element.

    Given the following nodes::

        <target ids="internal1" names="internal1">
        <target anonymous="1" ids="id1">
        <target ids="internal2" names="internal2">
        <paragraph>
            This is a test.

    `PropagateTargets` propagates the ids and names of the internal
    targets preceding the paragraph to the paragraph itself::

        <target refid="internal1">
        <target anonymous="1" refid="id1">
        <target refid="internal2">
        <paragraph ids="internal2 id1 internal1" names="internal2 internal1">
            This is a test.
    """
    default_priority = 260
    
    def apply(self) -> None:
        for target in self.document.findall(nodes.target):
            if (isinstance(target.parent, nodes.TextElement) or (target.hasattr('refid') or target.hasattr('refuri') or target.hasattr('refname'))):
                continue
            assert len(target) == 0, 'error: block-level target has children'
            next_node = target.next_node(ascend=True)
            while isinstance(next_node, nodes.system_message):
                next_node = next_node.next_node(ascend=True, descend=False)
            if (next_node is None or (isinstance(next_node, (nodes.Invisible, nodes.Targetable)) and not isinstance(next_node, nodes.target))):
                continue
            next_node['ids'].extend(target['ids'])
            next_node['names'].extend(target['names'])
            if not hasattr(next_node, 'expect_referenced_by_name'):
                next_node.expect_referenced_by_name = {}
            if not hasattr(next_node, 'expect_referenced_by_id'):
                next_node.expect_referenced_by_id = {}
            for id in target['ids']:
                self.document.ids[id] = next_node
                next_node.expect_referenced_by_id[id] = target
            for name in target['names']:
                next_node.expect_referenced_by_name[name] = target
            next_node.expect_referenced_by_name.update(getattr(target, 'expect_referenced_by_name', {}))
            next_node.expect_referenced_by_id.update(getattr(target, 'expect_referenced_by_id', {}))
            if (isinstance(target.parent, nodes.figure) and isinstance(next_node, nodes.caption)):
                target.parent.remove(target)
                continue
            target['refid'] = target['ids'][0]
            target['ids'] = []
            target['names'] = []
            self.document.note_refid(target)



class AnonymousHyperlinks(Transform):
    """
    Link anonymous references to targets.  Given::

        <paragraph>
            <reference anonymous="1">
                internal
            <reference anonymous="1">
                external
        <target anonymous="1" ids="id1">
        <target anonymous="1" ids="id2" refuri="http://external">

    Corresponding references are linked via "refid" or resolved via "refuri"::

        <paragraph>
            <reference anonymous="1" refid="id1">
                text
            <reference anonymous="1" refuri="http://external">
                external
        <target anonymous="1" ids="id1">
        <target anonymous="1" ids="id2" refuri="http://external">
    """
    default_priority = 440
    
    def apply(self) -> None:
        anonymous_refs = [node for node in self.document.findall(nodes.reference) if node.get('anonymous')]
        anonymous_targets = [node for node in self.document.findall(nodes.target) if node.get('anonymous')]
        if len(anonymous_refs) != len(anonymous_targets):
            msg = self.document.reporter.error('Anonymous hyperlink mismatch: %s references but %s targets.\nSee "backrefs" attribute for IDs.' % (len(anonymous_refs), len(anonymous_targets)))
            msgid = self.document.set_id(msg)
            for ref in anonymous_refs:
                prb = nodes.problematic(ref.rawsource, ref.rawsource, refid=msgid)
                prbid = self.document.set_id(prb)
                msg.add_backref(prbid)
                ref.replace_self(prb)
            return
        for (ref, target) in zip(anonymous_refs, anonymous_targets):
            if (ref.hasattr('refid') or ref.hasattr('refuri')):
                continue
            target.referenced = True
            while True:
                if target.hasattr('refuri'):
                    ref['refuri'] = target['refuri']
                    ref.resolved = True
                    break
                else:
                    if not target['ids']:
                        target = self.document.ids[target['refid']]
                        continue
                    ref['refid'] = target['ids'][0]
                    self.document.note_refid(ref)
                    break



class IndirectHyperlinks(Transform):
    """
    a) Indirect external references::

           <paragraph>
               <reference refname="indirect-external">
                   indirect external
           <target ids="id1" names="direct-external"
               refuri="http://indirect">
           <target ids="id2" names="indirect-external"
               refname="direct-external">

       The "refuri" attribute is migrated back to all indirect targets
       from the final direct target (i.e. a target not referring to
       another indirect target)::

           <paragraph>
               <reference refname="indirect-external">
                   indirect external
           <target ids="id1" names="direct-external"
               refuri="http://indirect">
           <target ids="id2" names="indirect-external"
               refuri="http://indirect">

       Once the attribute is migrated, the preexisting "refname" attribute
       is dropped.

    b) Indirect internal references::

           <target ids="id1" names="final-target">
           <paragraph>
               <reference refname="indirect-internal">
                   indirect internal
           <target ids="id2" names="indirect-internal-2"
               refname="final target">
           <target ids="id3" names="indirect-internal"
               refname="indirect-internal-2">

       Targets which indirectly refer to an internal target become one-hop
       indirect (their "refid" attributes are directly set to the internal
       target's "id"). References which indirectly refer to an internal
       target become direct internal references::

           <target ids="id1" names="final-target">
           <paragraph>
               <reference refid="id1">
                   indirect internal
           <target ids="id2" names="indirect-internal-2" refid="id1">
           <target ids="id3" names="indirect-internal" refid="id1">
    """
    default_priority = 460
    
    def apply(self) -> None:
        for target in self.document.indirect_targets:
            if not target.resolved:
                self.resolve_indirect_target(target)
            self.resolve_indirect_references(target)
    
    def resolve_indirect_target(self, target) -> None:
        refname = target.get('refname')
        refid = target.get('refid')
        if refid:
            reftarget = self.document.ids.get(refid)
        else:
            reftarget = self.document.names.get(refname)
            refid = self.document.nameids.get(refname)
            if (reftarget and not refid):
                refid = self.document.set_id(reftarget)
        if not reftarget:
            for resolver_function in self.document.transformer.unknown_reference_resolvers:
                if resolver_function(target):
                    break
            else:
                self.nonexistent_indirect_target(target)
            return
        reftarget.note_referenced_by(id=refid)
        if (isinstance(reftarget, nodes.target) and not reftarget.resolved and reftarget.hasattr('refname')):
            if hasattr(target, 'multiply_indirect'):
                self.circular_indirect_reference(target)
                return
            target.multiply_indirect = 1
            self.resolve_indirect_target(reftarget)
            del target.multiply_indirect
        if reftarget.hasattr('refuri'):
            target['refuri'] = reftarget['refuri']
            if 'refid' in target:
                del target['refid']
        elif reftarget.hasattr('refid'):
            target['refid'] = reftarget['refid']
            self.document.note_refid(target)
        elif reftarget['ids']:
            target['refid'] = refid
            self.document.note_refid(target)
        else:
            self.nonexistent_indirect_target(target)
            return
        if refname is not None:
            del target['refname']
        target.resolved = True
    
    def nonexistent_indirect_target(self, target) -> None:
        if self.document.names.get(target['refname'], '') is None:
            self.indirect_target_error(target, 'which is a duplicate, and cannot be used as a unique reference')
        else:
            self.indirect_target_error(target, 'which does not exist')
    
    def circular_indirect_reference(self, target) -> None:
        self.indirect_target_error(target, 'forming a circular reference')
    
    def indirect_target_error(self, target, explanation) -> None:
        naming = ''
        reflist = []
        if target['names']:
            naming = '"%s" ' % target['names'][0]
        for name in target['names']:
            reflist.extend(self.document.refnames.get(name, []))
        for id in target['ids']:
            reflist.extend(self.document.refids.get(id, []))
        if target['ids']:
            naming += '(id="%s")' % target['ids'][0]
        msg = self.document.reporter.error('Indirect hyperlink target %s refers to target "%s", %s.' % (naming, target['refname'], explanation), base_node=target)
        msgid = self.document.set_id(msg)
        for ref in utils.uniq(reflist):
            prb = nodes.problematic(ref.rawsource, ref.rawsource, refid=msgid)
            prbid = self.document.set_id(prb)
            msg.add_backref(prbid)
            ref.replace_self(prb)
        target.resolved = True
    
    def resolve_indirect_references(self, target) -> None:
        if target.hasattr('refid'):
            attname = 'refid'
            call_method = self.document.note_refid
        elif target.hasattr('refuri'):
            attname = 'refuri'
            call_method = None
        else:
            return
        attval = target[attname]
        for name in target['names']:
            reflist = self.document.refnames.get(name, [])
            if reflist:
                target.note_referenced_by(name=name)
            for ref in reflist:
                if ref.resolved:
                    continue
                del ref['refname']
                ref[attname] = attval
                if call_method:
                    call_method(ref)
                ref.resolved = True
                if isinstance(ref, nodes.target):
                    self.resolve_indirect_references(ref)
        for id in target['ids']:
            reflist = self.document.refids.get(id, [])
            if reflist:
                target.note_referenced_by(id=id)
            for ref in reflist:
                if ref.resolved:
                    continue
                del ref['refid']
                ref[attname] = attval
                if call_method:
                    call_method(ref)
                ref.resolved = True
                if isinstance(ref, nodes.target):
                    self.resolve_indirect_references(ref)



class ExternalTargets(Transform):
    """
    Given::

        <paragraph>
            <reference refname="direct-external">
                direct external
        <target ids="id1" names="direct-external" refuri="http://direct">

    The "refname" attribute is replaced by the direct "refuri" attribute::

        <paragraph>
            <reference refuri="http://direct">
                direct external
        <target ids="id1" names="direct-external" refuri="http://direct">
    """
    default_priority = 640
    
    def apply(self) -> None:
        for target in self.document.findall(nodes.target):
            if target.hasattr('refuri'):
                refuri = target['refuri']
                for name in target['names']:
                    reflist = self.document.refnames.get(name, [])
                    if reflist:
                        target.note_referenced_by(name=name)
                    for ref in reflist:
                        if ref.resolved:
                            continue
                        del ref['refname']
                        ref['refuri'] = refuri
                        ref.resolved = True



class InternalTargets(Transform):
    default_priority = 660
    
    def apply(self) -> None:
        for target in self.document.findall(nodes.target):
            if (not target.hasattr('refuri') and not target.hasattr('refid')):
                self.resolve_reference_ids(target)
    
    def resolve_reference_ids(self, target) -> None:
        """
        Given::

            <paragraph>
                <reference refname="direct-internal">
                    direct internal
            <target ids="id1" names="direct-internal">

        The "refname" attribute is replaced by "refid" linking to the target's
        "id"::

            <paragraph>
                <reference refid="id1">
                    direct internal
            <target ids="id1" names="direct-internal">
        """
        for name in target['names']:
            refid = self.document.nameids.get(name)
            reflist = self.document.refnames.get(name, [])
            if reflist:
                target.note_referenced_by(name=name)
            for ref in reflist:
                if ref.resolved:
                    continue
                if refid:
                    del ref['refname']
                    ref['refid'] = refid
                ref.resolved = True



class Footnotes(Transform):
    """
    Assign numbers to autonumbered footnotes, and resolve links to footnotes,
    citations, and their references.

    Given the following ``document`` as input::

        <document>
            <paragraph>
                A labeled autonumbered footnote reference:
                <footnote_reference auto="1" ids="id1" refname="footnote">
            <paragraph>
                An unlabeled autonumbered footnote reference:
                <footnote_reference auto="1" ids="id2">
            <footnote auto="1" ids="id3">
                <paragraph>
                    Unlabeled autonumbered footnote.
            <footnote auto="1" ids="footnote" names="footnote">
                <paragraph>
                    Labeled autonumbered footnote.

    Auto-numbered footnotes have attribute ``auto="1"`` and no label.
    Auto-numbered footnote_references have no reference text (they're
    empty elements). When resolving the numbering, a ``label`` element
    is added to the beginning of the ``footnote``, and reference text
    to the ``footnote_reference``.

    The transformed result will be::

        <document>
            <paragraph>
                A labeled autonumbered footnote reference:
                <footnote_reference auto="1" ids="id1" refid="footnote">
                    2
            <paragraph>
                An unlabeled autonumbered footnote reference:
                <footnote_reference auto="1" ids="id2" refid="id3">
                    1
            <footnote auto="1" ids="id3" backrefs="id2">
                <label>
                    1
                <paragraph>
                    Unlabeled autonumbered footnote.
            <footnote auto="1" ids="footnote" names="footnote" backrefs="id1">
                <label>
                    2
                <paragraph>
                    Labeled autonumbered footnote.

    Note that the footnotes are not in the same order as the references.

    The labels and reference text are added to the auto-numbered ``footnote``
    and ``footnote_reference`` elements.  Footnote elements are backlinked to
    their references via "refids" attributes.  References are assigned "id"
    and "refid" attributes.

    After adding labels and reference text, the "auto" attributes can be
    ignored.
    """
    default_priority = 620
    autofootnote_labels = None
    'Keep track of unlabeled autonumbered footnotes.'
    symbols = ['*', '†', '‡', '§', '¶', '#', '♠', '♥', '♦', '♣']
    
    def apply(self) -> None:
        self.autofootnote_labels = []
        startnum = self.document.autofootnote_start
        self.document.autofootnote_start = self.number_footnotes(startnum)
        self.number_footnote_references(startnum)
        self.symbolize_footnotes()
        self.resolve_footnotes_and_citations()
    
    def number_footnotes(self, startnum):
        """
        Assign numbers to autonumbered footnotes.

        For labeled autonumbered footnotes, copy the number over to
        corresponding footnote references.
        """
        for footnote in self.document.autofootnotes:
            while True:
                label = str(startnum)
                startnum += 1
                if label not in self.document.nameids:
                    break
            footnote.insert(0, nodes.label('', label))
            for name in footnote['names']:
                for ref in self.document.footnote_refs.get(name, []):
                    ref += nodes.Text(label)
                    ref.delattr('refname')
                    assert len(footnote['ids']) == len(ref['ids']) == 1
                    ref['refid'] = footnote['ids'][0]
                    footnote.add_backref(ref['ids'][0])
                    self.document.note_refid(ref)
                    ref.resolved = True
            if (not footnote['names'] and not footnote['dupnames']):
                footnote['names'].append(label)
                self.document.note_explicit_target(footnote, footnote)
                self.autofootnote_labels.append(label)
        return startnum
    
    def number_footnote_references(self, startnum) -> None:
        """Assign numbers to autonumbered footnote references."""
        i = 0
        for ref in self.document.autofootnote_refs:
            if (ref.resolved or ref.hasattr('refid')):
                continue
            try:
                label = self.autofootnote_labels[i]
            except IndexError:
                n = len(self.autofootnote_labels)
                s = ('s' if n > 1 else '')
                msg = self.document.reporter.error(f'Too many autonumbered footnote references: only {n} corresponding footnote{s} available.', base_node=ref)
                msgid = self.document.set_id(msg)
                for ref in self.document.autofootnote_refs[i:]:
                    if (ref.resolved or ref.hasattr('refname')):
                        continue
                    prb = nodes.problematic(ref.rawsource, ref.rawsource, refid=msgid)
                    prbid = self.document.set_id(prb)
                    msg.add_backref(prbid)
                    ref.replace_self(prb)
                break
            ref += nodes.Text(label)
            id = self.document.nameids[label]
            footnote = self.document.ids[id]
            ref['refid'] = id
            self.document.note_refid(ref)
            assert len(ref['ids']) == 1
            footnote.add_backref(ref['ids'][0])
            ref.resolved = True
            i += 1
    
    def symbolize_footnotes(self) -> None:
        """Add symbols indexes to "[*]"-style footnotes and references."""
        labels = []
        for footnote in self.document.symbol_footnotes:
            (reps, index) = divmod(self.document.symbol_footnote_start, len(self.symbols))
            labeltext = self.symbols[index] * (reps + 1)
            labels.append(labeltext)
            footnote.insert(0, nodes.label('', labeltext))
            self.document.symbol_footnote_start += 1
            self.document.set_id(footnote)
        i = 0
        for ref in self.document.symbol_footnote_refs:
            try:
                ref += nodes.Text(labels[i])
            except IndexError:
                msg = self.document.reporter.error('Too many symbol footnote references: only %s corresponding footnotes available.' % len(labels), base_node=ref)
                msgid = self.document.set_id(msg)
                for ref in self.document.symbol_footnote_refs[i:]:
                    if (ref.resolved or ref.hasattr('refid')):
                        continue
                    prb = nodes.problematic(ref.rawsource, ref.rawsource, refid=msgid)
                    prbid = self.document.set_id(prb)
                    msg.add_backref(prbid)
                    ref.replace_self(prb)
                break
            footnote = self.document.symbol_footnotes[i]
            assert len(footnote['ids']) == 1
            ref['refid'] = footnote['ids'][0]
            self.document.note_refid(ref)
            footnote.add_backref(ref['ids'][0])
            i += 1
    
    def resolve_footnotes_and_citations(self) -> None:
        """
        Link manually-labeled footnotes and citations to/from their
        references.
        """
        for footnote in self.document.footnotes:
            for label in footnote['names']:
                if label in self.document.footnote_refs:
                    reflist = self.document.footnote_refs[label]
                    self.resolve_references(footnote, reflist)
        for citation in self.document.citations:
            for label in citation['names']:
                if label in self.document.citation_refs:
                    reflist = self.document.citation_refs[label]
                    self.resolve_references(citation, reflist)
    
    def resolve_references(self, note, reflist) -> None:
        assert len(note['ids']) == 1
        id = note['ids'][0]
        for ref in reflist:
            if ref.resolved:
                continue
            ref.delattr('refname')
            ref['refid'] = id
            assert len(ref['ids']) == 1
            note.add_backref(ref['ids'][0])
            ref.resolved = True
        note.resolved = True



class CircularSubstitutionDefinitionError(Exception):
    pass



class Substitutions(Transform):
    """
    Given the following ``document`` as input::

        <document>
            <paragraph>
                The
                <substitution_reference refname="biohazard">
                    biohazard
                 symbol is deservedly scary-looking.
            <substitution_definition names="biohazard">
                <image alt="biohazard" uri="biohazard.png">

    The ``substitution_reference`` will simply be replaced by the
    contents of the corresponding ``substitution_definition``.

    The transformed result will be::

        <document>
            <paragraph>
                The
                <image alt="biohazard" uri="biohazard.png">
                 symbol is deservedly scary-looking.
            <substitution_definition names="biohazard">
                <image alt="biohazard" uri="biohazard.png">
    """
    default_priority = 220
    'The Substitutions transform has to be applied very early, before\n    `docutils.transforms.frontmatter.DocTitle` and others.'
    
    def apply(self):
        defs = self.document.substitution_defs
        normed = self.document.substitution_names
        nested = {}
        line_length_limit = getattr(self.document.settings, 'line_length_limit', 10000)
        subreflist = list(self.document.findall(nodes.substitution_reference))
        for ref in subreflist:
            msg = ''
            refname = ref['refname']
            if refname in defs:
                key = refname
            else:
                normed_name = refname.lower()
                key = normed.get(normed_name, None)
            if key is None:
                msg = self.document.reporter.error('Undefined substitution referenced: "%s".' % refname, base_node=ref)
            else:
                subdef = defs[key]
                if len(subdef.astext()) > line_length_limit:
                    msg = self.document.reporter.error('Substitution definition "%s" exceeds the line-length-limit.' % key)
            if msg:
                msgid = self.document.set_id(msg)
                prb = nodes.problematic(ref.rawsource, ref.rawsource, refid=msgid)
                prbid = self.document.set_id(prb)
                msg.add_backref(prbid)
                ref.replace_self(prb)
                continue
            parent = ref.parent
            index = parent.index(ref)
            if ('ltrim' in subdef.attributes or 'trim' in subdef.attributes):
                if (index > 0 and isinstance(parent[index - 1], nodes.Text)):
                    parent[index - 1] = parent[index - 1].rstrip()
            if ('rtrim' in subdef.attributes or 'trim' in subdef.attributes):
                if (len(parent) > index + 1 and isinstance(parent[index + 1], nodes.Text)):
                    parent[index + 1] = parent[index + 1].lstrip()
            subdef_copy = subdef.deepcopy()
            try:
                for nested_ref in subdef_copy.findall(nodes.substitution_reference):
                    nested_name = normed[nested_ref['refname'].lower()]
                    if nested_name in nested.setdefault(nested_name, []):
                        raise CircularSubstitutionDefinitionError
                    nested[nested_name].append(key)
                    nested_ref['ref-origin'] = ref
                    subreflist.append(nested_ref)
            except CircularSubstitutionDefinitionError:
                parent = ref.parent
                if isinstance(parent, nodes.substitution_definition):
                    msg = self.document.reporter.error('Circular substitution definition detected:', nodes.literal_block(parent.rawsource, parent.rawsource), line=parent.line, base_node=parent)
                    parent.replace_self(msg)
                else:
                    ref_origin = ref
                    while ref_origin.hasattr('ref-origin'):
                        ref_origin = ref_origin['ref-origin']
                    msg = self.document.reporter.error('Circular substitution definition referenced: "%s".' % refname, base_node=ref_origin)
                    msgid = self.document.set_id(msg)
                    prb = nodes.problematic(ref.rawsource, ref.rawsource, refid=msgid)
                    prbid = self.document.set_id(prb)
                    msg.add_backref(prbid)
                    ref.replace_self(prb)
                continue
            ref.replace_self(subdef_copy.children)
            for node in subdef_copy.children:
                if isinstance(node, nodes.Referential):
                    if 'refname' in node:
                        self.document.note_refname(node)



class TargetNotes(Transform):
    """
    Creates a footnote for each external target in the text, and corresponding
    footnote references after each reference.
    """
    default_priority = 540
    'The TargetNotes transform has to be applied after `IndirectHyperlinks`\n    but before `Footnotes`.'
    
    def __init__(self, document, startnode) -> None:
        Transform.__init__(self, document, startnode=startnode)
        self.classes = startnode.details.get('class', [])
    
    def apply(self) -> None:
        notes = {}
        nodelist = []
        for target in self.document.findall(nodes.target):
            if not target.hasattr('refuri'):
                continue
            names = target['names']
            refs = []
            for name in names:
                refs.extend(self.document.refnames.get(name, []))
            if not refs:
                continue
            footnote = self.make_target_footnote(target['refuri'], refs, notes)
            if target['refuri'] not in notes:
                notes[target['refuri']] = footnote
                nodelist.append(footnote)
        for ref in self.document.findall(nodes.reference):
            if not ref.get('anonymous'):
                continue
            if ref.hasattr('refuri'):
                footnote = self.make_target_footnote(ref['refuri'], [ref], notes)
                if ref['refuri'] not in notes:
                    notes[ref['refuri']] = footnote
                    nodelist.append(footnote)
        self.startnode.replace_self(nodelist)
    
    def make_target_footnote(self, refuri, refs, notes):
        if refuri in notes:
            footnote = notes[refuri]
            assert len(footnote['names']) == 1
            footnote_name = footnote['names'][0]
        else:
            footnote = nodes.footnote()
            footnote_id = self.document.set_id(footnote)
            footnote_name = 'TARGET_NOTE: ' + footnote_id
            footnote['auto'] = 1
            footnote['names'] = [footnote_name]
            footnote_paragraph = nodes.paragraph()
            footnote_paragraph += nodes.reference('', refuri, refuri=refuri)
            footnote += footnote_paragraph
            self.document.note_autofootnote(footnote)
            self.document.note_explicit_target(footnote, footnote)
        for ref in refs:
            if isinstance(ref, nodes.target):
                continue
            refnode = nodes.footnote_reference(refname=footnote_name, auto=1)
            refnode['classes'] += self.classes
            self.document.note_autofootnote_ref(refnode)
            self.document.note_footnote_ref(refnode)
            index = ref.parent.index(ref) + 1
            reflist = [refnode]
            if not utils.get_trim_footnote_ref_space(self.document.settings):
                if self.classes:
                    reflist.insert(0, nodes.inline(text=' ', Classes=self.classes))
                else:
                    reflist.insert(0, nodes.Text(' '))
            ref.parent.insert(index, reflist)
        return footnote



class CitationReferences(Transform):
    """Resolve <citation_references>.

    The 'use_bibtex'__ configuration setting indicates that citation entries
    are fetched from a BibTeX database by the backend (LaTeX).

    __ https://docutils.sourceforge.io/docs/user/config.html#use-bibtex
    """
    default_priority = 770
    
    def apply(self) -> None:
        if not getattr(self.document.settings, 'use_bibtex', []):
            return
        for node in self.document.findall(nodes.citation_reference):
            if (node.resolved or self.document.nameids.get(node.get('refname'))):
                continue
            if node.astext():
                node.delattr('refname')
                node.resolved = True



class DanglingReferences(Transform):
    """
    Check for dangling references (incl. footnote & citation) and for
    unreferenced targets.

    Provisional : pending deprecation
      Docutils readers will add separate transforms for resolving
      refnames to refids and for reporting unresolved references
      instead of this transform (to make space for reference-resolving
      transforms added by extensions or applications) in Docutils 1.0.
      This transform will be removed in Docutils 2.0.
    """
    default_priority = 850
    
    def apply(self) -> None:
        visitor = DanglingReferencesVisitor(self.document, self.document.transformer.unknown_reference_resolvers)
        self.document.walk(visitor)
        for target in self.document.findall(nodes.target):
            if not target.referenced:
                if target.get('anonymous'):
                    continue
                if target['names']:
                    naming = target['names'][0]
                elif target['ids']:
                    naming = target['ids'][0]
                else:
                    naming = target['refid']
                self.document.reporter.info('Hyperlink target "%s" is not referenced.' % naming, base_node=target)



class DanglingReferencesVisitor(nodes.SparseNodeVisitor):
    """Provisional : pending deprecation

    This auxiliary class is used by the `DanglingReferences` transform
    which will no longer be used in Docutils 1.0.
    It will be removed in Docutils 2.0.
    """
    
    def __init__(self, document, unknown_reference_resolvers) -> None:
        nodes.SparseNodeVisitor.__init__(self, document)
        self.document = document
        self.unknown_reference_resolvers = unknown_reference_resolvers
    
    def unknown_visit(self, node) -> None:
        pass
    
    def visit_reference(self, node) -> None:
        if (node.resolved or not node.hasattr('refname')):
            return
        refname = node['refname']
        id = self.document.nameids.get(refname, '')
        if id:
            del node['refname']
            node['refid'] = id
            self.document.ids[id].note_referenced_by(id=id)
            node.resolved = True
            return
        for resolver_function in self.unknown_reference_resolvers:
            if resolver_function(node):
                return
        if id is None:
            msg = self.document.reporter.error(f'Duplicate target name, cannot be used as a unique reference: "{refname}".', base_node=node)
        else:
            if ('<' in refname or '>' in refname):
                hint = 'Did you want to embed a URI or alias?'
                if '<' not in refname:
                    hint += '\nOpening bracket missing.'
                elif ' <' not in refname:
                    hint += '\nThe embedded reference must be preceded by whitespace.'
                if '>' not in refname:
                    hint += '\nClosing bracket missing.'
                elif not refname.endswith('>'):
                    hint += '\nThe embedded reference must be the last text before the end string.'
                if ('< ' in refname or ' >' in refname):
                    hint += '\nWhitespace around the embedded reference is not allowed.'
                details = [nodes.paragraph('', hint)]
            else:
                details = []
            msg = self.document.reporter.error(f'Unknown target name: "{refname}".', *details, base_node=node)
        msgid = self.document.set_id(msg)
        prb = nodes.problematic(node.rawsource, node.rawsource, refid=msgid)
        try:
            prbid = node['ids'][0]
        except IndexError:
            prbid = self.document.set_id(prb)
        msg.add_backref(prbid)
        node.replace_self(prb)
    visit_footnote_reference = visit_citation_reference = visit_reference


