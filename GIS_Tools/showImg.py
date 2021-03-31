import os
from PIL import Image
import matplotlib.pyplot as plt

dir = 'G:/shuj/我的课程/数据集/CCF遥感影像地块分割/'
img_name = 'tif1'
img_before = Image.open(os.path.join(dir,'img_testA/'+ img_name+'.jpg'))
img_results = Image.open(os.path.join(dir,'results/'+img_name+'.png'))

plt.figure("Image")

plt.subplot(1, 2, 1)
plt.imshow(img_before)
plt.title('img_before') # 图像题目

plt.subplot(1,2,2)
plt.imshow(img_results)
plt.title('img_results') # 图像题目

plt.tight_layout()
plt.show()