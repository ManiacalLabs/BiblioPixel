# 3. The `bp` program.

### 1. What is `bp`?

`bp` is short for the BLiPS project runner.  It's a command line application
that's installed as part of BLiPS, along with the `bibliopixel` Python library.

You've already used `bp` to run your BLiPS projects and `bp new` to create a new
BLiPS project, but `bp` has all sorts of other Commands, with names like
`run`, `new`, `demo`,  and `animations`.


### 2. Built-in documentation for `bp`.

`bp` has its own "help" system:

```
$ bp --help
## `bp` - The BiblioPixel Project Runner

`bp` is a command-line script installed with Bibliopixel.  It can run
projects and demos, configure hardware, save and load defaults, and more.
[... more help ...]
```

You can also type `bp -h`, `bp help` or just `bp` to get the same result.

If you want help on a specific Command, try this:

```
$ bp --help animations

usage: bp animations [-h]

List all animations

optional arguments:
  -h, --help            show this help message and exit
```

### 3.  `bp` command lines

Let's start with a few examples:
```
$ bp
$ bp color red
$ bp animations

$ bp one.yml
$ bp run one.yml
$ bp one.yml -vs --loglevel=frame
$ bp one.yml+two.yml three.yml

$ bp monitor midi
```

A `bp` command line has three parts, each optionalL

* the Command (e.g. `color`)
* the Arguments (e.g. `red` or `one.yml+two.yml three.yml`)
* the Flags (e.g. `-vs --loglevel=frame`)

The Command defaults to `run` so `bp one.yml` and `bp run one.yml` are the same.

Some Commands take no arguments: `bp animations`

Some Commands take exactly one argument:  `bp color green`

Some Commands take one optional argument:  `bp demo` or `bp demo cube`

Some Commands take one or more arguments: `bp run one.yml two.yml`


### 4. How to interrupt `bp`

The `bp demo` and sometimes the `bp run` Commands can continue indefinitely.

While Animations can have a specific, fixed length like ten seconds, most of
them go on indefinitely.  There are two ways to interrupt `bp` in the
middle of running an Animation.

The simplest way to interrupt `bp` is using control-C.  This keystroke
interrupts almost any command line program, not just `BLiPS`.  It must be
pressed from the command line which is running `bp`.

There are also three Commands that can be executed from any command line:
`bp shutdown`, `bp restart`, and `bp kill`.

`bp shutdown` requests an orderly shutdown of `bp`,  just as if you pressed
control-C from the command line.  It corresponds to sending a Unix SIGINT signal
to the `bp` process.

`bp restart` requests that `bp` shutdown and restart on the same Animation.  It
corresponds to sending a SIGHUP signal.

And `bp kill` kills the `bp` process dead, like sending a Unix SIGKILL.


_Previous:_  [2. How to write a Project](2-How-to-write-a-Project.md)
. . . . . . . . . . . . . . . . . . . . . . . .  _Next:_  [4. Projects](4-Projects.md)

---


```
shape: [64, 13]
animation: $bpa.strip.LarsonScanners.LarsonRainbow
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/3-footer.gif)
