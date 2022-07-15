exports.handler = (batch, context, callback) => {

    /**
     * Find Opt Out Events
     * When found, tranform  "is_opted_out": true to  "is_opted_out": false so data is not blocked from going downstream
     * 
     */

    function transform_event(eventItem) {
        try {
            if (eventItem.event_type === 'opt_out') {
                if (eventItem.data && eventItem.data.is_opted_out) {
                    eventItem.data.is_opted_out = false
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
