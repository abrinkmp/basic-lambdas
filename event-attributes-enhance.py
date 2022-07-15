# Sample Code - Enhance Event Attributes
# Read platform and app version for *ALL* events
# Read commerce event custom attributes into product custom attributes for *COMMERCE* events

def lambda_handler(event_batch, context):
    platform = get_platform(event_batch['device_info'])
    app_version = get_app_version(event_batch['application_info'])
    if app_version == None:
        app_version = 'none'

    new_batch = []
    events = event_batch['events']
    for event in events:
        # skip screens and SDK events
        if event['event_type'] == 'custom_event' or event['event_type'] == 'commerce_event':
            event['data']['custom_attributes']['platform'] = platform
            event['data']['custom_attributes']['app_version'] = app_version

        if event['event_type'] == 'commerce_event' and event['data']['product_action']['action'] == 'add_to_cart':
            new_event = copy_ev_attr_to_products(event)
        else:
            new_event = event
        new_batch.append(new_event)
        event_batch['events'] = new_batch

    return event_batch


def get_platform(device_info):
    platform = device_info['platform']
    return platform


def get_app_version(app_info):
    if 'application_version' in app_info:
        app_version = app_info['application_version']
    else:
        app_version = 'none'
    return app_version


def copy_ev_attr_to_products(event):
    platform = event['data']['custom_attributes']['platform']
    user_is_authenticated = event['data']['custom_attributes']['user_is_authenticated']

    new_products = []
    for product in event['data']['product_action']['products']:
        product['custom_attributes']['platform'] = platform
        product['custom_attributes']['user_is_authenticated'] = user_is_authenticated
        new_products.append(product)

    event['data']['product_action']['products'] = new_products

    return event
