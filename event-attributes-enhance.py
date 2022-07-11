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

    # test 3 - lots of events
    test_data = '{"events":[{"data":{"screen_name":"Contest"},"event_type":"screen_view"},{"data":{"custom_event_type":"navigation","event_name":"view_menu","custom_attributes":{"eventAttribute":"customflagtest"}},"event_type":"custom_event"},{"data":{"product_action":{"action":"add_to_cart","products":[{"id":"piz001","name":"pizzapepperoni","custom_attributes":{"currency":"USD"}}]},"custom_event_type":"add_to_cart","custom_attributes":{"order_is_reorder":"true","restaurant_brand_id":"12345","user_is_authenticated":"true","restaurant_location_id":"56789","restaurant_location_name":"Pastoral","order_is_asap":"false","order_ahead_datetime":"1645720578694","order_type":"pickup","hermosa_marketplace_id":"24680"}},"event_type":"commerce_event"},{"data":{"product_action":{"action":"purchase","products":[{"id":"piz001","name":"pizzapepperoni","custom_attributes":{"currency":"USD"}}]},"custom_event_type":"purchase","custom_attributes":{"order_is_reorder":"true","restaurant_brand_id":"12345","user_is_authenticated":"true","restaurant_location_id":"56789","restaurant_location_name":"Pastoral","order_is_asap":"false","order_ahead_datetime":"1645720578694","order_type":"pickup","hermosa_marketplace_id":"24680"}},"event_type":"commerce_event"}],"device_info":{"platform":"Android"},"application_info":{"application_name":"mPTestAndroid","application_version":"1.0","application_build_number":"1"}}'
    
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
    app_version = event['data']['custom_attributes']['app_version']
    restaurant_brand_id = event['data']['custom_attributes']['restaurant_brand_id']
    user_is_authenticated = event['data']['custom_attributes']['user_is_authenticated']
    restaurant_location_id = event['data']['custom_attributes']['restaurant_location_id']
    restaurant_location_name = event['data']['custom_attributes']['restaurant_location_name']
    order_is_asap = event['data']['custom_attributes']['order_is_asap']
    order_ahead_datetime = event['data']['custom_attributes']['order_ahead_datetime']
    order_type = event['data']['custom_attributes']['order_type']
    hermosa_marketplace_id = event['data']['custom_attributes']['hermosa_marketplace_id']

    new_products = []
    for product in event['data']['product_action']['products']:
        product['custom_attributes']['platform'] = platform
        product['custom_attributes']['app_version'] = app_version
        product['custom_attributes']['restaurant_brand_id'] = restaurant_brand_id
        product['custom_attributes']['user_is_authenticated'] = user_is_authenticated
        product['custom_attributes']['restaurant_location_id'] = restaurant_location_id
        product['custom_attributes']['restaurant_location_name'] = restaurant_location_name
        product['custom_attributes']['order_is_asap'] = order_is_asap
        product['custom_attributes']['order_ahead_datetime'] = order_ahead_datetime
        product['custom_attributes']['order_type'] = order_type
        product['custom_attributes']['hermosa_marketplace_id'] = hermosa_marketplace_id
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

