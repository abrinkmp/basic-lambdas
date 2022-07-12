# Example mParticle Lambda Rules

_Samples of common use-cases for transforming mParticle batches using Lambda Rules._

<!-- 
Visit https://www.mparticle.com/ to learn more and get started with the platform
-->

## Data Transformation Use-Cases

### Pull SDK variables into Event Attributes
- event-transform.py
- another.py

### Another Use-Case ...

## Lambda Testing Notes
Python lambdas can be easily tested in PyCharm using the pycharm.py file.

Here's the format for a python lambda rule:

```
import json
def lambda_handler(event_batch, context):
    # transformation code goes here
    return event_batch
```

