import logging
import os
import tempfile
import shutil
import json
from subprocess import check_call, check_output
from tarfile import TarFile
from dateutil.zoneinfo import METADATA_FN, ZONEFILENAME

def rebuild(filename, tag=None, format='gz', zonegroups=[], metadata=None):
    """Rebuild the internal timezone info in dateutil/zoneinfo/zoneinfo*tar*

    filename is the timezone tarball from ``ftp.iana.org/tz``.

    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('dateutil.zoneinfo.rebuild.rebuild', "rebuild(filename, tag=None, format='gz', zonegroups=[], metadata=None)", {'tempfile': tempfile, 'os': os, '__file__': __file__, 'TarFile': TarFile, '_run_zic': _run_zic, 'METADATA_FN': METADATA_FN, 'json': json, 'ZONEFILENAME': ZONEFILENAME, 'shutil': shutil, 'filename': filename, 'tag': tag, 'format': format, 'zonegroups': zonegroups, 'metadata': metadata}, 0)

def _run_zic(zonedir, filepaths):
    """Calls the ``zic`` compiler in a compatible way to get a "fat" binary.

    Recent versions of ``zic`` default to ``-b slim``, while older versions
    don't even have the ``-b`` option (but default to "fat" binaries). The
    current version of dateutil does not support Version 2+ TZif files, which
    causes problems when used in conjunction with "slim" binaries, so this
    function is used to ensure that we always get a "fat" binary.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('dateutil.zoneinfo.rebuild._run_zic', '_run_zic(zonedir, filepaths)', {'check_output': check_output, '_print_on_nosuchfile': _print_on_nosuchfile, 'check_call': check_call, 'zonedir': zonedir, 'filepaths': filepaths}, 0)

def _print_on_nosuchfile(e):
    """Print helpful troubleshooting message

    e is an exception raised by subprocess.check_call()

    """
    if e.errno == 2:
        logging.error("Could not find zic. Perhaps you need to install libc-bin or some other package that provides it, or it's not in your PATH?")

