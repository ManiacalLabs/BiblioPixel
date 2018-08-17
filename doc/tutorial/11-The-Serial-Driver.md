# 11. The Serial Driver

The Serial Driver handles LEDs that are attached to the computer with the USB
bus, specifically the [AllPixel](https://maniacallabs.com/products/allpixel/) and
[PiPixel](https://www.tindie.com/products/ManiacalLabs/pipixel-raspberry-pi-led-strip-hat/)
hardware controllers.

### Serial Driver Fields

[TBD: embed or point to generated documentation for serial/driver.py]


### LEDTYPE

The Serial Driver needs to have an LEDTYPE set to identify the LED chipset and
hardware.  This must be one of these values: [TBD: point to or embed generated
documentation for ledtype.py]


_Previous:_ [10. The `driver` and `drivers` Sections](10-The-driver-and-drivers-Sections.md)
. . . . . . . . . . . . . . . . . . . . . . . .
_Next:_ [12. The `controls` Sections](10-The-controls-Sections.md)


```
shape: [64, 24]
animation:
  typename: $bpa.matrix.MathFunc
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/11-footer.gif)
