/**
 * Pull a User Attribute and a Device Info element into all events
 * Needed for output filtering and downstream reporting
 */

exports.handler = (batch, context, callback) => {

    function process_event(eventItem, platform, brand) {
        try {
            if (eventItem.data) {
                if ( !eventItem.data.custom_attributes ) {
                    eventItem.data.custom_attributes = {'platform': platform, "brand_id": brand};
                }
                else {
                    eventItem.data.custom_attributes['platform'] = platform;
                    eventItem.data.custom_attributes['brand_id'] = brand;
                }               
            }
        }
        catch (err) {} 
    }
    
    // pull device_info.platform from the batch
    var batch_platform = batch.device_info.platform;
    
    // pull user_attributes
    var brand = 'none';
    if (batch.user_attributes && batch.user_attributes.brand_id) {
        brand = batch.user_attributes.brand_id;
    }
    
    batch.events.forEach(item => {
        try {
            process_event(item, batch_platform, brand);
        }
        catch (err) {}
    });

    callback(null, batch);
    
};
