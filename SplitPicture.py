from PIL import Image

'''
将一张图片的左半部分截取下来，左右颠倒之后旋转 180°；
将图片的右半边不作更改粘贴到左半部分；
最后将修改过的左半部分粘贴到右半部分
'''
def iamge_transpose(image):
    xsize, ysize = image.size           # 获取图片尺寸
    xsizeLeft    = xsize // 2           # 获取左半边图片尺寸(// 取商整数部分)

    # 定义左、上、右和下像素坐标的四元组
    boxLeft      = (0, 0, xsizeLeft, ysize)
    boxRight     = (xsizeLeft, 0, xsize, ysize)
    boxLeftNew   = (0, 0, xsize - xsizeLeft, ysize)
    boxRightNew  = (xsize - xsizeLeft, 0, xsize, ysize)

    # transpose() 可以将图片左右上下颠倒和旋转
    # 旋转颠倒左半部分图片
    partLeft     = image.crop(boxLeft).transpose(Image.FLIP_LEFT_RIGHT).\
        transpose(Image.ROTATE_180)
    # 右半部分图片保持不变
    partRight    = image.crop(boxRight)

    # 将右半部分图片黏贴到左边部分，左半部分黏贴到右半部分
    image.paste(partRight, boxLeftNew)
    image.paste(partLeft, boxRightNew)
    return image


img = Image.open('./Xuuuuu.jpg') # 打开指定位置的图片

img = iamge_transpose(img)

img.save('result.jpg')           # 保存图片

img.show()                       # 显示图片