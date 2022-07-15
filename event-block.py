# Block event based on user attribute values
#

def lambda_handler(event_batch, context):

    subscribed = get_uattr(event_batch['user_attributes'])
    new_batch = []
    events = event_batch['events']

    for event in events:
        if subscribed == True:
            new_event = event
            new_batch.append(new_event)

    event_batch['events'] = new_batch
    return event_batch

def get_uattr(uattrs):

    if 'subscribed_brand1' in uattrs and uattrs['subscribed_brand1'] == 'true':
        subscribed = True
    elif 'subscribed_brand2' in uattrs and uattrs['subscribed_brand2'] == 'true':
        subscribed = True    
    else:
        subscribed = False

    return subscribed