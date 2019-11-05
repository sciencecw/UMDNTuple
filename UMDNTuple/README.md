

```
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
cmsenv
```

Check out the necessary tools and patches
```
git cms-init
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaPostRecoRecipes#2018_Data_MC
git cms-merge-topic cms-egamma:EgammaPostRecoTools
git cms-merge-topic cms-egamma:PhotonIDValueMapSpeedup1029 #optional but speeds up the photon ID value module so things fun faster
git cms-addpkg EgammaAnalysis/ElectronTools
rm EgammaAnalysis/ElectronTools/data -rf
git clone git@github.com:cms-data/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools/data
scram b -j8
```

This might take some time

Get the ntuplizer
```
git clone https://github.com/albertobelloni/UMDNTuple
cd UMDNTuple
git checkout 102XFullRunII
cd UMDNTuple
scram b -j8
```

To run the code
```
cd ${CMSSW_BASE}
cmsRun src/UMDNTuple/UMDNTuple/run_production_cfg.py  isMC=1
```

To run with crab

```
python src/UMDNTuple/UMDNTuple/submit_crab.py --version 0228
chmod 744 submit_crab.sh
./submit_crab.sh
```
