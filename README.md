# Leveraging Language Models for Temporal Political Bias Analysis

Clayton Carlson, Ryan Diaz, Charlie Rapheal, Sanjali Roy

## Setup

Create the necessary environment using Conda:

`conda env create -n csci5541project --file environment.yml`

## Functionality

**Sanity Check**: To run politicalBiasBERT on the test set used in Baly et al. 2020 [1], 

`python test_set_inference.py`

**Inference on Transcripts**: To run inference on politicalBiasBERT on a given dataset of transcripts,

`python transcripts_inference.py --dataset DATASET --filter_cnn FILTER_CNN`

where `DATASET` can be one of `['fox_news', 'tucker', 'lemon', 'nyt', 'cnn_ltm', 'cnn_lad']` and `FILTER_CNN` can be either `True` or `False`

**Interpretation of Transcripts**: To run LIME (Local Interpretable Model-Agnostic Explanations [2]) on a dataset of transcripts,

`python transcripts_inference.py --dataset DATASET --filter_cnn FILTER_CNN`

where `DATASET` can be one of `['fox_news', 'tucker', 'lemon', 'nyt', 'cnn_ltm', 'cnn_lad']` and `FILTER_CNN` can be either `True` or `False`
