from . description import Description
from .. util import data_file


class SavedDescription:
    """
    Hold a Description and save and load it from a data_file.
    """
    def __init__(self, project_file='', desc=None, **kwds):
        self.desc = Description()

        self.project_file = project_file
        if project_file:
            self.load(project_file)
        else:
            self._project_file = project_file
        self.desc.update(desc, **kwds)

    def load(self, project_file=''):
        """Load/reload the description from a YML file. Prompt if no file given."""
        self._request_project_file(project_file)
        self.clear()
        self.desc.update(data_file.load(self._project_file))

    def save(self, project_file=''):
        """Save the description as a YML file. Prompt if no file given."""
        self._request_project_file(project_file)
        data_file.dump(self.desc.as_dict(), self.project_file)

    def clear(self):
        """Clear description to default values"""
        self.desc.clear()

    def __str__(self):
        return str(self.desc)

    def __repr__(self):
        rep = super().__repr__()
        if self.project_file:
            return rep + ' loaded from file ' + self.project_file
        else:
            return rep

    @property
    def project_file(self):
        return self._project_file

    @project_file.setter
    def project_file(self, project_file):
        if project_file and not project_file.endswith('.yml'):
            project_file += '.yml'
        self._project_file = project_file

    _ATTRIBUTES = 'project_file',

    def _request_project_file(self, project_file, action='store'):
        project_file = project_file or self.project_file
        if not project_file:
            project_file = input('Enter project_file to %s: ' % action).strip()
            if not project_file:
                raise ValueError('%s aborted', action.capitalize())
        self.project_file = project_file
