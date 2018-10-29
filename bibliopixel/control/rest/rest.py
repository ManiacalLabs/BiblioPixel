import pathlib
from . import rest_server
from .. import control

PORT = 8787
ROOT_FOLDER = pathlib.Path(__file__).parents[3] / 'ui' / 'rest'
INDEX_FILE = 'index.html'


class Rest(control.ExtractedControl):
    OPEN_PAGE = False

    def __init__(self, *args, port=PORT, external_access=False, open_page=None,
                 root_folder=ROOT_FOLDER, index_file=INDEX_FILE, **kwds):
        super().__init__(*args, **kwds)
        if open_page is None:
            open_page = self.OPEN_PAGE

        self.rest_server = rest_server.RestServer(
            port, external_access, open_page, root_folder, index_file)

    def set_project(self, project):
        super().set_project(project)
        self.rest_server.project = project

    def cleanup(self):
        super().cleanup()
        self.rest_server.project = None

    def _make_thread(self):
        return self.rest_server.server


class OpenPage(Rest):
    OPEN_PAGE = True
