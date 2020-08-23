# Date A Live: Spirit Pledge Live2D

Generate L2D model for Live2DViewerEX

## Requirements

- [Python 3+](https://www.python.org/downloads/)
- pip modules `lupa` : `pip install lupa`

## Usage

```
> python main.py -h

Date A Live: Spirit Pledge Live2D

Selectively copy folder structure for Live2D model to destination

Usage: main.py [options]

Options:
  -h, --help            show this help message and exit
  -d "DATA_FOLDER", --data="DATA_FOLDER"
                        Data Source (contains res, src, TFFramework folder)
  -o "OUTPUT", --output="OUTPUT"
                        Output Directory, Live2D Assets will be copied here
  -n "SPIRIT_NAME", --name="SPIRIT_NAME"
                        Decrypted Data Destination (MUST BE A FOLDER)
  -v, --verbose         Print debug messages to stdout
```

## Example

Data folder in `D:\DAL\DateALiveData`  
Export folder `D:\DAL\Live2D`  
Spirit L2D needed `Kotori`

```
> python main.py -d D:\DAL\DateALiveData -o D:\DAL\Live2D -n kotori

Date A Live: Spirit Pledge Live2D

Selectively copy folder structure for Live2D model to destination

[INFO] Spirit Name: Itsuka Kotori                 ID: 105
[INFO] Done!
```
