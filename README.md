# Example mParticle Lambda Rules

_Samples of common use-cases for transforming mParticle batches using Lambda Rules._

<!-- 
Visit https://www.mparticle.com/ to learn more and get started with the platform
-->

## Data Transformation Use-Cases

### Pull SDK variables into Event Attributes
- event-attributes-enhance.py
- event-attributes-enhance.js

### Block an event based on batch contents
- event-block.py

### Conditionally fix Screen Names
- screen-name-update.js

### Copy User Identities into User Attributes
- user-identity-uattr-copy.py

### Copy Commerce Event Attributes into Product Attributes
- event-attrs-to-product-attrs.js

### Convert a Session Start event into a Custom Event
- session-start-convert.js

### Add a Custom Attribute to All Events
- event-attributes-set-constant.js

### Convert a CSV comma-separated string into a list variable
- string-to-list-convert.py

### Call an API based on batch contents
- call-iterable-api.py

### Ignore legacy Opt Out events
-opt-out-ignore.js

## Lambda Testing Notes
Python lambdas can be easily tested in PyCharm using the pycharm.py file.

Here's the format for a python lambda rule:

```
import json
def lambda_handler(event_batch, context):
    # transformation code goes here
    return event_batch
```

## Javascript Testing Notes
Here's the format for a node.js lambda rule:

```
exports.handler = (batch, context, callback) => {
    batch.events.forEach(item => {
        try {
            // transform_code(item)
        }
        catch (err) { }
    });
    callback(null, batch);
};
```
