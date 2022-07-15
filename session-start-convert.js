exports.handler = (batch, context, callback) => {


    /**
     * Find Session Start Events
     * When found, tranform payload to a custom event 
     * Added for BRANCH event output
     * 
     */

    function transform_event(eventItem) {
        try {
            if (eventItem.event_type === 'session_start') {
                if (eventItem.data) {
                    var time_since_start_ms = 0;
                    if (eventItem.data.device_current_state) {
                        if (eventItem.data.device_current_state.time_since_start_ms) {
                            var time_since_start_ms = eventItem.data.device_current_state.time_since_start_ms
                        }
                        eventItem.data.device_current_state = {}; //remove session-specific data
                    }
                    if (!eventItem.data.custom_attributes ) {
                        eventItem.data.custom_attributes = {'time_since_start_ms': time_since_start_ms};
                    }
                    else {
                        eventItem.data.custom_attributes['time_since_start_ms'] = time_since_start_ms;
                    }               
                    eventItem.event_type = 'custom_event';
                    eventItem.data.custom_event_type = 'other';
                    eventItem.data.event_name = 'session_start';
                }
            }
        }
        catch (err) { } 
    }
    
    // loop thru events
    batch.events.forEach(item => {
        try {
            transform_event(item)
        }
        catch (err) { }
    });

    callback(null, batch);
};
