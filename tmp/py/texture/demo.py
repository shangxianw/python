from PIL import Image
from PIL import ImageDraw
import os


fileArray = os.listdir()
# print(fileArray)
imgNameArray = []
imgArray = []
for fileName in fileArray:
	if os.path.splitext(fileName)[1] == ".png":
		imgNameArray.append(fileName)
# print(imgNameArray)

tWidth  = 0
tHeight = 0
for imgName in imgNameArray:
	filePath = "./" + imgName
	img = Image.open(filePath)
	imgArray.append(img)
	tHeight += img.size[1]
	if img.size[0] > tWidth:
		tWidth = img.size[0]
print(tWidth)
print(tHeight)


new_img = Image.new('RGBA', (tWidth, tHeight), (255, 255, 255, 0))
# mask    = Image.new('L', new_img.size)
# draw    = ImageDraw.Draw(mask)
# haArea  = (0, 0, tWidth,tHeight)
# draw.rectangle(haArea, fill=0)
# new_img.putalpha(mask)
x = 0
y = 0
for img in imgArray: 
	width, height = img.size 
	new_img.paste(img, (x, y))
	y += height
new_img.save("./img/ok.png")


