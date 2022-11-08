# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import glob
import os
import pathlib
import shutil

import cv2
import urllib3
import wget
from bs4 import BeautifulSoup
import pandas as pd
import requests


def sortTuple(tup):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    tup.sort(key=lambda tup: tup[1], reverse=True)
    return tup


outDir = os.path.join(os.getcwd(), 'SelectedImages')

def scrapImagesAndSelect(pid, url, count):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features="html.parser")
    tmpDir = os.path.join(os.getcwd(), 'images')

    if os.path.isdir(tmpDir):
        shutil.rmtree(tmpDir)

    pathlib.Path(tmpDir).mkdir(parents=True, exist_ok=True)

    imageSizes = dict()
    for img in soup.findAll('img'):
        imgPath = img.get('src')
        if not imgPath.startswith('https') and not imgPath.startswith('http'):
            imgPath = 'https:' + imgPath
        if imgPath == 'https:':
            continue
        response = requests.get(imgPath)
        imageSizes[imgPath] = int(response.headers['Content-Length'])
        #filename = wget.download(imgPath, out=tmpDir)
        #print(os.path.getsize(filename), response.headers['Content-Length'])
        #img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        #print(filename, img.shape)

    print(pid, url)
    #print(imageSizes)
    listOfImages = [(k, v) for k, v in imageSizes.items()]
    sortTuple(listOfImages)
    for i in range(count):
        filename = wget.download(listOfImages[i][0], out=tmpDir)
        shutil.move(filename, os.path.join(outDir, pid + '_' + str(i) + pathlib.Path(filename).suffix))
# Get list of files in a directory
    # listOfFiles = filter(os.path.isfile,
    #                      glob.glob(tmpDir + '/' + '*'))
    # # Find the file with max size from the list of files
    # maxFile = max(listOfFiles, default=0, key=lambda x: os.stat(x).st_size)
    # print('Max File: ', maxFile)
    # print('Max File size in bytes: ', os.stat(maxFile).st_size)
    # shutil.move(maxFile, os.path.join(outDir, pid + pathlib.Path(maxFile).suffix))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def readCsv(filePath):
    df = pd.read_csv(filePath, header=0, encoding = "ISO-8859-1",
    usecols = ["pid", "ExternalLink"])
    return df


# Program starts here #
if os.path.isdir(outDir):
    shutil.rmtree(outDir)
pathlib.Path(outDir).mkdir(parents=True, exist_ok=True)

df = readCsv(os.path.join(pathlib.Path().resolve(), 'products.csv'))
for index, row in df.iterrows():
    scrapImagesAndSelect(df.pid[index], df.ExternalLink[index], 2);