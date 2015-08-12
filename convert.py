import sys
import os
from os.path import dirname
from urllib2 import Request, urlopen
from base64 import b64encode

key = "YOUR_KEY_HERE"
saveFolder = "converted"
queue = []
path = os.path.dirname(os.path.abspath(__file__))

def init():

    for filename in os.listdir(path):
      #if file is png, add to queue
      if getExtention(filename) == ".png":
        queue.append(filename)
        #print "added", filename, "to queue"
        
    #once queue is full, start batch conversion process
    if len(queue) >= 1:
      beginConversions()

def beginConversions():

    counter = 1
    #first, check if converted sub-directory exists
    if not os.path.exists(saveFolder):
      os.makedirs(saveFolder)
      
    #step through each item in queue and convert them
    for file in queue:
      convertFile(file, counter)
      counter +=1
      
    print "All files converted! Have a splendid day!"                  
    
def getExtention(file):
    name, ext = os.path.splitext(file)
    return ext  
    
def convertFile(file, counter):
    print "Converting file ", counter, "of", len(queue)
    request = Request("https://api.tinify.com/shrink", open(file, "rb").read())
    cafile = None
    auth = b64encode(bytes("api:" + key)).decode("ascii")
    request.add_header("Authorization", "Basic %s" % auth)
    
    response = urlopen(request, cafile)
    if response.getcode() == 201:
        dic = dict(response.info().items())
        loc = dic.get('location')
        img = urlopen(loc).read()
        newPath = os.path.join(path, saveFolder, file)
        a = open(newPath, 'w')
        a.write(img)
        a.close()

    else:
        # Something went wrong! You can parse the JSON body for details.
        print("Compression failed", response.getcode())     
       
init() 