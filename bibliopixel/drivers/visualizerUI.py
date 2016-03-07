from Tkinter import Tk, TclError, ALL, Canvas, TOP
import threading
import Queue
import time
import sys
import SocketServer
import platform
import os
os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import log

from network_receiver import ThreadedDataServer, ThreadedDataHandler


class VisualizerUI:

    def __init__(self, width, height, pixelSize, top=False):
        self._maxWindowWidth = 1024

        self._master = Tk()
        self._q = Queue.Queue()
        self._hasFrame = False

        self.x = width
        self.y = height
        self._count = self.x * self.y

        self._values = []
        self._leds = []

        self._pixelSize = pixelSize
        self._pixelPad = int(pixelSize / 2)
        self._pixelSpace = 0

        self.initUI()
        self.configure(self.x, self.y)

        self.checkQ()

        self._master.attributes("-topmost", top)

    def checkQ(self):
        if not self._q.empty():
            data = self._q.get_nowait()
            self.updateUI(data)

        wait = 0
        if "darwin" in platform.system().lower():
            wait = 1
        self._master.after(wait, self.checkQ)
        self._master.update_idletasks()

    def mainloop(self):
        self._master.mainloop()

    def updateUI(self, data):
        size = len(data) / 3
        if size != self._count:
            log.warning("Bytecount mismatch")
            return

        for i in range(size):
            r = data[i * 3 + 0]
            g = data[i * 3 + 1]
            b = data[i * 3 + 2]

            self._values[i] = self.toHexColor(r, g, b)

        try:
            for i in range(self._count):
                self._canvas.itemconfig(self._leds[i], fill=self._values[i])
        except TclError:
            # Looks like the UI closed!
            pass

    def toHexColor(self, r, g, b):
        return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)

    def update(self, data):
        self._q.put(data)

    def hasFrame(self):
        return not self._q.empty()

    def configure(self, x, y):
        self._type = type
        self.x = x
        self.y = y
        self._count = x * y

        self._values = []
        # init colors to all black (off)
        for i in range(self._count):
            self._values.append("#101010")

        c = self._canvas

        c.delete(ALL)
        self._leds = []
        for i in range(self._count):
            index = c.create_rectangle(
                0, 0, self._pixelSize, self._pixelSize, fill=self._values[i])
            self._leds.append(index)

        self.layoutPixels()

    def layoutPixels(self):
        if len(self._leds) == 0:
            return

        x_off = 0
        row = 0
        count = 0
        w = 0
        h = 0
        for y in range(self.y):
            for x in range(self.x):
                if y % 2 != 0:
                    x = self.x - x - 1
                _x = self._pixelPad + \
                    ((x - x_off) * (self._pixelSize + self._pixelSpace))
                _y = self._pixelPad + \
                    ((y + row) * (self._pixelSize + self._pixelSpace))
                if row > 0:
                    _y += 3 * row

                _w = _x + self._pixelSize + self._pixelSpace + self._pixelPad
                if _w > w:
                    w = _w
                _h = _y + self._pixelSize + self._pixelSpace + self._pixelPad
                if _h > h:
                    h = _h

                if self.y == 1 and _x + ((self._pixelSize + self._pixelSpace) * 2) > self._maxWindowWidth:
                    row += 1
                    x_off += (x - x_off + 1)

                self._canvas.coords(
                    self._leds[count], _x, _y, _x + self._pixelSize, _y + self._pixelSize)
                count += 1

        self._master.geometry("{0}x{1}".format(w, h))
        self._master.update()
        self._canvas.config(width=w, height=h)

    def __CancelCommand(self, event=None):
        self._master.quit()
        self._master.destroy()
        sys.exit()

    # def __resizeEvent(self, event):
    #    width = self._master.winfo_width()
    #    height = self._master.winfo_height()
    #    if width != self._width or height != self._height:
    #        self._width = width
    #        self._height = height
    #        self._master.after_idle(self.layoutPixels)

    # def __handleResize(self):
    #    width = self._master.winfo_width()
    #    height = self._master.winfo_height()
    #    if width != self._width or height != self._height:
    #        self._width = width
    #        self._height = height
    #        self.layoutPixels()
    #    self._master.after_idle(self.__handleResize)

    def initUI(self):
        m = self._master
        m.protocol('WM_DELETE_WINDOW', self.__CancelCommand)

        m.title("BiblioPixel Visualizer")
        m.geometry("10x10")
        m.update()
        self._width = m.winfo_width()
        self._height = m.winfo_height()
        m.minsize(self._width, self._height)

        self._canvas = Canvas(self._master, background="#000000")
        c = self._canvas
        c.pack(side=TOP)

        self.layoutPixels()
        # self._master.after_idle(self.__handleResize)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='BiblioPixel Visualizer')
    parser.add_argument('--width', help='Matrix Width',
                        required=True, type=int)
    parser.add_argument('--height', help='Matrix Height', default=1, type=int)
    parser.add_argument(
        '--pixelsize', help='width/height of pixels in visualizer (default: 10)', default=10, type=int)
    parser.add_argument(
        '--top', help='Keep the visualizer on top of all other windows', action='store_true')
    parser.add_argument(
        '--port', help='Advanced: TCP port to listen on (default: 1618)', default=1618, type=int)
    parser.add_argument(
        '--allip', help='Visualizer will listen for data on all network connections', action='store_true')

    args = vars(parser.parse_args())

    width = args['width']
    height = args['height']
    pixelSize = args['pixelsize']
    top = args['top']
    port = args['port']
    allip = args['allip']

    ui = VisualizerUI(width, height, pixelSize, top)

    ip = 'localhost'
    if allip:
        ip = '0.0.0.0'

    address = (ip, port)
    try:
        server = ThreadedDataServer(address, ThreadedDataHandler)
        server.update = ui.update
        server.hasFrame = ui.hasFrame

        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True)  # don't hang on exit
        t.start()
    except Exception as e:
        log.exception(e)
        log.error(
            "Unable to open port. Another visualizer is likely running. Exiting...")
        sys.exit(2)

    ui.mainloop()
