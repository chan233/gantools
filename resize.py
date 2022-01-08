#coding: utf-8
"""
采用多进程加快处理。添加了在读取图片时捕获异常，OpenCV对大分辨率或者tif格式图片支持不好
处理数据集 和 标签数据集的代码：（主要是对原始数据集裁剪）
    处理方式：分别处理
    注意修改 输入 输出目录 和 生成的文件名
    output_dir = "./label_temp"
    input_dir = "./label"
"""
import multiprocessing
import cv2
import os
import time
import random
g_x = 0
g_y = 0


def get_img(input_dir):
    img_paths = []
    print("input_dir ==>",input_dir)
    for (path,dirname,filenames) in os.walk(input_dir):
        for filename in filenames:
            img_paths.append(path+'/'+filename)
    print("img_paths:",img_paths)
    return img_paths

'''
                        xmax,ymax  
-------------------------
|                       |
|                       |
|                       |
|                       |
|                       |                  
-------------------------     
x0,y0                      
   

'''
def randomseed(height,weight):
    xend =  random.randint(g_x,weight) 
    xstart = xend - g_x 
    yend = random.randint(g_y,height) 
    ystart = yend - g_y 
    #print('ystart %d,yend %d,xstart %d,xend %d'%(ystart,yend,xstart,xend))
    return ystart,yend,xstart,xend
    

def cut_img(img_paths,output_dir):
    imread_failed = []
    try:
        img = cv2.imread(img_paths,1)
        height, weight = img.shape[:2]   
        if height < g_y or weight < g_x:
            print('image size not enough to reszie')
            return imread_failed    
        ystart,yend,xstart,xend = randomseed(height,weight)
        cropImg = img[ystart:yend, xstart:xend] # random reszie 1024*1024
        cropImg = cv2.cvtColor(cropImg, cv2.COLOR_BGR2RGB) # convert to rgb
        cv2.imwrite(output_dir + '/' + img_paths.split('/')[-1].split('.')[0]+".png",cropImg)  #save to png
  
        
    except Exception as e:
        print(str(e))
        print('imwrite failed...',img_paths)
        imread_failed.append(img_paths)
        
    return imread_failed


def main(input_dir,output_dir):
    img_paths = get_img(input_dir)
    scale = len(img_paths)

    results = []
    pool = multiprocessing.Pool(processes = 20)
    for i,img_path in enumerate(img_paths):
        a = "#"* int(i/10)
        b = "."*(int(scale/10)-int(i/10))
        c = (i/scale)*100
        results.append(pool.apply_async(cut_img, (img_path,output_dir )))
        print('{:^3.3f}%[{}>>{}]'.format(c, a, b)) # 进度条（可用tqdm）
       
    
    pool.close()                        # 调用join之前，先调用close函数，否则会出错。
    pool.join()                         # join函数等待所有子进程结束
    # for result in results:
    #     print('image read failed!:', result.get())
    print ("All done.")



if __name__ == "__main__":
    input_dir = '/root/Desktop/git/gantools/alphacoders/space'      # 读取图片目录表
    output_dir = '/root/Desktop/git/gantools/alphacoders/out'   # 保存截取的图像目录
    g_x = 1024
    g_y = 1024
    main(input_dir, output_dir)

