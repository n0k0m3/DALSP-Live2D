# Date A Live: Spirit Pledge Live2D

Generate L2D model for Live2DViewerEX

## Requirements

- [Python 3+](https://www.python.org/downloads/)
- pip modules `lupa` : `pip install lupa`

## Usage

```
> python main.py -h

Date A Live: Spirit Pledge Live2D

usage: main.py [-h] [-v] INPUT OUTPUT SPIRIT_NAME

Selectively copy folder structure for Live2D model to destination

positional arguments:
  INPUT          Data Source (contains res, src, TFFramework folder)
  OUTPUT         Output Directory, Live2D Assets will be copied here
  SPIRIT_NAME    Decrypted Data Destination (MUST BE A FOLDER)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Print debug messages to stdout
```

## Example

Data folder in `D:\DAL\DateALiveData`  
Export folder `D:\DAL\Live2D`  
Spirit L2D needed `Kotori`

```
> python main.py D:\DAL\DateALiveData D:\DAL\Live2D kotori

Date A Live: Spirit Pledge Live2D

Selectively copy folder structure for Live2D model to destination

[INFO] Spirit Name: Itsuka Kotori                 ID: 105
[INFO] Done!
```
