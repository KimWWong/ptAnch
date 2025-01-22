#!/usr/bin/env python
import numpy as np
import os
from file_utils import PathUtils, FileUtils
from msg_utils import Msg

def main():

    operationFolder = PathUtils.get_curr_path()
    readFolder = operationFolder + "/stimuli_huichao/Images/"
    outFolder = operationFolder + "/stimuli_huichao/Images/"
    FileUtils.create_dir(outFolder)

    agentList = [0,1,2]
    location = ["none","top","bottom"]
    color = ["blue","green"]

    for i in np.arange(len(agentList)):
        for j in np.arange(len(location)):
            for k in np.arange(len(color)):
                if (location[j] == "none"):
                    print(location[j])
                    oldFile = readFolder + "vert_simon_" + str(agentList[i]) + '_' + str(location[j]) + '.png'
                    newFile = outFolder + "vert_simon_" + str(agentList[i]) + '_' + str(location[j]) + '_1.png'
                else:
                    oldFile = readFolder + "vert_simon_" + str(agentList[i]) + '_' + str(location[j]) + '_' + str(
                        color[k]) + '.png'
                    newFile = outFolder + "vert_simon_" + str(agentList[i]) + '_' + str(location[j]) + '_' + str(
                        color[k]) + '_1.png'

                if os.path.exists(oldFile):
                    FileUtils.rename_from_to(oldFile,newFile)

if(__name__=='__main__'):
	main()
