# The `run` section

`run` is a Value Section with the following Fields:

* `fps` (default `0`): Number of frames per second to display

* `max_cycles` (default `0`): If set, play the animation this many times.
If `0`, then play the animation forever.

* `seconds` (default `None,`): Maximum number of seconds to play, if set.

For developers only, there's one more field:

* `main` (default `None`): If non-empty, then `bp` runs in a background thread,
  and the function named here runs in the foreground

# Examples

**Example 1**:  Run forever at 30 frames per second (fps)

```
run:
  fps: 30
```

**Example 2**:  Run for two seconds at 10 fps

```
run:
  seconds: 2
  fps: 10
```

**Example 3**:  Run three times

```
run:
  max_cycles: 3
```

_Previous:_ [5. The `animation` Section](5-The-animation-Section.md)
. . . . . . . . . . . . . . . . . . . . . . . .
_Next:_  [7. The `shape` and `layout` sections](7-The-shape-and-layout-Sections.md)


---


```
shape: [64, 17]
animation: $bpa.matrix.circlepop
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/6-footer.gif)
