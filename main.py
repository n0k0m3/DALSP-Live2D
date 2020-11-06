import os
from argparse import ArgumentParser

import dalsp_l2d_getfile as l2d


def main():
    print("Date A Live: Spirit Pledge Live2D Live2DViewerEX\n")
    parser = ArgumentParser(
        description="""Selectively copy folder structure for Live2D model to destination.
        Will output MVLE file according to Live2DViewerEX spec""")
    parser.add_argument(dest="dataPath",
                        help="Data Source (contains res, src, TFFramework folder)", metavar="INPUT")
    parser.add_argument(dest="wkPath", default=os.path.join(os.getcwd(), "Live2D_output"),
                        help="Output Directory, Live2D Assets will be copied here", metavar="OUTPUT")
    parser.add_argument("-l", "--list",
                        action="store_true", dest="list", default=False,
                        help="List all available spirits and end the script")
    parser.add_argument("-n", "--name", dest="spirit_need", default="all",
                        help="Specify Spirit Name to generate L2D, default: all", metavar="SPIRIT_NAME")
    parser.add_argument("-v", "--verbose",
                        action="store_true", dest="verbose", default=False,
                        help="Print debug messages to stdout")

    options = parser.parse_args()

    live2d = l2d.DALSP_L2D(options)
    live2d.getfile()


if __name__ == "__main__":
    main()
