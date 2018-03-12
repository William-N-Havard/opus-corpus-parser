#!/usr/bin/env python
#-*- coding: utf8 -*-

# Created by William N. Havard (william.havard@gmail.com)
# Date created: 09/03/2018
# Date last modified: 12/03/2018
# PhD Student at LIDILEM and LIG/GETALP

import re

def en(text):
    remove_double_spaces = re.compile(r' +')
    remove_space_before_punct = re.compile(r" ([,.:;?!'])")

    text = text.strip()
    text = text.replace('`', '\'')
    text = text.replace(' \'','\'')
    text = text.replace('\' ','\'')    
    text = text.replace(' "', '"')
    text = text.replace('" ', '"')
    text = remove_double_spaces.sub(' ', text)
    text = remove_space_before_punct.sub(r'\1', text)
    return text

def transform(sentences_as_list, postprocess):
    for process in postprocess.split(','):
        for i, sentence in enumerate(sentences_as_list):
            sentences_as_list[i]=globals()[process](sentences_as_list[i])
    return sentences_as_list
