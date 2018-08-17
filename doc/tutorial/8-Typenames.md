# Typenames, and the `path` and `aliases` Sections

### What is a Typename?

BLiPS lets you load projects, parts of projects, or even Python code from your
local drive or from the Internet.  Typenames are BLiPS's mechanism for importing
and reusing Python code.

 A _Typename_  identifies a Python class in a Class Section.

Each Class Section in a Project (`animation`, `controls`, `drivers`, or
`layout`) represents a Python class and has a `typename` field.

For convenience, you can write Typenames in four formats.

### 1. Absolute Typenames

An Absolute Typename is a full Python pathname of a class or function like
`math.log` or `bibliopixel.animation.tests.PixelTester`.

Absolute Typenames start with a letter and can contain only letters, numbers,
`.`, and `_`.

So `x23.he_is_13.yes` is an Absolute Typename but neither `23x.h` nor
`this-has-dashes` nor `this has spaces.no` nor `oops!` are Absolute Typenames.

### 2. Relative Typenames

To save typing, you can specify typenames relative to the base module for
that Class Section.  For example, the Absolute Typename
`bibliopixel.animation.tests.PixelTester` can be shortened to
the Relative Typename `.tests.PixelTester`

Relative Typenames start with a `.` and then look like Absolute Typenames.


### 3. File Typenames

You can directly load Python code from a file on your drive this way:
`/home/pi/Documents/myAnimation.py`

File Typenames always start with `/`.

### 4. Git Repo Typenames

You can directly load code from a Github repo.

`https://github.com/ManiacalLabs/BiblioPixelAnimations/blob/master/BiblioPixelAnimations/matrix/MatrixRain.py`

WARNING WARNING WARNING!

Git Repo Typenames allow you to load arbitrary code from the internet and
execute it.

Malicious code that you downloaded this way could do anything, including erasing
all your data or stealing money from your accounts.  ONLY use Git Repo Typenames
if you _completely and 100%_ trust the repo that you are loading from.
Remember, there's nothing preventing people from changing code that's perfectly
safe today to be malicious tomorrow.

The first time that you use a new Git Repo, `bp` will prompt you from the
command line to whitelist that site.  _Think long and hard_ before you do this!

### Class guessing

To save typing, BLiPS can often guess the name of the class you mean from the
file or module that it's in.

This happens in two cases:

* If there is only one class in the file or module
* or if there is exactly one class in the file or module whose name is
"canonically the same" as the file or module name

Two names are "canonically the same" if they are the same when you throw away
all punctuation and make them lower case - so `HelloWorld`, `HELLO_WORLD` and
`hello_world` are canonically the same.



### How to use Typenames in a Project.


**Example 1**:  Simple animation, Absolute Typename

```
    animation:
      typename: bibliopixel.animation.sequence.Sequence
```

For convenience, if the whole class section is a string, it's the `typename`:

**Example 3**:  Same animation as in Example 1

```
    animation: bibliopixel.animation.sequence.Sequence
```

**Example 4**:  Relative Typename

```
    animation: .sequence.Sequence
```

**Example 5**:  Relative Typename with type guessing

```
    animation: .sequence
```

_Previous:_ [7. The `shape` and `layout` sections](7-The-shape-and-layout-Sections.md)
. . . . . . . . . . . . . . . . . . . . . . . .
_Next:_ [9. The path and aliases Sections](9-the-path-and-aliases-Sections.md)

```
shape: [96, 8]
animation:
  typename: $bpa.strip.Wave
  color: coral
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/8-footer.gif)
