from __future__ import print_function
import os
import numpy as np
import matplotlib.pyplot as plt
import root_numpy as rtnp
import pandas as pd
import ROOT
import time
import progressbar
from array import array
import pdb

def writeinfofile(mylist1, mylist2, folder):
    scriptname = os.path.basename(__file__)
    timestamp = time.strftime("%Y.%m.%d_%H.%M.%S")
    outputfile = folder+scriptname +"_" + timestamp + ".txt"

    f = open(outputfile, 'w')
    #if len(mylist1 != mylist2):
    #    print("list lengths does not match ")

    for i in xrange(len(mylist1)):
        f.write("%s:\t%s\n" %(mylist1[i], mylist2[i]))
    f.close()
    return timestamp



#sig_storage = "/mnt/storage/lborgna/Wprime/"
#sig_file = "m600.root"

sig_storage ="/mnt/storage/lborgna/SignalStitch/"
sig_file = "SigAll2_Test.root"

#bkg_storage = '/mnt/storage/lborgna/BackgroundStitch/'
#bkg_file = 'BkgAll2_Training.root'
bkg_storage = '/mnt/storage/lborgna/BackgroundStitch/Testing/'
bkg_file = 'BkgAll2_Test.root'

#bkg_storage = "/mnt/storage/lborgna/BackgroundStitch/"
#bkg_file = "BkgAll.root"

treename = "FlatSubstructureJetTree"

GeV = 1000
ptmin = 100 * GeV
ptmax = 2500 * GeV

selection = "(fjet_fatjet_dRmatched_particle_flavor == 24 || fjet_fatjet_dRmatched_particle_flavor == -24) && fjet_pt > " + str(ptmin) + " && fjet_pt < " + str(ptmax)
print(selection)
#selection = "fjet_fatjet_dRmatched_particle_flavor == 24 || fjet_fatjet_dRmatched_particle_flavor == -24 "

#selectionQCD = "fjet_pt"

selectionQCD = "fjet_pt > "+ str(ptmin) + " && fjet_pt < " + str(ptmax)
#selectionQCD ="fjet_pt"

fjet_pt = "fjet_pt"
fjet_eta = "fjet_eta"
fjet_phi = "fjet_phi"
fjet_E = "fjet_E"
fjet_D2 = "fjet_D2"
fjet_Tau21_wta = "fjet_Tau21_wta"


start = 1000000
stop = 2000000

storage_output ="/mnt/storage/lborgna/BkgMatched/Final/"
out_file = "BkgAll6_HighPt_Test" +'.root'


fnew = ROOT.TFile(storage_output+out_file,"recreate")
Tree = ROOT.TTree("FlatSubstructureJetTree", "Reconst ntuple")

test = ROOT.TFile.Open(bkg_storage + bkg_file)
old_tree = test.Get("FlatSubstructureJetTree")

Wpt = rtnp.root2array(sig_storage + sig_file, treename = treename, selection = selection, branches = fjet_pt)
QCD_pt = rtnp.root2array(bkg_storage + bkg_file, treename = treename, selection = selectionQCD, branches = fjet_pt)

print(Wpt)
print(QCD_pt)

Nbins = 100
n, bins, patches = plt.hist(QCD_pt, Nbins, normed=False, facecolor='green', alpha=0.5)
nn, bbins, ppatches = plt.hist(Wpt, bins, normed=False, facecolor='red', alpha=0.5)

ratio = nn/(n+ 0.00000000001)
A = np.max(ratio)
ratio = (1/A) * ratio

cluster_E_entry = ROOT.vector('float')()
cluster_eta_entry = ROOT.vector('float')()
cluster_phi_entry = ROOT.vector('float')()
cluster_pt_entry  = ROOT.vector('float')()

fjet_pt_entry = array('f', [0.0])
fjet_feta_entry = array('f', [0.0])
fjet_fphi_entry = array('f', [0.0])
fjet_fE_entry = array('f', [0.0])
fjet_D2_entry = array('f', [0.0])
fjet_Tau21_wta_entry = array('f', [0.0])
fjet_dRmatched_maxEParton_flavor_entry = array('I', [0])
fjet_truthJet_pt_entry = array('f', [0.0])

Tree.Branch('fjet_pt', fjet_pt_entry, 'fjet_pt/F')
Tree.Branch('fjet_eta', fjet_feta_entry, 'fjet_eta/F')
Tree.Branch('fjet_phi', fjet_fphi_entry, 'fjet_phi/F')
Tree.Branch('fjet_E', fjet_fE_entry, 'fjet_E/F')
Tree.Branch('fjet_Tau21_wta', fjet_Tau21_wta_entry,'fjet_Tau21_wta/F')
Tree.Branch('fjet_D2', fjet_D2_entry, 'fjet_D2/F')
Tree.Branch('fjet_dRmatched_maxEParton_flavor', fjet_dRmatched_maxEParton_flavor_entry, 'fjet_dRmatched_maxEParton_flavor/I')
Tree.Branch('fjet_truthJet_pt', fjet_truthJet_pt_entry, 'fjet_truthJet_pt/F')
Tree.Branch('clus_E', cluster_E_entry)
Tree.Branch('clus_eta', cluster_eta_entry)
Tree.Branch('clus_phi', cluster_phi_entry)
Tree.Branch('clus_pt', cluster_pt_entry)

tosscount = 0

bar = progressbar.ProgressBar()

QCD_pt_new  = []

for i in bar(range(len(ratio))):

    for x in range(len(QCD_pt)):
        if QCD_pt[x] > bins[i] and QCD_pt[x] < bins[i+1]:
            U = np.random.uniform(0, 1)
            if ratio[i] < U:
                tosscount = tosscount + 1
            elif ratio[i] > U:
                old_tree.GetEntry(x)
                old_tree.SetBranchAddress("clus_pt", cluster_pt_entry)
                old_tree.SetBranchAddress("clus_phi", cluster_phi_entry)
                old_tree.SetBranchAddress("clus_eta", cluster_eta_entry)
                old_tree.SetBranchAddress("clus_E", cluster_E_entry)
                old_tree.SetBranchAddress("fjet_pt", fjet_pt_entry)
                old_tree.SetBranchAddress("fjet_eta", fjet_feta_entry)
                old_tree.SetBranchAddress("fjet_phi", fjet_fphi_entry)
                old_tree.SetBranchAddress("fjet_E", fjet_fE_entry)
                old_tree.SetBranchAddress('fjet_truthJet_pt', fjet_truthJet_pt_entry)
                old_tree.SetBranchAddress("fjet_D2", fjet_D2_entry)
                old_tree.SetBranchAddress("fjet_Tau21_wta", fjet_Tau21_wta_entry)
                old_tree.SetBranchAddress("fjet_dRmatched_maxEParton_flavor",
                                          fjet_dRmatched_maxEParton_flavor_entry)

                QCD_pt_new.append(QCD_pt[x])
                Tree.Fill()


fnew.Write()
fnew.Close()
QCD_pt_new = np.array(QCD_pt_new)

print("tosscount = ", tosscount)
writecount = len(QCD_pt) - tosscount
print("writecount = ", writecount)
print("total = ", len(QCD_pt))

mylist1=["Background File","Signal File ", "Tree", "Selection","Selection QCD", "number of bins" ,"tosscount", "writecount"]
mylist2=[bkg_storage+bkg_file, sig_storage+sig_file,treename,selection,selectionQCD,str(Nbins), str(tosscount), str(writecount)]

folder ="InfoText/"
timestamp = writeinfofile(mylist1 = mylist1, mylist2=mylist2, folder=folder)

plt.figure()
plt.plot(ratio)
plt.title('Normalized Ratio of Signal to Background Jet Pt')
plt.xlabel('Bin')
plt.ylabel('Ratio (S/B)')
plt.grid(True)
plt.savefig("pt_distributions/"+sig_file.replace(".root","")+"_ratio_"+timestamp+".png")

plt.figure()
plt.hist(QCD_pt, 100, normed = 1, facecolor = 'red', alpha = 0.5, label = 'Background')
plt.hist(Wpt, 100, normed = 1, facecolor = 'green', alpha =0.5, label = 'Signal')
plt.title('Jet Pt Distribution of Signal and Background Before Random Events Tossed')
plt.xlabel('Jet Pt (GeV)')
plt.ylabel('Probability')
plt.legend(loc = 'best')
plt.grid(True)
plt.savefig("pt_distributions/"+sig_file.replace(".root","")+"_before_"+timestamp+".png")

plt.figure()
plt.hist(QCD_pt_new, 100, normed = 1, facecolor = 'red', alpha = 0.5, label = 'Background New')
plt.hist(Wpt, 100, normed = 1, facecolor = 'green', alpha =0.5, label = 'Signal')
plt.title('Jet Pt Distribtuion of Signal and Background After Random Events Tossed')
plt.xlabel('Jet Pt (GeV)')
plt.ylabel('Probability')
plt.legend(loc = 'best')
plt.grid(True)
plt.savefig("pt_distributions/"+sig_file.replace(".root","")+"_after_"+timestamp+".png")

print('All Done - Timestamp: ', timestamp)




