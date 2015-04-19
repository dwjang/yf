#!/usr/bin/env python

import sys
import time
import yahoo_finance as yf

printwidth = 70

def main(argv):
    
    tag = "test"

    nargs = len(argv)
    if nargs > 0: tag = argv[0]

    start = time.time()

    yahoo = yf.Share("YHOO")
    hisdata = yahoo.get_historical('2014-01-01', '2015-04-18')
    print hisdata

    now = time.time()
    print 'total elapsed time :', round((now-start)/60.,2), "minutes"
    print "-"*printwidth 



if __name__ == "__main__":
    main(sys.argv[1:])
