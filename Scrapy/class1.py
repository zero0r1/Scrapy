import pytesseract

from PIL import Image

image = Image.open('D:/support/xiangtianhao/Downloads/1.png')

vcode = pytesseract.image_to_string(image,lang='chi_sim')

print (vcode)