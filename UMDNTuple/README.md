#Setup for 2016 data analysis

----------------------- YOU CAN SIMPLY COPY-PASTE THIS RECIPE  ------------------------

Make a working directory,
```
mkdir UMDNTuple
```

Setup CMSSW_9_4_9_cand2 (Eventually we will probably use CMSSW_10X for full Run 2)
```
cmsrel CMSSW_9_4_9_cand2

cd CMSSW_9_4_9_cand2/src

cmsenv
```

Merge the EgammaPostRecoTools for photon and electron objects (https://twiki.cern.ch/twiki/bin/viewauth/CMS/Egamma2016DataRecommendations)
```
git cms-init
git cms-merge-topic cms-egamma:EgammaPostRecoTools_940
git cms-merge-topic lathomas:L1Prefiring_9_4_9
```

Get the ntuplizer
```
git clone https://github.com/albertobelloni/UMDNTuple
cd UMDNTuple
git checkout legacy2016
cd UMDNTuple
scram b -j4
```

##To run the code
```
cd ${CMSSW_BASE}
cmsRun src/UMDNTuple/UMDNTuple/run_production_cfg.py  isMC=1
```
this will produce the ntuple.root under the current directory
(Note the default input file is no lxplus. You need to change it if on a different site.)

##To run with crab
after the standard settings to run crab (i.e., voms and source crab), 

```
cd ${CMSSW_BASE}/src/UMDNTuple/UMDNTuple
```
edit the datasets in `data_samples` and `mc_samples`, under `submit_crab.py`. Then

```
python submit_crab.py --version 0228
chmod 744 submit_crab.sh
./submit_crab.sh
```
Then the jobs will be submitted.
