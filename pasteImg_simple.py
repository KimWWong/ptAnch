from PIL import Image
import numpy as np
from file_utils import PathUtils, FileUtils

operationFolder = PathUtils.get_curr_path()
readFolder = operationFolder + "/stimuli_samebody/base_prename/"
addFolder = operationFolder + "/stimuli_samebody/frag/"
outFolder = operationFolder + "/stimuli_samebody/renamed_layered/"


def layerImages(ogFileName, addFileName, newFileName):
    # baseImg = Image.open(backgroundFileName)
    baseImg = Image.open(readFolder + ogFileName)
    baseImg = baseImg.convert("RGBA")

    # addImg = Image.open(readFolder + ogFileName + ".png")
    addImg = Image.open(addFolder + addFileName)
    addImg = addImg.convert("RGBA")

    # baseImg.paste(addImg, (0,0), addImg)
    # baseImg.save(outFolder + newFileName+ ".png", "PNG")
    ## new method to deal with artifacts
    Image.alpha_composite(baseImg, addImg).save(outFolder + newFileName, format="png")


# listOfFiles = PathUtils.extract_all_files_with(readFolder,".png")
# print(listOfFiles)
#
# for i in np.arange(len(listOfFiles)):
#     layerImages(listOfFiles[i], backgroundFolder + "resizedframe-brownwall-greentable-whiteboard2.png", listOfFiles[i])

# people = ['gray_gray','caucasian_female', 'caucasian_male', 'black_female', 'black_male']
# correspond_people = ['0','1','2','3','4']
# buttons = ['gray_gray','gray_blue','gray_green','blue_gray','green_gray']
# correspond_buttons = ['none','bottom_blue','bottom_green','top_blue','top_green']

# people = [
#     "gray_gray",
#     "caucasian_female",
#     "caucasian_male",
#     "black_female",
#     "black_male",
#     "black_female2",
#     "caucasian_male2",
# ]
people = [
    "caucasian_male2",
]
# correspond_people = ["0", "1", "2", "3", "4", "5", "6"]
correspond_people = ["6"]
buttons = [
    "gray_gray",
    "brighter_gray_blue",
    "brighter_gray_green",
    "brighter_blue_gray",
    "brighter_green_gray",
]
correspond_buttons = ["none", "bottom_blue", "bottom_green", "top_blue", "top_green"]

for i in np.arange(len(people)):
    for j in np.arange(len(buttons)):
        layerImages(
            ogFileName=people[i] + ".png",
            addFileName=buttons[j] + "_frag.png",
            newFileName="vert_simon_"
            + correspond_people[i]
            + "_"
            + correspond_buttons[j]
            + ".png",
        )
