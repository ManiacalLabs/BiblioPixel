import re
from .. import data_file, log

PREFIX = """\
https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/"""

GIF_RE = re.compile(r'! \[ .* \] \(' + PREFIX + r'(.* \.gif) \)', re.X)


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
            m = GIF_RE.match(line.strip())
            if m:
                yield m.group(1), code

            if line.strip():
                state = TEXT


def extract_gif_lines(lines):
    for filename, code in _extract(lines):
        codelines = '\n'.join(code)
        try:
            project = data_file.loads(codelines)
        except:
            log.error('Unable to load code: $s\n%s', filename, codelines)
        else:
            yield filename, project
