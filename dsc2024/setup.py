#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright © 2024 Manoel Vilela
#
#    @project: nlp-tir
#     @author: Manoel Vilela
#      @email: manoel_vilela@engineer.com
#

import nltk


def nltk_download_packages():
    nltk.download('averaged_perceptron_tagger')
    nltk.download('movie_reviews')
    nltk.download('omw')
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('tagsets')
    nltk.download('treebank')
    nltk.download('wordnet')
