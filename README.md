# Date A Live: Spirit Pledge Live2D

Generate L2D model for Live2DViewerEX

## Requirements

- [Python 3+](https://www.python.org/downloads/)
- pip modules `lupa` : `pip install lupa`

## Usage

```
> python main.py -h

Date A Live: Spirit Pledge Live2D Live2DViewerEX

usage: main.py [-h] [-l] [-n SPIRIT_NAME] [-r SPIRIT_NAME] [-v] INPUT OUTPUT

Selectively copy folder structure for Live2D model to destination. Will output
MVLE file according to Live2DViewerEX spec

positional arguments:
  INPUT                 Data Source (contains res, src, TFFramework folder)
  OUTPUT                Output Directory, Live2D Assets will be copied here

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List all available spirits and end the script
  -n SPIRIT_NAME, --name SPIRIT_NAME
                        Specify Spirit Name to generate L2D, default: all
  -r SPIRIT_NAME, --region SPIRIT_NAME
                        Specify the region of the data (EN/CN), default: EN
  -v, --verbose         Print debug messages to stdout
```

## Example

Data folder in `D:\DAL\DateALiveData`  
Export folder `D:\DAL\Live2D`  
Spirit L2D needed `Kotori`

```
> python main.py D:\DAL\DateALiveData D:\DAL\Live2D -n kotori
```
