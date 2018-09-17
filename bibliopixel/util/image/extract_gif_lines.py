import os
from .. import data_file, log

CODE_BLOCK = '.. code-block:: '

IMAGE = '.. image:: \
https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/'

LANGS = 'json', 'yaml'


def extract_gif_lines(lines):
    for filename, code in _extract(lines):
        codelines = '\n'.join(code)
        try:
            project = data_file.loads(codelines)
        except:
            log.error('Unable to load code: $s\n%s', filename, codelines)
        else:
            yield filename, project


def _extract(lines):
    in_code = False

    for line in lines:
        if line.startswith('.. '):
            if line.startswith(CODE_BLOCK):
                code = []
                in_code = True

            elif line.startswith(IMAGE) and in_code:
                filename = line[len(IMAGE):].strip()
                code = _remove_common_prefix(code)
                yield filename, code
                in_code = False

            elif line.startswith(IMAGE) and not in_code:
                pass

            elif line.startswith('.. image:'):
                print('missing image')
                print(line)
                print(IMAGE)

        elif in_code:
            if not line or line[0].isspace():
                code.append(line)
            else:
                in_code = False


def _remove_common_prefix(lines):
    lines = list(lines)
    while lines and not lines[0].strip():
        lines.pop(0)

    while lines and not lines[-1].strip():
        lines.pop()

    fill = ' ' * max(len(i) for i in lines)
    lines = [i or fill for i in lines]

    prefix = os.path.commonprefix(lines)
    spaces = len(prefix) - len(prefix.lstrip())
    return [i[spaces:] for i in lines]
