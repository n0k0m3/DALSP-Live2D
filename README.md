# Date A Live: Spirit Pledge Live2D

Generate L2D model for Live2DViewerEX

## Requirements

- [Python 3+](https://www.python.org/downloads/)
- pip modules `lupa` : `pip install lupa`

## Usage

General help

```
Date A Live: Spirit Pledge Live2D Live2DViewerEX

usage: main.py [-h] {get,gen} ...

Selectively copy folder structure for Live2D model to destination. Will output
MVLE file according to Live2DViewerEX spec

positional arguments:
  {get,gen}
    get       Generate Folder and MVLE files
    gen       Generate MVLE files from existing folder

optional arguments:
  -h, --help  show this help message and exit
```

`get` mode

```
> python main.py get -h

Date A Live: Spirit Pledge Live2D Live2DViewerEX

usage: main.py get [-h] [-l] [-n SPIRIT_NAME] [-r REGION] [-v] INPUT OUTPUT

positional arguments:
  INPUT                 Data Source (contains res, src, TFFramework folder)
  OUTPUT                Output Directory, Live2D Assets will be copied here

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List all available spirits and end the script
  -n SPIRIT_NAME, --name SPIRIT_NAME
                        Specify Spirit Name to generate L2D, default: all
  -r REGION, --region REGION
                        Specify the region of the data (EN/CN), default: EN
  -v, --verbose         Print debug messages to stdout
```

`gen` mode

```
> python main.py gen -h

Date A Live: Spirit Pledge Live2D Live2DViewerEX

usage: main.py gen [-h] [-v] WKFOLDER

positional arguments:
  WKFOLDER       Folder to generate MLVE

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Print debug messages to stdout
```

## Example

Data folder in `D:\DAL\DateALiveData`  
Export folder `D:\DAL\Live2D`  
Spirit L2D needed `Kotori`

```
> python main.py get D:\DAL\DateALiveData D:\DAL\Live2D -n kotori
```
