import numpy as np
import cv2
from PIL import Image
from file_utils import PathUtils, FileUtils
from msg_utils import Msg

operationFolder = PathUtils.get_curr_path()
readFolder = operationFolder + "/stimuli_samebody/renamed_layered/"
outFolder = operationFolder + "/stimuli_samebody/resized/"
FileUtils.create_dir(outFolder)

print(readFolder)
def resizeImg(imgName):
	im = Image.open(readFolder + imgName + '.png')
	im = im.resize((2400, 1822))
	im.save(outFolder + imgName + '.png')

listOfFiles = PathUtils.extract_all_files_with(readFolder,".png")
print(listOfFiles)

for file in listOfFiles:
	resizeImg(file)


#
# ## all of this below is for resizing
# # folder = path.join(getcwd(), "towerjsons\\valid_renamed\\")
# folder = path.join(getcwd(), "stims_bwPOSTCUT\\")
# save_folder = path.join(getcwd(), "stims_bwPOSTCUTresize150300\\")
# # actual loop would start here:
#
# _, _, files = next(walk(folder))
#
#
# file_count = int(len(files)/2)
# for i in np.arange(1,file_count+1):
# 	ims = Image.open(folder+"tower"+str(i)+"s"+".png")
# 	# ims_r = ims.resize((200,400))
# 	ims_r = ims.resize((150,300))
# 	ims_r.save(save_folder+"tower"+str(i)+"s"+".png")
#
# 	imu = Image.open(folder+"tower"+str(i)+"u"+".png")
# 	# imu_r = imu.resize((200,400))
# 	imu_r = imu.resize((150,300))
# 	imu_r.save(save_folder+"tower"+str(i)+"u"+".png")
