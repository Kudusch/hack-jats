#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tf_crawler as tf

import sys

def slugify(value):
    return(value.replace("/", "_"))

if ".txt" in sys.argv[1]:
    with open(sys.argv[1], "r") as f:
        dois = [doi.strip() for doi in f.readlines()]
else:
    dois = [sys.argv[1]]

for doi in dois:
    print(doi)
    try:
        tf.download_article(doi, file = f"example/{slugify(doi)}.json")
    except:
        pass