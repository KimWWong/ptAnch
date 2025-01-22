#!/usr/bin/env python
import numpy as np
import os
from file_utils import PathUtils, FileUtils
from msg_utils import Msg
from PIL import Image


def main():

    operationFolder = PathUtils.get_curr_path()
    readFolder = operationFolder + "/stimuli_samebody/resized/"
    outFolder = operationFolder + "/stimuli_samebody/temp/"
    FileUtils.create_dir(outFolder)

    agentList = [0, 1, 2, 3, 4, 5, 6]
    location = ["top", "bottom", "none"]
    color = ["blue", "green"]

    for i in np.arange(len(agentList)):
        for j in np.arange(len(location)):
            for k in np.arange(len(color)):
                if location[j] == "none":
                    oldFile = (
                        readFolder
                        + "vert_simon_"
                        + str(agentList[i])
                        + "_"
                        + str(location[j])
                        + ".png"
                    )
                    newFile = (
                        outFolder
                        + "vert_simon_"
                        + str(agentList[i])
                        + "_"
                        + str(location[j])
                        + "_1.png"
                    )
                else:
                    oldFile = (
                        readFolder
                        + "vert_simon_"
                        + str(agentList[i])
                        + "_"
                        + str(location[j])
                        + "_"
                        + str(color[k])
                        + ".png"
                    )
                    newFile = (
                        outFolder
                        + "vert_simon_"
                        + str(agentList[i])
                        + "_"
                        + str(location[j])
                        + "_"
                        + str(color[k])
                        + "_1.png"
                    )

                if os.path.exists(oldFile):
                    img = Image.open(oldFile)
                    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    flipped_img.save(newFile)


if __name__ == "__main__":
    main()
