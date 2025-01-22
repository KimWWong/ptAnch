from PIL import Image
import math
import numpy as np

readFolder = "stimuli_sideview/"
outFolder = "stimuli_sideview/auto/"


def layerImages(backgroundImg, firstLayerImg, secondLayerImg, newImgName):
    baseImg = Image.open(readFolder + backgroundImg + ".png")
    baseImg = baseImg.convert("RGBA")
    # old_width, old_height = img.size
    # print(baseImg.size)

    firstImg = Image.open(readFolder + firstLayerImg + ".png")
    firstImg = firstImg.convert("RGBA")
    # print(mondImg.size)

    if secondLayerImg != 0:
        secondImg = Image.open(readFolder + secondLayerImg + ".png")
        secondImg = secondImg.convert("RGBA")

    # baseImg.paste(blockImg, (250,100), blockImg)
    baseImg.paste(firstImg, (0, 0), firstImg)
    # ## new method to deal with artifacts
    # Image.alpha_composite(baseImg, addImg).save(outFolder + newFileName+ ".png", format="png")

    if secondLayerImg != 0:
        baseImg.paste(secondImg, (0, 0), secondImg)

    baseImg.save(outFolder + newImgName + ".png", "PNG")


possAgent = ["fb", "f"]
possColor = ["b", "r", "gl", "gd"]
# possSym = [1,2,3,4,6]
# finalSym = [6]
# possNum = [16,91]
# possSym = [1,2,3]
possSym = [4]
finalSym = 4
possNum = [16, 91]


# ## for two image pasting
# for i in np.arange(len(possAgent)):
#     for j in np.arange(len(possNum)):
#         for k in np.arange(len(possSym)):
#             for l in np.arange(len(possColor)):
#                 for m in np.arange(len(possColor)):
#                     backgroundName = "blank_" + possAgent[i]
#                     # secondImgName = "u" + str(possSym[k]) + "_" + possColor[m]
#                     secondImgName = "symJ" + str(possSym[k]) + "_" + possColor[m]
#
#                     if possSym[k] == finalSym:
#                         firstImgName = str(possNum[j]) + "_" + possColor[l]
#                         newImgName = possAgent[i] + str(possNum[j]) + "_" + possColor[l] + "_" + possColor[m]
#                     else:
#                         # firstImgName = "sym" + str(possSym[k]) + "_" + possColor[l]
#                         # newImgName = possAgent[i] + "sym" + str(possSym[k]) + "_" + possColor[l] + "_" + possColor[m]
#                         firstImgName = "symT" + str(possSym[k]) + "_" + possColor[l]
#                         newImgName = possAgent[i] + "sym" + str(possSym[k]) + "_" + possColor[l] + "_" + possColor[m]
#
#                     layerImages(backgroundName, firstImgName, secondImgName, newImgName)

## for just a single symbol pasting
for i in np.arange(len(possAgent)):
    for j in np.arange(len(possNum)):
        for k in np.arange(len(possSym)):
            for l in np.arange(len(possColor)):
                backgroundName = "blank_" + possAgent[i]
                if possSym[k] == finalSym:
                    firstImgName = str(possNum[j]) + "_" + possColor[l]
                    newImgName = possAgent[i] + str(possNum[j]) + "_" + possColor[l]
                else:
                    # firstImgName = "symT" + str(possSym[k]) + "_" + possColor[l]
                    # newImgName = possAgent[i] + "sym" + str(possSym[k]) + "_" + possColor[l]
                    firstImgName = "symR" + str(possSym[k]) + "_" + possColor[l]
                    newImgName = (
                        possAgent[i] + "sym" + str(possSym[k]) + "_" + possColor[l]
                    )

                layerImages(backgroundName, firstImgName, 0, newImgName)
