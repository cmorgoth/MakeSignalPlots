#! /usr/bin/env python
import ROOT as rt
import os.path
import sys, glob, re
from array import *
import math

def setstyle():
    # For the canvas:
    rt.gStyle.SetCanvasBorderMode(0)
    rt.gStyle.SetCanvasColor(rt.kWhite)
    rt.gStyle.SetCanvasDefH(400) #Height of canvas
    rt.gStyle.SetCanvasDefW(600) #Width of canvas
    rt.gStyle.SetCanvasDefX(0)   #POsition on screen
    rt.gStyle.SetCanvasDefY(0)
    
    # For the Pad:
    rt.gStyle.SetPadBorderMode(0)
    # rt.gStyle.SetPadBorderSize(Width_t size = 1)
    rt.gStyle.SetPadColor(rt.kWhite)
    rt.gStyle.SetPadGridX(False)
    rt.gStyle.SetPadGridY(False)
    rt.gStyle.SetGridColor(0)
    rt.gStyle.SetGridStyle(3)
    rt.gStyle.SetGridWidth(1)
    
    # For the frame:
    rt.gStyle.SetFrameBorderMode(0)
    rt.gStyle.SetFrameBorderSize(1)
    rt.gStyle.SetFrameFillColor(0)
    rt.gStyle.SetFrameFillStyle(0)
    rt.gStyle.SetFrameLineColor(1)
    rt.gStyle.SetFrameLineStyle(1)
    rt.gStyle.SetFrameLineWidth(1)
    
    # set the paper & margin sizes
    rt.gStyle.SetPaperSize(20,26)
    rt.gStyle.SetPadTopMargin(0.09)
    #rt.gStyle.SetPadRightMargin(0.065)
    rt.gStyle.SetPadRightMargin(0.15)
    rt.gStyle.SetPadBottomMargin(0.15)
    rt.gStyle.SetPadLeftMargin(0.17)
    
    # use large Times-Roman fonts
    rt.gStyle.SetTitleFont(132,"xyz")  # set the all 3 axes title font
    rt.gStyle.SetTitleFont(132," ")    # set the pad title font
    rt.gStyle.SetTitleSize(0.06,"xyz") # set the 3 axes title size
    rt.gStyle.SetTitleSize(0.06," ")   # set the pad title size
    rt.gStyle.SetLabelFont(132,"xyz")
    rt.gStyle.SetLabelSize(0.05,"xyz")
    rt.gStyle.SetLabelColor(1,"xyz")
    rt.gStyle.SetTextFont(132)
    rt.gStyle.SetTextSize(0.08)
    rt.gStyle.SetStatFont(132)
    
    # use bold lines and markers
    rt.gStyle.SetMarkerStyle(20)
    rt.gStyle.SetLineStyleString(2,"[12 12]") # postscript dashes
    
    #..Get rid of X error bars
    #rt.gStyle.SetErrorX(0.001)
    
    # do not display any of the standard histogram decorations
    rt.gStyle.SetOptTitle(0)
    rt.gStyle.SetOptStat(0)
    rt.gStyle.SetOptFit(1111)
    rt.gStyle.SetStatY(0.85)        
    rt.gStyle.SetStatX(0.92)                
    rt.gStyle.SetStatW(0.15)                
    rt.gStyle.SetStatH(0.15)                
    
    # put tick marks on top and RHS of plots
    rt.gStyle.SetPadTickX(1)
    rt.gStyle.SetPadTickY(1)
    
    ncontours = 999
    
    stops = [ 0.00, 0.1, 0.25, 0.65, 1.00 ]
    #stops = [ 0.00, 0.34, 0.61, 0.84, 1.00 ]
    red =   [ 1.0,   0.95,  0.95,  0.65,   0.15 ]
    green = [ 1.0,  0.85, 0.7, 0.5,  0.3 ]
    blue =  [ 0.95, 0.6 , 0.3,  0.45, 0.65 ]
    s = array('d', stops)
    r = array('d', red)
    g = array('d', green)
    b = array('d', blue)
        
    npoints = len(s)
    rt.TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    rt.gStyle.SetNumberContours(ncontours)
   
    rt.gStyle.cd()

def makeHistos(model,gchipairs):
    fileNames = {}
    h_MR = {}
    h_MRT = {}
    h_Rsq = {}
    h_nBtag = {}
    h_MRRsq = {}
    tree = {}
    rootFile = {}
    fileNames[700] = "root://eoscms//eos/cms/store/group/phys_susy/razor/Cristian_DM/ILV/TTJetsHad_ILV_MGDecays.root"
    fileNames[400] = "root://eoscms//eos/cms/store/group/phys_susy/razor/Cristian_DM/ILV/TTJetsSemiLept_ILV_MGDecaysTauola.root"
    fileNames[10] = "root://eoscms//eos/cms/store/group/phys_susy/razor/Cristian_DM/ILV/TTJets_ILV_FullyLeptMGDecaysTauola.root"
    for mchi in gchipairs:
        #fileNames[mchi] = "root://eoscms//eos/cms/store/group/phys_susy/razor/Cristian_DM/ILV/TTJetsHad_ILV_MGDecays.root"
        
        print  fileNames[mchi] 
        h_MRRsq[mchi] = rt.TH2D("h_MRRsq_%i"%(mchi), "h_MRRsq_%i"%(mchi),75,300., 2500.,50,0.15,1.5)
        h_MR[mchi]  = rt.TH1D("h_MR_%i"%(mchi), "h_MR_%i"%(mchi), 75,0.,2500.)
        h_MRT[mchi]  = rt.TH1D("h_MRT_%i"%(mchi), "h_MRT_%i"%(mchi), 75,0.,1500.)
        h_Rsq[mchi]  = rt.TH1D("h_Rsq_%i"%(mchi), "h_Rsq_%i"%(mchi), 50,0.3,1.5)
        h_nBtag[mchi]   = rt.TH1D("h_nBtag_%i"%(mchi), "h_nBtag_%i"%(mchi), 3,1.,4.)
        rootFile[mchi] = rt.TFile.Open(fileNames[mchi],"read")
        tree[mchi] = rootFile[mchi].Get("outTree")

        tree[mchi].Draw('>>elist','RSQ[2]>0.3 && nBtag==0 && BOX_NUM==0','entrylist')
        elist = rt.gDirectory.Get('elist')
        while True:
            entry = elist.Next()
            if entry == -1: break
            tree[mchi].GetEntry(entry)
            h_MR[mchi].Fill(tree[mchi].MR[2])
            h_Rsq[mchi].Fill(tree[mchi].RSQ[2])
            h_MRT[mchi].Fill(tree[mchi].MR[2]*math.sqrt(tree[mchi].RSQ[2]))
            h_nBtag[mchi].Fill(tree[mchi].nBtag)
            h_MRRsq[mchi].Fill(tree[mchi].MR[2],tree[mchi].RSQ[2])

    outputFile = rt.TFile.Open("%s_plots.root"%model,"recreate")
    for mchi in gchipairs:
        h_MRRsq[mchi].Write()
        h_MR[mchi].Write()
        h_MRT[mchi].Write()
        h_Rsq[mchi].Write()
        h_nBtag[mchi].Write()

def printPlots(plotDict, c, tleg, colors, varName, pdfName):
    c.Clear()
    tleg.Clear()
    c.cd()
    c.SetLogy(0)
    #if varName=="R^{2}":
        #c.SetLogy()
    tleg.SetFillColor(rt.kWhite)
    tleg.SetLineColor(rt.kWhite)
    tleg.SetTextFont(132)

    tLines = {}
    for mchi in gchipairs:
        plotDict[mchi].SetFillColor(colors[mchi])
        plotDict[mchi].SetLineColor(colors[mchi])
        if len(varName)==2:
            plotDict[mchi].SetFillStyle(1001)
            plotDict[mchi].GetXaxis().SetTitle(varName[0])
            plotDict[mchi].GetXaxis().CenterTitle()
            plotDict[mchi].GetYaxis().SetTitle(varName[1])
            plotDict[mchi].GetYaxis().CenterTitle()
        else:
            plotDict[mchi].SetFillStyle(3001)
            plotDict[mchi].SetLineWidth(3)
            if varName=="n_{b-tag}":
                plotDict[mchi].GetXaxis().SetLabelSize(0.075)
                plotDict[mchi].GetXaxis().SetBinLabel(1,"1")
                plotDict[mchi].GetXaxis().SetBinLabel(2,"2")
                plotDict[mchi].GetXaxis().SetBinLabel(3,"3")
            scale = plotDict[mchi].Integral()
            plotDict[mchi].Scale(1./scale)
            plotDict[mchi].GetXaxis().SetTitle(varName)
            plotDict[mchi].GetYaxis().CenterTitle()
            plotDict[mchi].GetYaxis().SetTitle("a.u.")
            plotDict[mchi].GetYaxis().CenterTitle()
    
            
    if model=="TJets":
        if len(varName)==2:
            tleg.AddEntry(plotDict[700],"t#bar{t} Had","f")
            tleg.AddEntry(plotDict[10],"t#bar{t} Leptonic","f")
            tleg.AddEntry(plotDict[400],"t#bar{t} SemiLeptonic","f")
            #tleg.AddEntry(plotDict[700],"m_{#tilde{#chi}}=700 GeV","f")
        else:
            tleg.AddEntry(plotDict[700],"t#bar{t} Had","lf")
            tleg.AddEntry(plotDict[10],"t#bar{t} Leptonic","lf")
            tleg.AddEntry(plotDict[400],"t#bar{t} SemiLeptonic","lf")
            #tleg.AddEntry(plotDict[700],"m_{#tilde{#chi}}=700 GeV","lf")
        if varName=="R^{2}":
            plotDict[700].SetMaximum(.1)
        elif varName=="n_{b-tag}":
            plotDict[700].SetMaximum(0.8)
        else:
            plotDict[700].SetMaximum(0.12)

            
        if len(varName)==2:
            plotDict[10].Draw("box")
            plotDict[400].Draw("boxsame") 
            plotDict[700].Draw("boxsame")
            #plotDict[1].Draw("boxsame")
        else:
           plotDict[10].Draw("hist")
           plotDict[400].Draw("histsame")
           plotDict[700].Draw("histsame")
           #plotDict[1].Draw("histsame") 

    tleg.Draw("same")
    
    l = rt.TLatex()
    l.SetTextAlign(12)
    l.SetTextSize(0.04)
    l.SetTextFont(132)
    l.SetNDC()
    if model=="TJets":
        l.DrawLatex(0.2,0.85,"CMS Simulation, #sqrt{s} = 8 TeV")
        #l.DrawLatex(0.2,0.80,"pp->#")
        l.DrawLatex(0.2,0.80,"pp#rightarrow t#bar{t} +Jets")
    
    c.Print(pdfName)


def makePlots(model,gchipairs):
    print "hello"
    h_MR = {}
    h_MRT = {}
    h_Rsq = {}
    h_nBtag = {}
    h_MRRsq = {}
    rootFile = rt.TFile.Open("%s_plots.root"%model)
    if model=="TJets":
        colors = {(1):rt.kGreen+1,(10):rt.kCyan+1, (400):rt.kBlue+3, (700):rt.kViolet-2}
    for mchi in gchipairs:
        h_MRRsq[mchi] = rootFile.Get("h_MRRsq_%i"%(mchi))
        h_MR[mchi] = rootFile.Get("h_MR_%i"%(mchi))
        h_MRT[mchi] = rootFile.Get("h_MRT_%i"%(mchi))
        h_Rsq[mchi] = rootFile.Get("h_Rsq_%i"%(mchi))
        h_nBtag[mchi] = rootFile.Get("h_nBtag_%i"%(mchi))
        
    c  = rt.TCanvas("c","c",600,500)
    tleg = rt.TLegend(0.68, 0.65, 0.9, 0.9)
    #printPlots(h_nBtag,c,tleg,colors,"n_{b-tag}","%s_nBtag.pdf"%model)
    printPlots(h_MR,c,tleg,colors,"M_{R} [GeV]","%s_MR.pdf"%model)
    printPlots(h_Rsq,c,tleg,colors,"R^{2}","%s_Rsq.pdf"%model)
    printPlots(h_MRT,c,tleg,colors,"M_{T}^{R} [GeV]", "%s_MRT.pdf"%model)
    printPlots(h_MRRsq,c,tleg,colors,["M_{R} [GeV]","R^{2}"], "%s_MRRsq.pdf"%model)


    
if __name__ == '__main__':
    setstyle()
    model = sys.argv[1]
    if model=="TJets":
        gchipairs = [(10),(400),(700)]

    if glob.glob("%s_plots.root"%model):
        makePlots(model,gchipairs)
    else:
        makeHistos(model,gchipairs)
