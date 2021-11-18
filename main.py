import sys
from os.path import exists

import pytesseract
from pdf2image import convert_from_path
import cv2
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import pyautogui

from termcolor import colored, cprint
import colorama


path = 'tmp.png'
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
flag_show_gui = False
flag_screenshot = False
flag_timer = False
flag_show_text = False

def main():
  colorama.init()
  path = handleInput()
  if(path):
    showTitle()

    """
    # screenshot
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(path)
    """

    txt = pytesseract.image_to_string(path)
    file = open("output.txt","w")
    file.write(txt)
    file.close()

    blob = TextBlob(txt, analyzer=NaiveBayesAnalyzer())
    showResults(txt, blob)

def handleInput():
  if(len(sys.argv)==1):
    cprint("Error - Try : python mulder.py -i path/to/file.png", 'red')
    quit()
  else:
    if(len(sys.argv)%2!=1):
      cprint("Error - No value given", 'red')
      quit()
    else: # input style : -o name
      name = "tmp" # TODO : if name is tmp then delete file after
      for i in range(1, len(sys.argv), 2):
        option_i = sys.argv[i]
        argument_i = sys.argv[i+1]
        print(option_i, argument_i)
        # option screen shot
        # option screen shot a repetition
        # option no graphics
        # option créer
        if(option_i == "-i"):
          name = argument_i
          if(exists(name)):
            return name
  return None

def showTitle():
  cprint("  ___  ___      _     _                  ___", 'green')
  cprint("  |  \/  |     | |   | |             ___/   \___", 'green')
  cprint("  | .  . |_   _| | __| | ___ _ __   /   '---'   \\", 'green')
  cprint("  | |\/| | | | | |/ _` |/ _ \ '__|  '--_______--'", 'green')
  cprint("  | |  | | |_| | | (_| |  __/ |          / \\", 'green')
  cprint("  \_|  |_/\__,_|_|\__,_|\___|_|         /   \\", 'green')
  cprint('  The screen reader.', 'yellow')

def showResults(txt, blob):
  len_txt = len(txt)
  nb_word = len(blob.words)
  nb_sentence = len(blob.sentences)

  print(" =================================================")
  print(" Statistics : ")
  txt = "  - Numbers char. :" + str(len_txt)
  cprint(txt, 'green')
  print("  - Numbers words :", nb_word )
  print("  - Numbers sentences :", nb_sentence)
  print(" =================================================")


def showImage():
  img = cv2.imread(path)
  h, w, _ = img.shape # assumes color image
  boxes = pytesseract.image_to_boxes(img) # also include any config options you use
  # draw the bounding boxes on the image
  for b in boxes.splitlines():
      b = b.split(' ')
      img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
  # show annotated image and wait for keypress
  cv2.imshow(path, img)
  cv2.waitKey(0)

if __name__ == '__main__':
  main()
