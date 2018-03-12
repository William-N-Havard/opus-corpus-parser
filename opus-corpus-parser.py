#!/usr/bin/env python
#-*- coding: utf8 -*-

# Created by William N. Havard - william.havard@gmail.com
# PhD Student at LIDILEM and LIG/GETALP
#
# Date created: 09/03/2018
# Date last modified: 12/03/2018
#
# Python 2 and 3 compatible :)

import os
import gzip
import tarfile
import argparse
import detokenizer
from pprint import pprint
import xml.etree.ElementTree as ET
# Python 2.7/3 compatibility
try:
    from urllib.request import urlretrieve as download
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urllib import urlretrieve as download
    from urlparse import urlparse, parse_qs


# Utils

def _filename_from_URL(url_):
    parsed_url = urlparse(url_)
    parsed_query = parse_qs(parsed_url.query)
    return parsed_query['f'][0]


def _get_path(path):
    return os.path.split(path)[0]


def _get_bare_filename(path):
    while '.' in path:
        path = os.path.splitext(os.path.basename(path))[0]
    return path


def _get_filename(path):
    return os.path.basename(path)


def _get_extensions(path):
    ext = []
    while '.' in path:
        ext.append(os.path.splitext(os.path.basename(path))[1])
        path = os.path.splitext(os.path.basename(path))[0]
    return ''.join(reversed(ext))

#

def parse_xml(xml_data):
    sentences = []
    root = ET.fromstring(xml_data)
    for sentence in root.iter('s'):
        sentences.append([token.text for token in sentence.iter(tag='w')])
    return sentences


def get_gz_data(gz):
    with gzip.GzipFile(fileobj=gz) as read_gz_file:
        return read_gz_file.read().decode('utf8', 'ignore')


def process_gz_file(data, xml_outdir, postprocess): 
    # Create dir if necessary
    if not os.path.exists(_get_path(xml_outdir)):
        os.makedirs(_get_path(xml_outdir))

    # Process file and dump data
    try:
        with open(xml_outdir, 'wb') as write_xml:
            parsed_xml = parse_xml(data.encode('utf8'))
            sentences = process_sentences(parsed_xml, postprocess)
            for sentence in sentences:
                write_xml.write(sentence.encode('utf8')+b'\n')
        return None
    except:
        return xml_outdir       


def process_sentences(sentences_as_token_list, postprocess):
    if postprocess == None:
        postprocess = 'tokens_as_str'
    return detokenizer.transform(sentences_as_token_list, postprocess)


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='Parameters for XML parser.')
    parser.add_argument('URL',
                        help='URL of file to be downloaded\
                             (e. g. http://opus.nlpl.eu/download.php?f=OpenSubtitles/ro.tar.gz)')
    parser.add_argument('--outdir', default="./",
                        help='Path where processed files will be saved')
    parser.add_argument('--ext', default=".txt",
                        help='Extension that will be given to the processed files')
    parser.add_argument('--transform', default=None,
                        help='Post-process each sentence with a user-specified function (to be found in detokenizer.py)\
                        \n (e. g. --transform="default, en" will first transform each sentence using "default" function \
                        in detokenizer.py and will then process each sentence using the "en" function)')
    parser.add_argument('--verbose', action="store_true", default=False,
                        help='Increase verbosity')

    args = parser.parse_args()
    dataset_url = args.URL
    outdir = args.outdir
    verbose = args.verbose
    suffix = args.ext
    transform = args.transform

    # setting up names
    dataset_bare_filename = _get_bare_filename(_filename_from_URL(dataset_url))
    dataset_filename = _get_filename(_filename_from_URL(dataset_url))
    final_outdir = os.path.join(outdir, dataset_bare_filename)
    final_outname = os.path.join(final_outdir, dataset_filename)

    # create outdir
    if os.path.exists(final_outdir) == False:
        if verbose:
            print("Creating output directory {} ...".format(final_outdir))
        os.makedirs(final_outdir)

    # Download XML corpus
    if verbose:
        print("Downloading corpus from {} ...".format(dataset_url))
    download(dataset_url, final_outname)
    if verbose:
        print("Saved to {} ...".format(final_outname))

    if verbose:
        print("Reading file {} ...".format(final_outname))

    # Open .tar file
    ext = _get_extensions(dataset_filename)
    errors = []
    if ext == '.tar.gz':
        with tarfile.open(final_outname, 'r') as zipped_data:
            # List .gz files
            file_list = zipped_data.getnames()
            nb_files = len(file_list)
            for i_, gz_file in enumerate(file_list):
                i_ += 1
                if verbose:
                    print("[{}/{}]({} errors) Processing file {} ...".format(i_, nb_files, len(errors), _get_bare_filename(gz_file)))
                # Get data
                compressed_gz_file = zipped_data.extractfile(gz_file)
                gz_data = get_gz_data(compressed_gz_file)
                # Get path
                path_ = os.path.join(final_outdir, _get_path(gz_file))
                xml_outdir = os.path.join(path_, _get_bare_filename(gz_file)+suffix)
                # Parse XML and dump data
                e=process_gz_file(gz_data, xml_outdir, transform)
                if e != None: errors.append(e)

        if errors!=[]:
            print('Warning: could not process the following files:')
            for e_files in errors:
                print('\t{}'.format(e_files))

    elif ext == '.xml.gz':
        print('Error: Wrong file format! As for now, this program\
               only supports monolingual XML files')
        exit()
    else:
        print('Error: Unknown file format!')
        exit()

    if os.path.exists(final_outname):
        os.remove(final_outname)

if __name__ == '__main__':
    main()
