#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tf_crawler as tf

doi = "10.1080/21670811.2021.1962728"

article = tf.download_article(doi, "test.json")