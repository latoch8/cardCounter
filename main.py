import numpy as np
#import imutils
import cv2
from pygame.math import Vector2 
import time
from pathlib import Path
from PIL import ImageGrab

###########################################################
##################### Do pliku config #####################
###########################################################
pathPlayerPattern = 'pattern1.jpg'
playerArea = [Vector2(495,800),Vector2(580,830)]
pathCroupierPattern = 'pattern2.jpg'
croupierArea = [Vector2(500,660),Vector2(570,690)]
dirPlayerCards = Path('./Player/')
dirCroupierCards = Path('./Croupier/')
###########################################################

def save_paterns():
  #Player
  img = take_screenshot(playerArea)
  save_photo(img,pathPlayerPattern)
  #Croupier
  img = take_screenshot(croupierArea)
  save_photo(img,pathCroupierPattern)
  return

def take_screenshot(area):
  leftCorner = area[0]
  rightCorner = area[1] 
  img = ImageGrab.grab()
  capturedScreen = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
  cropedScreen = capturedScreen[int(leftCorner.y):int(rightCorner.y), int(leftCorner.x):int(rightCorner.x)]
  return cropedScreen

#Load pattern picture and resize
def open_image_and_resize(corners, filepath):
  dif_size = corners[1]-corners[0]
  img = cv2.imread(filepath)
  img = cv2.resize(img, (int(dif_size.x), int(dif_size.y)), interpolation=cv2.INTER_LINEAR)
  return img

def load_paterns():
  tempPlayerPattern = open_image_and_resize(playerArea, pathPlayerPattern)
  tempCroupierPattern = open_image_and_resize(croupierArea, pathCroupierPattern)
  return (tempPlayerPattern,tempCroupierPattern)

def compare_two_image(image, pattern):
  difference = cv2.subtract(image, pattern)
  black_img = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
  difference2 = black_img.ravel()
  difference2 = difference2.tolist()
  area = len(difference2)
  difference2.sort(reverse=True)
  black = 4 #parameter of black color - mean the same object 0 - mean exactly the same
  while(black >= 0):
    try:
      pozycja = difference2.index(black)
      break
    except:
      #print("Don't found {0}".format(black)) #to debug
      pozycja = -1 #if not found
    black -= 1
  return ((1-(pozycja/area))*100)

def check_if_card_is_on_table(whoPlay):
  if whoPlay == 'Player':
    pattern = playerPattern
    image = take_screenshot(playerArea)
  elif whoPlay == 'Croupier':
    pattern = croupierPattern
    image = take_screenshot(croupierArea)
  else:
    return False
  percentage = compare_two_image(image, pattern)
  print("{whoPlay} percentage: {similarity}".format(similarity = percentage, whoPlay = whoPlay))
  return True if percentage < 45 else False

def save_photo(photo, savePath):
  print('Zapisano plik {}'.format(savePath))
  cv2.imwrite(str(savePath), photo)
  return

def this_is_new_card(i, currentPhoto):
  if i > 1:
    pathToPhoto = dirPlayerCards/'{name}.{extension}'.format(name = str(i-1), extension = 'jpg')
    previousPhoto = cv2.imread(str(pathToPhoto))
    precentageComparision = compare_two_image(currentPhoto, previousPhoto)
    print('Poprzednie karta jest podobna do aktualnej w {}%'.format(precentageComparision))
    if precentageComparision > 80:
      return False
  return True

#MAIN
#save_paterns()
(playerPattern, croupierPattern) = load_paterns()

nameIterator=1
tableEmpty = True

while True:
  if tableEmpty:
    if check_if_card_is_on_table('Player'):
      time.sleep(1.5)
      capturedScreen = take_screenshot(playerArea)
      saveFilePath = dirPlayerCards/'{name}.{extension}'.format(name = str(nameIterator), extension = 'jpg')
      save_photo(capturedScreen, saveFilePath)
      tableEmpty = False
      time.sleep(10)
  else:
    if check_if_card_is_on_table('Croupier'):
      time.sleep(1.5)
      capturedScreen = take_screenshot(croupierArea)
      saveFilePath = dirCroupierCards/'{name}.{extension}'.format(name = str(nameIterator), extension = 'jpg')
      save_photo(capturedScreen, saveFilePath)
      tableEmpty = True
      while check_if_card_is_on_table('Player'):
        print('Wait for take a card')
        time.sleep(5)
      nameIterator += 1
  time.sleep(0.8)