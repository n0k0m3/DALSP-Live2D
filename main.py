import os
import sys
from optparse import OptionParser

import dalsp_l2d_getfile as l2d


def main():
    print("Date A Live: Spirit Pledge Live2D\n")
    print("Selectively copy folder structure for Live2D model to destination\n")
    parser = OptionParser()
    parser.add_option("-d", "--data", dest="dataPath",
                      help="Data Source (contains res, src, TFFramework folder)", metavar="\"DATA_FOLDER\"")
    parser.add_option("-o", "--output", dest="wkPath", default=os.path.join(os.getcwd(),"Live2D_output"),
                      help="Output Directory, Live2D Assets will be copied here", metavar="\"OUTPUT\"")
    parser.add_option("-n", "--name", dest="spirit_need",
                      help="Decrypted Data Destination (MUST BE A FOLDER)", metavar="\"SPIRIT_NAME\"")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Print debug messages to stdout")


    (options, args) = parser.parse_args()

    if options.dataPath is None or options.spirit_need is None:
        print("[ERROR] No data source or spirit name specified. Run \"python main.py -h\" for more details")
        print()
        return
    l2d.getfile(options)
    print("[INFO]","Done!")

if __name__ == "__main__":
    main()
