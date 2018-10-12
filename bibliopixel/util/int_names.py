"""
Fanciful names for integer indexes into lists - either a day of week,
a month, a planet, or a chemical element.


"""

import calendar


def to_index(name):
    if isinstance(name, float):
        raise KeyError('Indexes cannot be floating point')
    try:
        return int(name)
    except:
        pass
    try:
        return NAME_TO_INDEX[name.lower()]
    except:
        raise KeyError('Can\'t understand index "%s"' % name)


def to_names(index):
    return INDEX_TO_NAME[index]


def _combine(*name_lists):
    name_to_index = {}
    index_to_name = {}

    def add(i, name):
        nl = name.lower()
        if nl not in name_to_index:
            name_to_index[nl] = i
            index_to_name.setdefault(i, []).append(name)
        elif nl not in DUPES:
            raise ValueError(name + ' duplicated')

    for z in ZEROES:
        add(0, z)

    for name_list in name_lists:
        for i, names in enumerate(name_list):
            if isinstance(names, str):
                names = names,

            for name in names:
                add(i + 1, name)

    return name_to_index, index_to_name


DUPES = 'may', 'mercury'
ZEROES = 'none', 'nothing', 'zero', 'zip'

DAYS = tuple(zip(calendar.day_abbr, calendar.day_name))
MONTHS = tuple(zip(calendar.month_abbr, calendar.month_name))[1:]
COLORS = 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'
PLANETS = ('Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
           'Neptune', 'Pluto')

ELEMENTS = (
    ('H', 'hydrogen'),
    ('He', 'helium'),
    ('Li', 'lithium'),
    ('Be', 'beryllium'),
    ('B', 'boron'),
    ('C', 'carbon'),
    ('N', 'nitrogen'),
    ('O', 'oxygen'),
    ('F', 'fluorine'),
    ('Ne', 'neon'),
    ('Na', 'sodium'),
    ('Mg', 'magnesium'),
    ('Al', 'aluminum'),
    ('Si', 'silicon'),
    ('P', 'phosphorus'),
    ('S', 'sulfur'),
    ('Cl', 'chlorine'),
    ('Ar', 'argon'),
    ('K', 'potassium'),
    ('Ca', 'calcium'),
    ('Sc', 'scandium'),
    ('Ti', 'titanium'),
    ('V', 'vanadium'),
    ('Cr', 'chromium'),
    ('Mn', 'manganese'),
    ('Fe', 'iron'),
    ('Co', 'cobalt'),
    ('Ni', 'nickel'),
    ('Cu', 'copper'),
    ('Zn', 'zinc'),
    ('Ga', 'gallium'),
    ('Ge', 'germanium'),
    ('As', 'arsenic'),
    ('Se', 'selenium'),
    ('Br', 'bromine'),
    ('Kr', 'krypton'),
    ('Rb', 'rubidium'),
    ('Sr', 'strontium'),
    ('Y', 'yttrium'),
    ('Zr', 'zirconium'),
    ('Nb', 'niobium'),
    ('Mo', 'molybdenum'),
    ('Tc', 'technetium'),
    ('Ru', 'ruthenium'),
    ('Rh', 'rhodium'),
    ('Pd', 'palladium'),
    ('Ag', 'silver'),
    ('Cd', 'cadmium'),
    ('In', 'indium'),
    ('Sn', 'tin'),
    ('Sb', 'antimony'),
    ('Te', 'tellurium'),
    ('I', 'iodine'),
    ('Xe', 'xenon'),
    ('Cs', 'cesium'),
    ('Ba', 'barium'),
    ('La', 'lanthanum'),
    ('Ce', 'cerium'),
    ('Pr', 'praseodymium'),
    ('Nd', 'neodymium'),
    ('Pm', 'promethium'),
    ('Sm', 'samarium'),
    ('Eu', 'europium'),
    ('Gd', 'gadolinium'),
    ('Tb', 'terbium'),
    ('Dy', 'dysprosium'),
    ('Ho', 'holmium'),
    ('Er', 'erbium'),
    ('Tm', 'thulium'),
    ('Yb', 'ytterbium'),
    ('Lu', 'lutetium'),
    ('Hf', 'hafnium'),
    ('Ta', 'tantalum'),
    ('W', 'tungsten'),
    ('Re', 'rhenium'),
    ('Os', 'osmium'),
    ('Ir', 'iridium'),
    ('Pt', 'platinum'),
    ('Au', 'gold'),
    ('Hg', 'mercury'),
    ('Tl', 'thallium'),
    ('Pb', 'lead'),
    ('Bi', 'bismuth'),
    ('Po', 'polonium'),
    ('At', 'astatine'),
    ('Rn', 'radon'),
    ('Fr', 'francium'),
    ('Ra', 'radium'),
    ('Ac', 'actinium'),
    ('Th', 'thorium'),
    ('Pa', 'protactinium'),
    ('U', 'uranium'),
    ('Np', 'neptunium'),
    ('Pu', 'plutonium'),
    ('Am', 'americium'),
    ('Cm', 'curium'),
    ('Bk', 'berkelium'),
    ('Cf', 'californium'),
    ('Es', 'einsteinium'),
    ('Fm', 'fermium'),
    ('Md', 'mendelevium'),
    ('No', 'nobelium'),
    ('Lr', 'lawrencium'),
    ('Rf', 'rutherfordium'),
    ('Db', 'dubnium'),
    ('Sg', 'seaborgium'),
    ('Bh', 'bohrium'),
    ('Hs', 'hassium'),
    ('Mt', 'meitnerium'),
    ('Ds', 'darmstadtium'),
    ('Rg', 'roentgenium'),
    ('Cn', 'copernicium'),
    ('Nh', 'nihonium'),
    ('Fl', 'flerovium'),
    ('Mc', 'moscovium'),
    ('Lv', 'livermorium'),
    ('Ts', 'tennessine'),
    ('Og', 'oganesson'),
)


NAME_TO_INDEX, INDEX_TO_NAME = _combine(DAYS, MONTHS, COLORS, PLANETS, ELEMENTS)
