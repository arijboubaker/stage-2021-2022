import sys
from IPython import display
from fpdf import FPDF
from IPython.display import clear_output
import os
import cv2 as cv
import ipywidgets as widgets
import numpy as np
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image



image_path = sys.argv[1]
newname = image_path
filetype = newname.split('.')[-1]
oldname = "card_img." + filetype
path = newname

# initialize Variable
widthImg = 1920
heightImg = 1080
lower = 100
upper = 150
kernel = np.ones((5,5)) 
NAME = ""
ROLE = ""
COMPANY = ""
EMAIL = ""
PHONE = ""
WEBSITE = ""
ADDRESS = ""


# Read uploaded image
img_card = cv.imread(sys.argv[1])
img_card = cv.resize(img_card, (widthImg, heightImg), interpolation = cv.INTER_AREA)
img_card = cv.cvtColor(img_card, cv.COLOR_BGR2RGB)

     

# 1 convert to gray image
imgGray = cv.cvtColor(img_card, cv.COLOR_RGB2GRAY)

# 2 apply gaussian blur
imgBlur = cv.GaussianBlur(imgGray, (5, 5), 1)


def threshBar():

  threshBar.btn = widgets.Button(description = 'Canny Edge Detect',disabled = False,button_style = 'success',tooltip = 'Click me',)

  threshBar.lowerThresh = widgets.IntSlider(value=100, min=0,
                         max=255,
                          step=1,
                          description='lower threshold:',
                          disabled=False,
                          continuous_update=True,
                          orientation='horizontal',
                          readout=True,
                          readout_format='d'
                      )
  threshBar.upperThresh = widgets.IntSlider(
                          value=150,
                          min=0,
                          max=255,
                          step=1,
                          description='upper threshold:',
                          disabled=False,
                          continuous_update=True,
                          orientation='horizontal',
                          readout=True,
                          readout_format='d'
                          )

  def btn_clicked(b):
    global lower
    global upper
    lower = threshBar.lowerThresh.value
    upper = threshBar.upperThresh.value
    clear_output()
    display(threshBar.lowerThresh)
    display(threshBar.upperThresh)
    display(threshBar.btn)
    imgThreshold = cv.Canny(imgBlur, lower, upper)

  threshBar.btn.on_click(btn_clicked)

  imgThreshold = cv.Canny(imgBlur, lower, upper)

threshBar()

# 3 Apply Canny Edge detection
imgThreshold = cv.Canny(imgBlur, lower, upper)

# 4 Apply Dilation
imgDial = cv.dilate(imgThreshold, kernel, iterations=2)

# 5 Apply Erosion
imgErode = cv.erode(imgDial, kernel, iterations=1)

# 6 Find Contour
contours, hierarchy = cv.findContours(imgBlur, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

imgContours = img_card.copy()
cv.drawContours(imgContours, contours, -1, (0, 255, 0), 10)


# 7 Find biggest Contour
biggest = np.array([])
max_area = 0
for i in contours:
    area = cv.contourArea(i)
    if area > 5000:
        peri = cv.arcLength(i, True)
        approx = cv.approxPolyDP(i, 0.02 * peri, True)
        if area > max_area and len(approx) == 4:
            biggest = approx
            max_area = area
        else:
            print("no")

# 8 Reorder 4 points of contour's corner
myPoints = biggest      
myPoints = myPoints.reshape((4, 2))
myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
add = myPoints.sum(1)

myPointsNew[0] = myPoints[np.argmin(add)]
myPointsNew[3] =myPoints[np.argmax(add)]
diff = np.diff(myPoints, axis=1)
myPointsNew[1] =myPoints[np.argmin(diff)]
myPointsNew[2] = myPoints[np.argmax(diff)]
biggest_new = myPointsNew

# 9 Perform Perspective crop
pts1 = np.float32(biggest_new)
pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg], [widthImg, heightImg]])
matrix = cv.getPerspectiveTransform(pts1, pts2)
imgWarp = cv.warpPerspective(img_card, matrix, (widthImg, heightImg))
imgWarp = cv.resize(imgWarp, (widthImg, heightImg),interpolation = cv.INTER_AREA)
img_temp = imgWarp.copy()
img_temp = cv.cvtColor(img_temp, cv.COLOR_RGB2BGR)
cv.imwrite('colored_img.jpg', img_temp)


# // Convert cropped image to gray scale //
imgWarp = cv.cvtColor(imgWarp,cv.COLOR_RGB2GRAY)

# 10 Apply adaptive threshold
imgAdaptiveThre = cv.adaptiveThreshold(imgWarp, 255, 1, 1, 7, 2)
imgAdaptiveThre = cv.bitwise_not(imgAdaptiveThre)

# 11 Apply median blur
imgMed = cv.medianBlur(imgAdaptiveThre, 3)

cv.imwrite('scanned_card.jpg', imgMed) 
img_scan = cv.imread('scanned_card.jpg')


# Extract text from card using google tesseract Optical character recognition
extractedInformation = pytesseract.image_to_string(Image.open('scanned_card.jpg'))

# Get rid of some OCR error text extraction
splt = extractedInformation.split('\n')
for i in range(len(splt)-1, -1, -1):
  if len(splt[i]) < 4:
    del splt[i]
  else:
    space = True
    for j in splt[i]:
      if j != ' ' and j != '\t':
        space = False
    if space:
      del splt[i]

names_lower = []

for name in splt:
    names_lower.append(name.lower())
print(names_lower)



