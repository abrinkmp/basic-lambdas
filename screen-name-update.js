/*
** 
** Update Screen View Names from one data source to match another data source
**
*/

exports.handler = (batch, context, callback) => {

    function update_screen(screen_view) {
        try {
            if (screen_view.data && screen_view.data.screen_name) {

                switch(screen_view.data.screen_name) {
                    case "account_viewed":
                        screen_view.data.screen_name = "Account"
                        break;
                    case "cart_viewed":
                        screen_view.data.screen_name = "Cart"
                        break;
                    case "coupons_viewed":
                        screen_view.data.screen_name = "Coupons"
                        break;  
                    case "login_viewed":
                        screen_view.data.screen_name = "Login"
                        break;  
                    case "product_details_viewed":
                        screen_view.data.screen_name = "Product Details"
                        break;  
                    case "search_viewed":
                        screen_view.data.screen_name = "Search"
                        break;  
                    case "shopping_list_viewed":
                        screen_view.data.screen_name = "Shopping List"
                        break;
                }
            }
        }
        catch (err) { } 
    }

    var new_events = [];
    // loop thru events to find screens
    batch.events.forEach(item => {
        try {
            if (item.event_type && item.event_type === "screen_view") {
                update_screen(item);
            }
            new_events.push(item);
        }
        catch (err) { }
    });
    batch.events = new_events;

    callback(null, batch);
};

