import sbem_parser
import sbem_decoder

import sys
import subprocess
import os
import sys
import datetime

# arguments
base_path = os.getcwd()

wbmd_file_path = './wbcmd.exe'
wbmd_zip_path = '../wbcmd_win.zip'

data_file_path = "data/logdata.txt"
descriptor_file_path = "data/logdata_desc.txt"
result_file_path = "data/logdata_res.txt"

use_files_only = False
use_simulator = True

if not use_files_only:
    # check if required files existing
    if not os.path.isfile(wbmd_file_path):
        print("could not find " + wbmd_file_path + ", unzipping...")
        if not os.path.isfile(wbmd_zip_path):
            print("could not find " + wbmd_zip_path + ", please place this repo in movesense-device-lib/tools/movesense-test-tools")
            sys.exit(0)
        subprocess.run(['unzip', wbmd_zip_path])

    # read data from simulator or device
    if use_simulator:
        print("trying to read data from simulator...")
        subprocess.run([wbmd_file_path, "--port", "TCP127.0.0.1:7809", "--path", "Mem/Logbook/byId/1/Data", "--op", "get", "--target", data_file_path])
        subprocess.run([wbmd_file_path, "--port", "TCP127.0.0.1:7809", "--path", "Mem/Logbook/byId/1/Descriptors", "--op", "get", "--target", descriptor_file_path])

        print("retrieved log data succesfully\nsaved log description as", descriptor_file_path)
        print("saved log data as", data_file_path)
    else:
        print("trying to read data from device on COM1")
        subprocess.run([wbmd_file_path, "--port", "COM1", "--path", "Mem/Logbook/byId/1/Data", "--op", "get", "--target", data_file_path])
        subprocess.run([wbmd_file_path, "--port", "COM1", "--path", "Mem/Logbook/byId/1/Descriptors", "--op", "get", "--target", descriptor_file_path])

        print("retrieved log data succesfully\nsaved file log description as", descriptor_file_path)
        print("saved log data as", data_file_path)

# parse the files
if not os.path.isfile(data_file_path):
    print("could not find", data_file_path)
    sys.exit(0)
if not os.path.isfile(descriptor_file_path):
    print("could not find", descriptor_file_path)
    sys.exit(0) 

# parse
print("parsing files...")
(dataChunks, descChunks) = sbem_parser.parseSbemFiles(data_file_path, descriptor_file_path)

# decode
print("decoding data...")
dataChunkValues, dataChunksDescriptors =  sbem_decoder.decodeDataChunks(dataChunks, descChunks)

# remove array markers
dataChunksDescriptors = [d for d in dataChunksDescriptors if d[1] != 'array']

# write results
if os.path.isfile(result_file_path):
    result_file_path = result_file_path.replace(".txt", '')
    result_file_path = result_file_path + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"

print("writing results as", result_file_path)
with open(result_file_path, 'w') as f:
    for i in range(0, len(dataChunkValues)):
        f.write(str(dataChunksDescriptors[i]) + "\n" + str(dataChunkValues[i]) + "\n\n")
sys.exit(0)