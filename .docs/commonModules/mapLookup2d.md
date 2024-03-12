# MapLookup2D

A [function](https://en.wikipedia.org/wiki/Function_(mathematics)) defines the relationship between an input value, and an output value.

In software, a common way to define a function is by providing sample points. When an input value is provided, the nearest sample points are used to "look up" the output value.

`MapLookup2D` provides a simple method for doing this.

To use a `MapLookup2D`, first import it:

```py
from utils.mapLookup2d import MapLookup2D
```

Then, instantiate a new Map. You must provide a _list_ of two-element _tuples_ as the points in the map.

```py
myMapLookup = MapLookup2D([
    (1,4),
    (3,2),
    (5,2),
    (6,3),
    (9,0),
    ])
```


Finally, at runtime, perform the lookup when needed:

```py
outputVal = myMapLookup.lookup(inputVal)
```

In this example, we expect the points to form the following relationship:


```
outputVal
    ^
   5+
    |
====+==o
    |   ++ 
   3+      ++
    |         ++
   2+           +o=========o====o
    |                             +++
   1+                                 +++ 
    |                                     +++    
 <--+--+----+----+----+----+----+----+----+----o=======> inputVal
       1    2    3    4    5    6    7    8    9    10
 ```   