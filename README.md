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

\[1\] Ramy Baly, Giovanni Da San Martino, James Glass, and Preslav Nakov. 2020. We Can Detect Your Bias: Predicting the Political Ideology of News Articles. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pages 4982–4991, Online. Association for Computational Linguistics.

\[2\] M. T. Ribeiro, S. Singh, and C. Guestrin, “”why should I trust you?”: Explaining the predictions of any classifier,” in Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, San Francisco, CA, USA, August 13-17, 2016, pp. 1135–1144, 2016.