"""
List all BiblioPixel Animations
"""

import os, bibliopixel, inspect, BiblioPixelAnimations
from bibliopixel import animation
from bibliopixel.animation import (
    collection, indexed, parallel, receiver, wrapper)
from bibliopixel.util import log, walk
from bibliopixel.project import importer


def run(args):
    animations = {}
    for root, filename in walk.walk(ROOTS):
        basepath = os.path.dirname(root)
        relpath = os.path.relpath(filename, basepath)
        for category, name in _get_classes(relpath):
            animations.setdefault(category, []).append(name)

    count = 0
    for category, entries in sorted(animations.items()):
        log.printer(category + ':')
        for e in sorted(entries):
            if e not in _BLACKLIST:
                log.printer(' ', _canonicalize(e))
                count += 1
        log.printer()

    log.printer('Total animation classes', count)


def set_parser(parser):
    parser.set_defaults(run=run)


def _animation_category(value):
    if not (inspect.isclass(value) and issubclass(value, animation.Animation)):
        return

    for cls_name, cls in BASE_CLASSES:
        if value is cls or value is animation.Animation:
            return

        if issubclass(value, cls):
            return cls_name
    return 'all'


def _get_classes(filename):
    if not filename.endswith('.py'):
        return

    filename = filename[:-3]
    path = []

    while filename:
        filename, segment = os.path.split(filename)
        path.insert(0, segment)

    if not path or path[-1].startswith('_'):
        return

    python_path = '.'.join(path)

    try:
        module = importer.import_module(python_path)
    except:
        return

    python_path += '.'
    for name, value in vars(module).items():
        category = _animation_category(value)
        if category and not name.startswith('_'):
            yield category, python_path + name


def _canonicalize(name):
    parts = name.split('.')
    p = parts[-1].lower().replace('_', '')
    q = parts[-2].lower().replace('_', '')

    if p == q:
        parts.pop()

    name = '.'.join(parts)
    name = name.replace('bibliopixel.animation.', '.')
    name = name.replace('BiblioPixelAnimations.', '$bpa.')
    return name


BP_ROOT = os.path.dirname(bibliopixel.__file__)
BPA_ROOT = os.path.dirname(BiblioPixelAnimations.__file__)
ROOTS = BP_ROOT, BPA_ROOT
BASE_CLASSES = (
    ('circle', animation.Circle),
    ('cube', animation.BaseCubeAnim),
    ('game', animation.BaseGameAnim),
    ('matrix', animation.BaseMatrixAnim),
    ('strip', animation.BaseStripAnim),
    ('parallel', parallel.Parallel),
    ('wrapper', wrapper.Wrapper),
    ('indexed', indexed.Indexed),
    ('collection', collection.Collection),
    ('receiver', receiver.BaseReceiver),
    ('simple', animation.Animation),
)

_BLACKLIST = set((
    'bibliopixel.animation.off.OffAnim',
    'bibliopixel.animation.remote.control.Off',
    'bibliopixel.main.demo_table.Sequence',
    'bibliopixel.main.all_pixel_test.StripChannelTest',
    'bibliopixel.animation.failed.Failed',
    'BiblioPixelAnimations.simple.Fill.Fill',
))
