# movesense-test-tools
python simple tools for testing a movesense device

# installation
This installation assumes you already have cloned [movesense-device-lib](https://bitbucket.org/suunto/movesense-device-lib/src/master/)
1. Go into the tools folder and clone this repository
```
cd movesense-device-lib/tools
git clone https://github.com/krebsalad/movesense-test-tools.git
cd movesense-test-tools
```
# usage
* get_log_data.py : a script that can be used with the [wbcmd tool](http://www.movesense.com/docs/esw/tools/) in combination with the device (with programming jig) or simulator to read data log data. The script will automatically run sbem_parser and sbem_decoder
* sbem_parser.py : a script for parsing sbem data. This script was taken from [this](https://stackoverflow.com/questions/52992615/movesense-decode-sbem-data-from-logbook) stackoverflow article with minor changes
* sbem_decoder.py : a script to decode the data on basis of the descriptor chunks and data chunks parsed by the sbem_parser
* gen_csv.py : run this script to generate a (obviously) fake acc, gyro and magn csv file as data/accelerometer.csv.
