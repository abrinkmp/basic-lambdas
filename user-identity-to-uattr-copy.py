# Take extended User Identities and copy into User Attributes
# Used for ease of finding users downstream based on the extended UIDs
# Handles Schema 1 and Schema 2 input formats
#
# Also filters out events when users are not email subscribed to at least one brand
#

import json

def lambda_handler(event_batch, context):

    if 'user_attributes' in event_batch:
        subscribed = get_uattr(event_batch['user_attributes'])
    else:
        subscribed = False

    new_batch = []
    events = event_batch['events']

    for event in events:
        if subscribed == True:
            new_batch.append(event)

    event_batch['events'] = new_batch

    if 'user_identities' in event_batch:
        identities = identity_mapper(event_batch['user_identities'])
        if 'user_attributes' in event_batch:
            event_batch['user_attributes'].update(identities)
        else:
            event_batch['user_attributes'] = identities

    return event_batch

def get_uattr(uattrs):
    subscribed = False
    if 'subscribed_email_brand1' in uattrs:
        if uattrs['subscribed_email_brand1'] == 'true':
            subscribed = True
    if 'subscribed_email_brand2' in uattrs:
        if uattrs['subscribed_email_brand2'] == 'true':
            subscribed = True

    return subscribed

def identity_mapper(id_array):
    id_dict = {}
    for id_entry in id_array:
        if 'identity_type' in id_entry and 'identity' in id_entry:
            # SCHEMA 1
            id_key = id_entry['identity_type']
            id_value = id_entry['identity']
            id_dict.update({id_key: id_value})  
        else:
            # SCHEMA 2
            id_dict = id_array
            
    return id_dict
