#!/usr/bin/env python
#-*- coding: utf8 -*-

# Created by William N. Havard (william.havard@gmail.com)
# Date created: 09/03/2018
# Date last modified: 12/03/2018
# PhD Student at LIDILEM and LIG/GETALP

import re

def en(token_list):
    # merge tokens
    text = ' '.join(token_list)

    remove_double_spaces = re.compile(r' +')
    remove_space_before_punct = re.compile(r' ([,.:;?!\'`/\(\)\[\]])')
    remove_space_after_punct = re.compile(r'([\'`/\(\)\[\]]) ')
    remove_inner_spaces = re.compile(r'" (.+?) "')

    text = text.strip()   
    text = text.replace('`', '\'') 
    text = remove_double_spaces.sub(' ', text)
    text = remove_space_before_punct.sub(r'\1', text)
    text = remove_space_after_punct.sub(r'\1', text)
    text = remove_inner_spaces.sub(r'"\1"', text) 
    return text

def rm_commentary(sentence):
    begin_=['<', '[', '(']
    end_=['>', ']', ')']
    if len(sentence)!=0 and sentence[0] not in begin_ and sentence[-1] not in end_:
        return sentence
    else:
        return None

def tokens_as_str(token_list):
    return ' '.join(token_list)

def transform(sentences_as_token_list, postprocess):
    for process in postprocess.split(','):
        process = process.strip()
        for i, sentence in enumerate(sentences_as_token_list):
            sentences_as_token_list[i]=globals()[process](sentences_as_token_list[i])
    return [x for x in sentences_as_token_list if x is not None]
