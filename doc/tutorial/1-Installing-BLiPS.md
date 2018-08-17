# 1. Installing BLiPS

BLiPS is a combination of a Python 3 library named BiblioPixel and a command
line program named `bp`.

In this documentation, lines that you type into a command line will start
with the dollar sign character `$` to distinguish them from the results -
so don't type the `$` yourself when entering command lines!

BLiPS is installed from the command line by typing:

```
$ pip3 install -U bibliopixel
```

If you get a "Permission Denied" error then you need to run this command with
`sudo`:

```
$ sudo pip3 install -U bibliopixel
```

If you get an error like "pip3: command not found" then you need to then install
Python 3 before you continue.

Download Python 3 from [here](https://www.python.org/downloads/), and then try
the instructions above again.

### Testing the installation.

To test your installation, type

```
$ bp demo matrix
```

and you should see flashing lights in your browser!

Most of the time, you want your animations to go on forever until they are
deliberately interrupted. .

To interrupt the `bp`, hold down the key named Control or CTL on your keyboard
and press C a few times.    Try it now!

In future, the documentation will just say "press control-C" when you need to do
this.


_Previous:_ [0. Before you start](0-Before-you-start.md)
. . . . . . . . . . . . . . . . . . . . . . . .
_Next:_ [2. How to write a Project](2-How-to-write-a-Project.md)

```
shape: [64, 16]
animation: $bpa.matrix.MatrixRain
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/1-footer.gif)
