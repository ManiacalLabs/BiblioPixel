# 5. The `animation` Section

BLiPS comes with a library of Animations called BiblioPixelAnimations
which you can reuse without programming.

And if you can program, writing an Animation is quite easy and often the best
way to solve your problem - there are more types of Animation than all the other
class types put together.

 The `animation` Class Section works together with the `run` Value Section to
describe everything to do with time in your Project.

The `animation` Section determines specifically how the lights change over time,
while the `run` Section describes more general information - like the frame rate
(in frames per second or fps), or how many times the animation is repeated.

### The Fields in the `animation` Section depend on its Class

Aside from `typename`, the Fields in the `animation` Section depend entirely on
the Class of the Animation itself.

Each Animation Class has a documentation page which should explain how it works,
its Fields, and give examples of usage.

**Example 1**: a single Animation with no Fields

```
animation: $bpa.matrix.bloom
shape: [32, 32]
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-example-1.gif)


**Example 2**: an animation with fields `scroll`, `color` and `bgcolor`

```
animation:
  typename: $bpa.matrix.Mainframe
  scroll: false
  color: green
  bgcolor: dark gray

shape: [32, 32]
```
![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-example-2.gif)

**Example 3**: Mix four animations together

```
animation:
    typename: mixer
    levels: [0.25, 0.25, 0.25, 0.25]
    animations:
        - $bpa.matrix.ImageAnim
        - $bpa.matrix.ImageShow
        - $bpa.matrix.ImageDissolve
        - $bpa.matrix.Mainframe

shape: [64, 64]
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-example-3.gif)

### A long list of Animation Classes.

To get a list of the possible `typenames` for Animation Classes, use  the `bp
animations` Command:

```
$ bp animations

circle:
  $bpa.circle.Twinkle
  $bpa.circle.arc_clock
  [... many more ...]

collection:
  .split

cube:
  $bpa.cube.GameOfLife.CubeGameOfLife
  $bpa.cube.Rain.RainBow
  $bpa.cube.bloom.CubeBloom

[... many more ...]
```

_Previous:_  [4. Projects](4-Projects.md)
. . . . . . . . . . . . . . . . . . . . . . . .
_Next:_ [6. The `run` Section](6-The-run-Section.md)

---



```
shape: [64, 17]
animation: $bpa.matrix.pinwheel
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-footer.gif)
