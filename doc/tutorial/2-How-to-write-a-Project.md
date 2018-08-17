# 2. How to write a Project

### 1. Open a terminal

### 2. Change directory to the directory you want to work in: for example, your home
directory:

```
cd ~
```

### 3. Use the `bp new <your-project-name>` to create a new project in this
directory - for example

```
bp new my_lights
```

This will create a new directory named `my_lights/` in your current directory.

That directory contains a sample project file and a sample Python file for you
to edit!


### 4. Run the Project file:

Change directory to the project directory, and run the Project file.

```
cd my_lights
bp -s my_lights.yml
```

A window will open on your browser and you will see a lighting pattern like
this:

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-1.gif)



### 5.  Stop the program.

Hold down the Control key and press C (we'll call this Ctrl-X) to stop the `bp`
program.

Close the browser window.


### 6. Edit the Project to change the Shape.

With your text editor, edit the project file `my_lights.yml`.

Go to the line that says: `shape: [32, 48]` and change it to say
`shape: [96, 16]` and run the Project again.  You should see this:

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-2.gif)

Now change that line to say: `shape: [48, 48]` and run the Project again.  You
should see this:

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-3.gif)


### 7. Change the Animation

Go to the line that says: `animation: $bpa.matrix.bloom` and change it to say
`animation: $bpa.matrix.SpinningTriangle` and run it again.  You get this:

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-4.gif)


Now, let's try a sequence.

Delete that line `animation: $bpa.SpinningTriangle`

Go down a little to around line 48, and uncomment all those lines by removing
the first _two_ characters from each line, so it looks like this:

```
animation:
  typename: sequence
  length: 2
  animations:
    - $bpa.bloom
    - $bpa.pinwheel
    - $bpa.GameOfLife.GameOfLifeRGB
    - $bpa.SpinningTriangle
```

Run it again.  You should see a series of four animations, each running for ten
seconds, like this:

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-5.gif)


### 8.  Use a custom Python Animation

The `bp new` command creates a new custom Python animation for you to play with.
In this case, it's called `my_lights.MyLights`.

Delete the `animation:` lines above with the `sequence`, scroll down a little to
the lines at the end of the Project file, and uncomment them:

```
animation:
  typename: my_lights.MyLights
  color: red
```
Resulting in this:

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-6.gif)

Run the Project again.  Change the `color:` line to read `color: goldenrod` and
run it again to get this:

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-7.gif)


Now let's change the Python code.

With your text editor, edit the Python file `my_lights.py`.

After these lines in the file:

```
        # Set the previous pixel to black.
        self.color_list[this_pixel - 1] = COLORS.black
```

add these two lines:

```
        self.color_list[this_pixel - 2] = COLORS.yellow
        self.color_list[this_pixel - 3] = COLORS.black
```

and run it again to get this:

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-8.gif)


_Previous:_ [1.  Installing BLiPS](1-Installing-BLiPS.md)
. . . . . . . . . . . . . . . . . . . . . . . .
_Next:_  [3. The `bp` program](3-The-bp-program.md)

```
shape: [64, 16]
animation: $bpa.matrix.GameOfLife.GameOfLifeRGB
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-footer.gif)
