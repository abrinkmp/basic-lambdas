
/*
** Set a user attribute consistently on all events in an input source 
** Used for consistent event attribute filtering to outputs
**
*/

exports.handler = (batch, context, callback) => {

    function process_event(eventItem) {
        try {
            if (eventItem.data) {
                if ( !eventItem.data.custom_attributes ) {
                    eventItem.data.custom_attributes = {'platform':'web'};
                }
                else {
                    eventItem.data.custom_attributes['platform'] = 'web';
                }               
            }
        }
        catch (err) { } 
    }

    newEvents = [];
    
    batch.events.forEach(item => {
        try {
            process_event(item);
            newEvents.push(item);
        }
        catch (err) { }
    });
    batch.events = newEvents;

    callback(null, batch);
};
