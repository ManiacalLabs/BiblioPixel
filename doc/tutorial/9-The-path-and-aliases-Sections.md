# 9 - The `aliases` and `path` Sections


The `path` and `aliases` Sections make it easier for you to find Python code
for Typenames.

## The `aliases` Project Section.

The optional Project Section `alias` is a dictionary of aliases to Typenames or
parts of Typenames that can be put together to save typing in your project.

The `$` character is used to introduce an alias into a typename.  Aliases are
terminated by the characters `.`,  `/` or `#`.

There is one alias built in: `$bpa` maps to `BiblioPixelAnimations`.

**Example 1**: Using `aliases`

```
    aliases:
      mat: BiblioPixelAnimations.matrix
      fade: christmas_lights.Fade

    animation:
        typename: sequence
        length: 2
        animations:
            - $mat.ImageAnim
            - $fade
            - $mat.ImageShow
            - $fade
            - $mat.ImageDissolve
            - $fade
```


## The `path` Project Section.

The optional Project Section `path` is a list of external directories that
contain extra Python code used by the Project.

The `path` is represented either by a list of strings, or by a single string
which is a list of directories separated by colons (like the `PATH` and
`PYTHONPATH` environment variables).

When Typenames in a Project are resolved to a class, these directories are
searched for code, in this order:

1. The local directory
2. The directory local to the Project .json file
3. Directories in the  `path` Project Section, in order given in the project
4. Directories in the `PYTHONPATH` environment variable
5 The Python installation directory

[TODO: make sure this is really true.]

**Example 2**: Using `path`

```
    path: [/home/pi/my-library, /var/stuff/some-library]

    # Equivalent using colon separated strings would be
    # path: "/home/pi/my-library:/var/stuff/some-library"
```

_Previous:_ [8. Typenames](8-Typenames.md)
. . . . . . . . . . . . . . . . . . . . . . . .
_Next:_ [10. The `driver` and `drivers` Sections](10-The-driver-and-drivers-Sections.md)

```
shape: [96, 8]
animation: $bpa.strip.Rainbows.Rainbow
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/9-footer.gif)
