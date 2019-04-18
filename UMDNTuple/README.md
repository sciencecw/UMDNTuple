

```
cmsrel CMSSW_9_4_9_cand2
cd CMSSW_9_4_9_cand2/src
cmsenv
```

Check out the necessary tools and patches
```
git cms-init
git cms-merge-topic cms-egamma:EgammaID_949  ## this is not necessary after CMMSW94_13
git cms-merge-topic cms-egamma:EgammaPostRecoTools
git cms-merge-topic lathomas:L1Prefiring_9_4_9
mv src/L1Prefiring/EventWeightProducer/files src/L1Prefiring/EventWeightProducer/data ## for crab data transport
```

This might take some time

Get the ntuplizer
```
git clone https://github.com/albertobelloni/UMDNTuple
cd UMDNTuple
git checkout 94X2017
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
