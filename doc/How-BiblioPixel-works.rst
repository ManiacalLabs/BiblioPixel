BiblioPixel has three key data structures: ``Driver``, ``LED`` and
``Animation``.

-  A ``Driver`` communicates with the actual lights or software
   visualizations.

-  A ``Layout`` represents the geometry of those lights.

-  And an ``Animation`` controls how those lights' values change over
   time.

A BiblioPixel program has exactly one ``Driver``, one ``LED``, and one
top-level ``Animation`` - though that ``Animation`` may be composed of
many other lower-level ``Animation``\ s.

The BiblioPixel system has drivers for all popular LED strip types,
including RGB and mono strips, but also for raw serial port drivers,
Philips Hue lights. For all your prototyping and entertainment needs,
BiblioPixel comes with a virtual driver named ``SimPixel`` - a fast,
customizable WebGL visualizer that runs immediately in the browser
without any plug-in or installation step.

[[Using BiblioPixel]]
