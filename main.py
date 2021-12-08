import sys
import time

import pytesseract
import cv2
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import pyautogui
from collections import Counter

from termcolor import colored, cprint
import colorama

# TODO : transform image to have a better text extraction (treshold)

path = 'tmp.png'
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
flag_show_gui = True
flag_screenshot = False
flag_timer = False
flag_show_text = False
flag_show_image = False
flag_word = False
flag_sentence = False
current_iteration = 0

def main():
  global current_iteration
  colorama.init()
  path, output, repeat, nbwords = handleInput()

  if(flag_screenshot):
    path = "tmp.png"
    takeScreenshot(path)

  if(path):
    if(flag_show_gui):
      showTitle()

    if(flag_timer):
      if(flag_show_gui):
        print(" =================================================")
      start = time.time()
      now = time.time()
      while(now - start < repeat):
        if(int(now-start) % 1 == 0):
          path = "tmp" + str(current_iteration) + ".png"
          takeScreenshot(path)

          if(flag_show_gui):
            print(colored(" New screenshot :",'green'), current_iteration, " - ", now-start, "sec.")

          now = time.time()
          current_iteration += 1
          analyzeTxt(path, output, nbwords)
    else:
      analyzeTxt(path, output, nbwords)


def takeScreenshot(path):
  myScreenshot = pyautogui.screenshot()
  myScreenshot.save(path)


def analyzeTxt(path, output, nbwords):
  global current_iteration, flag_timer
  txt = pytesseract.image_to_string(path)
  if(output):
    out = output
  else:
    if(flag_timer):
      out = "output" + str(current_iteration) + ".txt"
    else:
      out = "output.txt"
  file = open(out,"w")
  file.write(txt)
  file.close()
  blob = TextBlob(txt, analyzer=NaiveBayesAnalyzer())
  if(flag_show_gui):
    if(flag_show_text):
      showRawTxt(txt)
    showResults(txt, blob, nbwords)
    if(flag_show_image):
      showImage()


def handleInput():
  global flag_show_gui, flag_screenshot, flag_show_image, flag_show_text, flag_timer, flag_word, flag_sentence
  if(len(sys.argv)==1):
    cprint(" Error - Try : python mulder.py -i path/to/file.png", 'red')
    quit()
  else:
    if(len(sys.argv)%2!=1):
      cprint(" Error - No value given", 'red')
      showHelp()
      quit()
    else: # input style : -o name
      name = None # TODO : if name is tmp then delete file after
      output = None
      repeat = None
      nbwords = None
      for i in range(1, len(sys.argv), 2):
        option_i = sys.argv[i]
        argument_i = sys.argv[i+1]
        # option screen shot a repetition
        if(option_i == "-i"): # input
          name = argument_i
        if(option_i == "-o"): # output
          output = argument_i
        if(option_i == "-s"): # screenshot
          if(argument_i == "y"):
            flag_screenshot = True
        if(option_i == "-t"): # timer
          flag_screenshot = True
          flag_timer = True
          try:
            repeat = int(argument_i)
          except ValueError:
            cprint(" Error - Wrong option value", 'red')
            showHelp()
            quit()
        if(option_i == "-sen"): # most common word
          if(argument_i == "y"):
            flag_sentence = True
        if(option_i == "-w"): # most common word
          flag_word = True
          nbwords = int(argument_i)
        if(option_i == "-img"): # show image
          if(argument_i == "y"):
            flag_show_image = True
        if(option_i == "-txt"): # show txt
          if(argument_i == "y"):
            flag_show_text = True
        if(option_i == "-g"): # gui
          if(argument_i == "n"):
            flag_show_gui = False

        # CHECK IF A WORD IS IN A PICTURE
  return name, output, repeat, nbwords


def showHelp():
  print(" -option arg : Description")
  print(" =================================================")
  print(" -i path    : Specify input file path")
  print(" -o path    : Specify output file path")
  print(" -g 'y/n'   : Show GUI or not")
  print(" -txt 'y/n' : Show the raw text on the input image")
  print(" -sen 'y/n' : Show the sentences on the input image")
  print(" -img 'y/n' : Show the analyzed input image")
  print(" -s 'y/n'   : Take screenshot as input")
  print(" -t x       : Take screenshot for x seconds")
  print(" -w x       : Show the x most common words")
  print(" =================================================")


def showTitle():
  cprint("  ___  ___      _     _                  ___", 'green')
  cprint("  |  \/  |     | |   | |             ___/   \___", 'green')
  cprint("  | .  . |_   _| | __| | ___ _ __   /   '---'   \\", 'green')
  cprint("  | |\/| | | | | |/ _` |/ _ \ '__|  '--_______--'", 'green')
  cprint("  | |  | | |_| | | (_| |  __/ |          / \\", 'green')
  cprint("  \_|  |_/\__,_|_|\__,_|\___|_|         /   \\", 'green')
  cprint('  The screen reader.', 'yellow')


def showRawTxt(txt):
  print(" =================================================")
  print(txt)


# Make function to get Statistics
def showResults(txt, blob, nbwords):
  len_txt = len(txt)
  nb_word = len(blob.words)
  nb_sentence = len(blob.sentences)
  split_it = txt.split()
  counter = Counter(split_it)
  if(flag_word):
    most_commo = counter.most_common(nbwords)
  print(" =================================================")
  print(" Statistics : ")
  print("  - Numbers char. : ", colored(str(len_txt), 'yellow'))
  print("  - Numbers words :", colored(str(nb_word), 'yellow'))
  print("  - Numbers sentences :", colored(str(nb_sentence), 'yellow'))
  print(" =================================================")
  if(flag_word):
      print(" Most common words : ")
      for key, val in most_commo:
          print("  - ", key, ":", colored(str(val), 'yellow'))
      print(" =================================================")
  if(flag_sentence):
      print(" Sentences : ")
      for elem in blob.sentences:
          print("  -", elem)
      print(" =================================================")

def showImage():
  img = cv2.imread(path)
  h, w, _ = img.shape # assumes color image
  boxes = pytesseract.image_to_boxes(img) # also include any config options you use
  for b in boxes.splitlines():
      b = b.split(' ')
      img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
  cv2.imshow(path, img)
  cv2.waitKey(0)


if __name__ == '__main__':
  main()
