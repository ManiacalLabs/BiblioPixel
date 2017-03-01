def set_parser(parser):
    parser.set_defaults(run=print)
    parser.add_argument('-name', type=str, default='bloom')
