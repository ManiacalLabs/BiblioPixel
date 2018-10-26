Using the REST api
-----------------------------------

Introduction
====================

The REST api provides access to controls through the use of Web calls. You can use simple web calls.

The `REST README <https://github.com/ManiacalLabs/BiblioPixel/blob/master/bibliopixel/control/rest/README.rst>`_ provides some deeper information on the different types of endpoints, but this will get you started.

For the purpose of this tutorial, we'll start with a simple Project to fill a 50 pixel RGB light strip with solid blue.

.. code-block:: yaml

    shape: 50
    animation:
      typename: fill.Fill
      palette: blue

Starting BiblioPixel with the REST API enabled
==============================================

In order to start the rest api, we must add just two lines of YAML. We are assuming that you are running this one the same computer as your browser. If not, we'll address that in the next section.

.. code-block:: yaml

    shape: 50
    animation:
      typename: fill.Fill
      palette: blue
    controls:
      typename: rest

You rest API gets setup on port 8787 of your localhost by default. It is not externally accessible as there are no authentication methods in place.

You should now be able to go to http://127.0.0.1:8787 and see a very simple form to build some basic API requests. Try putting `animation.palette` into the Address box and hitting the `Get` button. You should have the RGB values for blue returned. 

Make your API remotely accessible
=================================
To make this remotely accessible, you will need to add `external_access: true` to the controls section like this.

.. code-block:: yaml

    controls:
      typername: rest
      external_access: true

Now you should be able to access the same API with http://YOURIP:8787. Replace YOURIP with your computer's IP. If you  have problems, consider your computers firewall may be blocking external access on port 8787.

Changing the port
====================

If you wish to change the port of the API server, you can do so with something like this.

.. code-block:: yaml

    controls:
      typername: rest
      external_access: true
      port: 8888

