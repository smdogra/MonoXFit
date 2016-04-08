# MonoXFit

## Installation

```bash
setenv SCRAM_ARCH slc6_amd64_gcc481
cmsrel CMSSW_7_1_5
cd CMSSW_7_1_5/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
git clone https://gitlab.com/sidnarayanan/MonoXFit MonoX
scram b -j16
```

## Produce fitting trees

1. Modify `config/categories_config.py` to point to the correct input root file
2. Call `python buildModel.py categories_config` to create `mono-x.root`
3. Call `python runModel.py` to create `combined-model.root`

## Running a single fit

`datacards/combined.txt` is the full datacard for this analysis. You can choose which signal model to use by uncommenting the appropriate line. The datacard automatically points to the `combined-model.root` file one directory up. **Any changes to the datacard must be made here and in the datacard used for scans (see below)**

To run the fit:

```bash
cd datacards/
combine -M MaxLikelihoodFit combined.txt --saveShapes --saveWithUncertainties
```

## Running the limit scan

`datacards/combined_tmpl.txt` is identical to `combined.txt`, except the signal model is not specified. **Any changes to the scan datacard must be made here and in the datacard used for fits (see above)**

To run the scan:

```bash
cd datacards/
python scan.py
```

The results are dumped in `*_obs_limits.txt`

## Making postfit plots

All plotting tools are in `plotting/`. They must be run after running the fit (or limit scan, depending on what plots you want to make). These scripts automatically point to the ROOT files generated by the above combine calls, so there is nothing you need to do.

```bash
python plot_ratio.py                                             # plots the xfer factors - no need to rerun now that the inputs are finalized
python plotStackedPostFit.py                                     # makes the stack plots with prefit and postfit comparisons to data
python diffNuisances.py -g pulls.root ../datacards/mlfit.root    # draws the pulls plot
python plotLimits.py                                             # makes the limit plots (both sigma and sigma/sigma_theory)
```

The output directories are specified inside the above scripts and will need to be changed to fit the user's preferences. This should probably be changed to an environment variable.

