// Copy commerce event custom_attributes and platform and app version into product custom_attributes 
// Done to allow advanced filtering in Iterable at the product level

exports.handler = (batch, context, callback) => {

    function process_event(eventItem, platform, app_version) {
        try {
            // every event gets platform and app_version added as event custom_attributes
            if (eventItem && eventItem.data) {
                if ( !eventItem.data.custom_attributes ) {
                    eventItem.data.custom_attributes = {'platform': platform, "app_version": app_version};
                }
                else {
                    eventItem.data.custom_attributes['platform'] = platform;
                    eventItem.data.custom_attributes['app_version'] = app_version;
                }               
            }

            // commerce events get event custom_attributes moved into item custom_attributes
            if (eventItem.event_type && eventItem.event_type === "commerce_event") {
                if (eventItem.data && eventItem.data.custom_attributes) {
                    var brand_id = eventItem.data.custom_attributes.brand_id;
                    var user_is_authenticated = eventItem.data.custom_attributes.user_is_authenticated;
                    var location_id = eventItem.data.custom_attributes.location_id;
                    var location_name = eventItem.data.custom_attributes.location_name;
                    if (eventItem.data.product_action.products) {
                        //loop through the products to check for eligible id values
                        eventItem.data.product_action.products.forEach(product => {
                            //custom_attributes already exist for this product
                            if (product.custom_attributes) {
                                product.custom_attributes.platform = platform;
                                product.custom_attributes.app_version = app_version;
                                product.custom_attributes.brand_id = brand_id;
                                product.custom_attributes.user_is_authenticated = user_is_authenticated;
                                product.custom_attributes.location_id = location_id;
                                product.custom_attributes.location_name = location_name;                      
                            }
                            else { 
                                product.custom_attributes.custom_attributes['platform'] = platform;
                                product.custom_attributes.custom_attributes['app_version'] = app_version;
                                product.custom_attributes.custom_attributes['brand_id'] = brand_id;
                                product.custom_attributes.custom_attributes['user_is_authenticated'] = user_is_authenticated;
                                product.custom_attributes.custom_attributes['location_id'] = location_id;
                                product.custom_attributes.custom_attributes['location_name'] = location_name;
                            }
                        });
                    }
                }
            }
        }
        catch (err) { } 
    }
    
    var platform = 'unknown';
    if (batch && batch.device_info && batch.device_info.platform) {
        platform = batch.device_info.platform;
    }
    
    var app_version = 'unknown';
    if (batch && batch.application_info && batch.application_info.application_version) {
        app_version = batch.application_info.application_version;
        if (app_version.search('[.]') > -1) {
            var app_split = app_version.split('.');
            app_version = app_split[1]; 
        }
    }
     
    // loop thru events
    batch.events.forEach(item => {
        try {
            process_event(item, platform, app_version);
        }
        catch (err) { }
    });

    callback(null, batch);
    
};

