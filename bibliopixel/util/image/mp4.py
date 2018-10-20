from .. import log
from . import file_writer

try:
    import cv2
except:
    log.error("""\
Could not import the OpenCV Python library - install it with:

    $ pip install opencv-python
""")
    cv2 = None

# https://tsaith.github.io/combine-images-into-a-video-with-python-3-and-opencv-3.html


class Writer(file_writer.FileWriter):
    def write(self, filename, frames, fps, show=False):
        fps = max(1, fps)
        out = None

        try:
            for image in frames:
                frame = cv2.imread(image)
                if show:
                    cv2.imshow('video', frame)

                if not out:
                    height, width, channels = frame.shape
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(filename, fourcc, 20, (width, height))

                out.write(frame)

        finally:
            out and out.release()
            cv2.destroyAllWindows()
