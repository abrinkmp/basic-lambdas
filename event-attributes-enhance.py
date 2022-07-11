# Sample Code - Enhance Event Attributes
# Read platform and app version for *ALL* events
# Read commerce event custom attributes into product custom attributes for *COMMERCE* events

# ##################################### PYCHARM TESTING ###############################################
import json

def test_data():

    # test 1 - one custom event
    # test_data = '{"events": [{"data": {"custom_event_type": "navigation","event_name": "view_menu","custom_attributes": {"eventAttribute": "custom flag test","platform": "web","app_version": "test"}},"event_type": "custom_event"}],"device_info": {"platform": "Switch"},"application_info": {"application_version": "1.999"}}'

    # test 2 - one commerce event
    # test_data = '{"events":[{"data":{"product_action":{"action":"purchase","products":[{"id":"740992_835421","name":"Frying","custom_attributes":{"currency":"USD"}}]},"custom_event_type":"purchase","custom_attributes":{"order_type":"Pickup","restaurant_brand_id":"728590","has_marketplace_diner_fee":"true","restaurant_location_id":"393767","user_is_authenticated":"false","order_ahead_datetime":"","has_misc_fee":"true","has_delivery_fee":"false","order_is_asap":"true","misc_fee_amount":"0.25","hermosa_marketplace_id":"2","menu_id":"323330_202203011456","restaurant_location_name":"DellsCafe-HQ","marketplace_diner_fee_amount":"0.99","restaurant_location_category":"Burgers","delivery_fee_amount":"0","order_is_reorder":"false"}},"event_type":"commerce_event"}],"device_info":{"platform":"xbox"},"application_info":{"application_version":"1.123"}}'
    
    event_batch = json.loads(test_data)
    lambda_handler(event_batch, True)
    return {True}
# ##################################### PYCHARM TESTING - END ###############################################

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


# ##################################### PYCHARM TESTING ###############################################
if __name__ == '__main__':
    try:
        test_data()
    except:
        print('update did not work')
    else:
        print('update completed')
# ##################################### PYCHARM TESTING - END ###############################################

