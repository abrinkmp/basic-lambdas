import json

def lambda_handler(event_batch, context):
    if 'user_attributes' in event_batch:
        new_user_attributes = list_update(event_batch['user_attributes'])
    else:
        new_user_attributes = []
    event_batch['user_attributes'] = new_user_attributes
    return event_batch

def list_update(uattrs):
    if 'csv_a' in uattrs:
        uattrs['list_a'] = (uattrs['csv_a']).rsplit(",")
    new_uattrs = uattrs
    
    if 'csv_b' in uattrs:
        uattrs['list_b'] = (uattrs['csv_b']).rsplit(",")
    new_uattrs = uattrs
    
    if 'csv_c' in uattrs:
        uattrs['list_c'] = (uattrs['csv_c']).rsplit(",")
    new_uattrs = uattrs
    
    return new_uattrs