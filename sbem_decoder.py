import struct

# convert a description header containg a group tag to a list of ids
def getGroupFromDescriptorStr(descStr):
    ids = []
    if descStr.find('<PTH>') != -1:
        return None
    str_start = '<GRP>'
    str_end = '\\x00'
    ids = descStr[descStr.find(str_start)+len(str_start):descStr.rfind(str_end)].split(',')
    return (ids, 'group')

# convert a description header containing a path tag to a path with corresponding value type
def getPathFromDescriptorStr(descStr):
    path = ''
    frmt = ''
    if descStr.find('<GRP>') != -1:
        return None
    str_start = '<PTH>'
    str_end = '\\x00'
    if descStr.find('<FRM>') != -1:
        str_start = '<FRM>'
        frmt = descStr[descStr.find(str_start)+len(str_start):descStr.rfind(str_end)]
        str_start = '<PTH>'
        str_end = '\\n'
    else:
        frmt = 'array'
    path = descStr[descStr.find(str_start)+len(str_start):descStr.rfind(str_end)]
    return (path, frmt)

# check if descriptor chunk has path tag 
def isDescriptorStrPath(descStr):
    if descStr.find('<PTH>') != -1:
        return True
    return False

# convert group ids recursively to a list of paths
def getPathsFromGroupIds(descChunks, descGroupIds):
    
    dataChunkDesc = []
    for id in descGroupIds:
        descStr = str(descChunks[int(id) - 1])
        
        if isDescriptorStrPath(descStr):
            dataChunkDesc.append(getPathFromDescriptorStr(descStr))
        else:
            dataChunkDesc.append((getPathsFromGroupIds(descChunks, getGroupFromDescriptorStr(descStr)[0]), 'group')) 

    return dataChunkDesc

def getValuesFromDataChunk(dataChunk, dataChunkDesc, data_i):
    l = []
    # convert bytes to values depending on description. (function is made to work after using getPathsFromGroupIds )
    for desc in dataChunkDesc:
        if desc[1] == 'group':
            l.append(getValuesFromDataChunk(dataChunk, desc[0], data_i))
        if desc[1] == 'uint32':
            l.append(struct.unpack('<I', dataChunk[data_i[0]:data_i[0]+4])[0])
            data_i[0] += 4 
        if desc[1] == 'float32':
            l.append(struct.unpack('<f', dataChunk[data_i[0]:data_i[0]+4])[0])
            data_i[0] += 4   
    return l

def decodeDataChunks(dataChunks, descChunks):
    dataDescRes = []
    dataValuesRes = []
    for dataChunk in dataChunks:

        ret, dat = dataChunk

        # convert group ids into python lists
        descGroupIds = getGroupFromDescriptorStr(str(descChunks[ret[0] - 1][1]))[0] # take groups this descriptor has as basis
        dataChunkDesc = getPathsFromGroupIds(descChunks, descGroupIds) # recursively get all the paths and formats coresponding to the group ids
        
        # convert to values
        dataChunkValues = getValuesFromDataChunk(dat, dataChunkDesc, data_i=[0]) # read the data chunk using the descriptor, starting from data_i 0 (list used passing by ref)

        # save
        dataDescRes.append(dataChunkDesc)
        dataValuesRes.append(dataChunkValues)

    return dataValuesRes, dataDescRes
