from boto3.resources.action import CustomModeledAction

def inject_delete_tags(event_emitter, **kwargs):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.ec2.deletetags.inject_delete_tags', 'inject_delete_tags(event_emitter, **kwargs)', {'CustomModeledAction': CustomModeledAction, 'delete_tags': delete_tags, 'event_emitter': event_emitter, 'kwargs': kwargs}, 0)

def delete_tags(self, **kwargs):
    kwargs['Resources'] = [self.id]
    return self.meta.client.delete_tags(**kwargs)

