# resize all the images to same size
import os
from tqdm import tqdm

from PIL import Image
import numpy as np
import uniq
import gloabl


def resizepic():
    path = '/root/Desktop/webtools/gan/'+gloabl.g_name+'/'
    for filename in tqdm(os.listdir(path),desc ='reading images ...'):
        print("filename==>",filename)
        image = Image.open(path+filename)
        image = image.resize((1024,1024))
        image = np.array(image.convert("RGB"))
        image=Image.fromarray(image) # numpy 转 image类
        image.save(path+filename, image.format)


uniq.doprocess()
# for filename in tqdm(os.listdir(path),desc ='reading images ...'):
  