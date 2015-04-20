#!/usr/bin/env python

import os, sys
import time
import numpy as np
import ROOT
import yahoo_finance as yf

printwidth = 70


def moving_average(values, window):
    n = len(values)
    ma = []
    for i in range(n):
        if i < window:
            ma.append(values[i])
            continue
        sumv = 0
        for j in range(i,i-window-1,-1):
            sumv += values[j]
        sumv /= window
        ma.append(sumv)
    return ma


def main(argv):
    
    tag = "test"

    nargs = len(argv)
    if nargs > 0: tag = argv[0]

    start = time.time()

    hisdata_dir = "hisdata"
    try: os.stat(hisdata_dir)
    except: os.mkdir(hisdata_dir)

    result_dir = "results"
    try: os.stat(result_dir)
    except: os.mkdir(result_dir)

    plot_dir = "plots"
    try: os.stat(plot_dir)
    except: os.mkdir(plot_dir)

    rootfilename = result_dir+"/hists_stocks_"+tag+".root"
    fout = ROOT.TFile(rootfilename,"RECREATE")
    ROOT.gErrorIgnoreLevel=1001
    ROOT.gROOT.SetBatch(True) # run ROOT as a batch mode by default
    # ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetPadTopMargin(0.08)
    ROOT.gStyle.SetPadBottomMargin(0.11)
    ROOT.gStyle.SetPadLeftMargin(0.1)
    ROOT.gStyle.SetPadRightMargin(0.05)
    ROOT.gStyle.SetTitleOffset(1.4,"Y")

    symbols = ["GSPC"]
    start_date = "2015-01-01"
    end_date = "2015-04-18"

    for sb in symbols:
        stock = yf.Share(sb)
        hisdata_raw = stock.get_historical(start_date, end_date)
        hisdata = []
        for d in hisdata_raw:
            l = [d["Symbol"],d["Date"],d["Open"],d["High"],d["Low"],d["Close"],d["Adj_Close"]]
            hisdata.append(l)
        # print hisdata
        print len(hisdata)
        data = np.array(hisdata)
        values = [float(x) for x in data[:,5].tolist()]
        print len(values), values

        sma = moving_average(values,5)
        print len(sma), sma
        

    fout.Write()
    fout.Close()

    now = time.time()
    print 'total elapsed time :', round((now-start)/60.,2), "minutes"
    print "-"*printwidth 



if __name__ == "__main__":
    main(sys.argv[1:])
