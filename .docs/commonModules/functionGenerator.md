# Function Generation

A _FunctionGenerator_ generates functions.

A Function is a value that changes over time. Generating one is useful for testing and tuning closed-loop control algorithms.

## Usage - End-User

A FunctionGenerator will produce multiple calibrations, prefixed with the provided name. Use the Calibrations webpage to use a FunctionGenerator.

## Usage - Code

To declare a new FunctionGenerator, first import the proper module:

```py
from utils.functionGenerator import FunctionGenerator
```

Then, declare your FunctionGenerator.

```py
myFg =  = FunctionGenerator("My Super-De-Duper Awesome Function Generator")
```

The FunctionGenerator must have a unique `name`.

Perodically, check whether the FunctionGenerator is active. Use this active status to change whether you are overriding a value or not

```py
if(fgTest.isActive()):
    # Do override behavior
else:
    # Do normal control behavior
```

Access the FunctionGenerator's current value with the `get()` method.

```py
val = fgTest.get()
```
