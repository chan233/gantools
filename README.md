在 stylegan2 炼丹过程中，你是否有过一下烦恼：
1. 不会爬虫：好一张一张的手扒百度图片
2. 爬出来图片：大量重复图片/尺寸不对/质量不高/不符合炼丹要求

以下是解决方法：

  resize.py 图片预处理 ，使用opencv规范图片到1024x1024，统一格式到png，统一转换通道到rgb
  
  uniq.py 图片去重处理
  
  crawling.py 爬取图片模块
  
requment.txt:
