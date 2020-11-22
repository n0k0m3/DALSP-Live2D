import os
from argparse import ArgumentParser

import dalsp_l2d_getfile as l2d


def get(options):
    live2d = l2d.DALSP_L2D(options)
    live2d.getfile()


def gen(options):
    live2d = l2d.DALSP_L2D_mlve(options)
    live2d.genmlve()


def main():
    print("Date A Live: Spirit Pledge Live2D Live2DViewerEX\n")
    parser = ArgumentParser(
        description="""Selectively copy folder structure for Live2D model to destination.
        Will output MVLE file according to Live2DViewerEX spec""")
    subparsers = parser.add_subparsers()
    parser_getfile = subparsers.add_parser(
        'get', help='Generate Folder and MVLE files')
    parser_getfile.add_argument(dest="dataPath",
                                help="Data Source (contains res, src, TFFramework folder)", metavar="INPUT")
    parser_getfile.add_argument(dest="wkPath", default=os.path.join(os.getcwd(), "Live2D_output"),
                                help="Output Directory, Live2D Assets will be copied here", metavar="OUTPUT")
    parser_getfile.add_argument("-l", "--list",
                                action="store_true", dest="list", default=False,
                                help="List all available spirits and end the script")
    parser_getfile.add_argument("-n", "--name", dest="spirit_need", default="all",
                                help="Specify Spirit Name to generate L2D, default: all", metavar="SPIRIT_NAME")
    parser_getfile.add_argument("-r", "--region", dest="region", default="EN",
                                help="Specify the region of the data (EN/CN), default: EN", metavar="REGION", choices=["EN", "CN"])
    parser_getfile.set_defaults(func=get)
    parser_getfile.add_argument("-v", "--verbose",
                                action="store_true", dest="verbose", default=False,
                                help="Print debug messages to stdout")
    parser_genmlve = subparsers.add_parser(
        'gen', help='Generate MVLE files from existing folder')
    parser_genmlve.add_argument(dest="wkPath", help="Folder to generate MLVE", metavar="WKFOLDER")
    parser_genmlve.set_defaults(func=gen)
    parser_genmlve.add_argument("-a", "--all",
                            action="store_true", dest="all", default=False,
                            help="generate an mlve file contains all characters")
    parser_genmlve.add_argument("-v", "--verbose",
                            action="store_true", dest="verbose", default=False,
                            help="Print debug messages to stdout")


    options = parser.parse_args()
    options.func(options)


if __name__ == "__main__":
    main()
