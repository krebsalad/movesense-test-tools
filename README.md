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
get_log_data.py : a script that can be used in combination with the simulator or device (with programming jig) to read data from the sensor
sbem_parser.py : a script for reading sbem data. This script was taken from [this](https://stackoverflow.com/questions/52992615/movesense-decode-sbem-data-from-logbook) stackoverflow article
sbem_decoder.py : a script to decode the data on basis of the descriptor chunks and data chunks parsed by the sbem_parser
gen_csv.py : run this script to generate a fake acc, gyro and magn csv file as  data/accelerometer.csv. (Used to verify if data is loaded correctly in the simulator)