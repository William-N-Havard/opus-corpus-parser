# opus-corpus-parser
Download, parse and postprocess any Opus monolingual file. **Python 2.7 and 3 compatible** (significantly slower with Python 2.7 though)

This Python script allows you to download, extract and postprocess any monolingual file from the [Opus Database](http://opus.nlpl.eu/index.php). Each file in the .tar.gz file is extracted and read into memory so that no temporary file is created. The XML file is then parsed and raw text is outputed in a .txt file. The original .tar.gz directory structure is kept unchanged.

The user can specify its own processing functions, which make the processing operation language independent. As for now, only a basic English detokenizer has been provided. 

# Usage
```
python[2.7|3] opus-corpus-parser.py URL --outdir='./my-outdir' --ext='.txt' --transform='en' --verbose
```

**URL**: URL of file to be downloaded (e. g. http://opus.nlpl.eu/download.php?f=OpenSubtitles/ro.tar.gz)

**--outdir**: Path where processed files will be saved. If not path is provided, path name will be derived automatically

**--ext**: Extension that will be given to the processed files

**--tranform**: Post-process each sentence with a user-specified function (to be found in [detokenizer.py](detokenizer.py).
(e. g. --transform="my_fct, en" will first transform each sentence using "my_fct" in [detokenizer.py](detokenizer.py) and will then process each sentence using the "en" function)

**--verbose**: Increase verbosity

# Credits
[Opus Database - http://opus.nlpl.eu/index.php](http://opus.nlpl.eu/index.php)
**Jörg Tiedemann**, 2012, Parallel Data, Tools and Interfaces in OPUS.  [\[pdf\]](http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf)  *In  Proceedings of the 8th International Conference on Language Resources and Evaluation (LREC'2012)*
