import requests
from bs4 import *
import argparse
import os

# add argument parser for passing the target folder for saving the images
parser = argparse.ArgumentParser()
parser.add_argument('--saveto', help='Target directory to save the Images (default: images/', action='store', dest='dirName')
parser.add_argument('--pages', help='No. of pages (default: 40/', action='store', dest='last_pagination')
args = parser.parse_args()

if(args.dirName):
    dirName = str(args.dirName) + '/'
else :
    dirName = 'images/'

if(args.last_pagination):
    last_pagination = int(args.last_pagination) + 1
else :
    last_pagination = 40

if not os.path.exists(dirName):
    os.mkdir(dirName)

headers_std = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
'Content-Type': 'text/html',
}

link = input('Search Query URL: ')
req = requests.get(link)
soup = BeautifulSoup(req.text, 'lxml')

urls = []

for x in range (1, last_pagination):
    urls.append(link + '&page=' + str(x))

k = 1 
pag = 1
for x in urls:
    print('Pagination : ' + str(pag))
    req = requests.get(x,headers=headers_std).text
    soup = BeautifulSoup(req, 'lxml')
    imgs = soup.find_all('img',{'class':'s-image'})
   
    for i in imgs:
        if str(i).find('src') != -1:
            url = i['src']
            name_image_folder = dirName + str(k) + '.jpg'
            image = requests.get(url).content
            
            with open(name_image_folder, 'wb') as handler:
                handler.write(image)
        k += 1
    pag += 1
