import os, re
from .. import data_file, log

GIF_RE = re.compile(r'\b[\w-]+\.gif\b')
GIF_ROOT = 'doc/'
PATTERNS = {GIF_ROOT: GIF_ROOT}


def doc_path(filename):
    dirname = os.path.dirname(filename)

    for prefix, replacement in PATTERNS.items():
        if dirname.startswith(prefix):
            return replacement + dirname[len(prefix):]

    return GIF_ROOT + dirname


def _extract(lines):
    # State machine with three states
    TEXT, CODE, AFTER_CODE = 'text', 'code', 'after-code'

    state = TEXT
    code = []

    for line in lines:
        if line.strip() == '```':
            if state is CODE:
                state = AFTER_CODE

            else:
                code = []
                state = CODE

        elif state is CODE:
            code.append(line)

        elif state is AFTER_CODE:
            m = GIF_RE.search(line)
            if m:
                yield m.group(), code

            if line.strip():
                state = TEXT


def extract_gif_lines(filename, lines):
    path = doc_path(filename)
    for base, code in _extract(lines):
        full_path = os.path.join(path, base)
        codelines = '\n'.join(code)
        try:
            project = data_file.loads(codelines)
        except:
            log.error('Unable to load code: $s\n%s', filename, codelines)
        else:
            yield full_path, project
