#! /usr/bin/env python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
# import mpld3

stopwords = nltk.corpus.stopwords.words('english')

def load_lyrics(json_file):
    with open(json_file, 'rt') as f:
        data = json.load(f)
        


def main():
    pass

if __name__ == '__main__':
    main()