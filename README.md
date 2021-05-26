# EDO&pi;: A Python Library for Group-Theoretic Microtonal Music Structures

### Installation
```
pip install edopi
```

### Get started
How to generate the main structures and visualizations:

```Python
from edopi import TonalSystem

# Instantiate a 12-EDO with generator 7
edo_12 = TonalSystem(12, 7)

# Show the Chromatic representation
edo_12.show()

# Show the cycle of Fifths
edo_12.show_gCycle()

# Get the diatonic scale and show it
diatonic = edo_12.diatonic_scale()
diatonic.show()

# Get Balzano Diagram and show it
b_diagram = edo_12.balzano_diagram(3, 4)
b_diagram.show()
```
