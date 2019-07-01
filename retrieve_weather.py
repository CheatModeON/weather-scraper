# Author: 	Achilleas Papakonstantinou (A.S.M. 1490003982013)
# Date:		4/6/2019
# INFO:	

import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import re

html = ''	
resp = requests.get('https://freemeteo.gr/kairos/litoxoro/7-imeres/pinakas/?gid=735399&language=greek&country=greece')
if resp.ok:
    html = resp.text
else:
    print ("Error! {}".format(resp.status_code))
    print (resp.text)
	
soup = BeautifulSoup(html, 'html.parser')

img = Image.new('RGBA', (981, 552), color = (73, 109, 137))
d = ImageDraw.Draw(img)
img.save('weather.png')

img = Image.open("camo_bg.jpg")

img = img.convert("RGBA")

tmp = Image.new('RGBA', img.size, (0,0,0,0))

draw = ImageDraw.Draw(tmp)

counter = 5
for i in range(0, 7):
	draw.rectangle(((counter, 10), (counter+135, 542)), fill=(0,0,0,127))
	counter += 139

# Alpha composite the two images together.
img = Image.alpha_composite(img, tmp)
img = img.convert("RGB") # Remove alpha for saving in jpg format.
img.save('weather.png')

unicode_font_header = ImageFont.truetype("C:\Windows\Fonts\Tahoma.ttf", 24)
unicode_font_big = ImageFont.truetype("C:\Windows\Fonts\Tahoma.ttf", 20)
unicode_font_medium = ImageFont.truetype("C:\Windows\Fonts\Tahoma.ttf", 15)
unicode_font_small = ImageFont.truetype("C:\Windows\Fonts\Arial.ttf", 12)

week = [0,0,0,0,0,0,0]
compass = [0,0,0,0,0,0,0]
d = ImageDraw.Draw(img)
counter = 15
for i in range(0, 7):
	day = (soup.find_all('div', attrs={'class':'day'})[i].findChildren()[0].findChildren()[0].get_text())
	date = (soup.find_all('div', attrs={'class':'day'})[i].findChildren()[0].findChildren()[1].get_text())
	

	max = (soup.find_all('div', attrs={'class':'day'})[i].findChildren()[5].findChildren()[0].get_text())

	min = (soup.find_all('div', attrs={'class':'day'})[i].findChildren()[5].findChildren()[1].get_text())
	
	
	wind = (soup.find_all('div', attrs={'class':'wind'})[i].get_text())
	w = wind.split("°")
	
	info = (soup.find_all('div', attrs={'class':'info'})[i].findChildren()[0].get_text())
	words = info.split()

	extra = (soup.find_all('div', attrs={'class':'extra'})[i].findChildren()[1].get_text())
	
	d.text((counter,20), day, font=unicode_font_header, fill=(255,255,255))
	d.text((counter,60), date + " 2019", font=unicode_font_medium, fill=(255,145,0))
	d.text((counter,200), max, font=unicode_font_big, fill=(255,255,255))
	d.text((counter,240), min, font=unicode_font_small, fill=(185,185,185))
	d.text((counter,460), w[0]+"° / " + w[1], font=unicode_font_medium, fill=(255,255,255))
	compass[i] = round(((int(w[0])*10) / 225))
	if compass[i] == 16: compass[i]=0
	
	# d.text((counter,650), w[1], font=unicode_font_small, fill=(255,255,0))
	d.text((counter,490), "Υετός: ", font=unicode_font_medium, fill=(185,185,185))
	d.text((counter,510), extra + " mm", font=unicode_font_medium, fill=(185,185,185))
	
	count2=0
	# if(len(words)/2==5):
		# count2=0
	# elif(len(words)/2==4):
		# count2=10
	# elif(len(words)/2==3):
		# count2=20
	# elif(len(words)/2==2):
		# count2=30
	# elif(len(words)/2==1):
		# count2=40
		
	for x in range (0, len(words)-1, 2):
		d.text((counter,280+count2),  words[x] + " " + words[x+1], font=unicode_font_medium, fill=(185,185,185))
		count2+=20
		
	if (len(words)%2==1): 
		d.text((counter,280+count2),  words[len(words)-1], font=unicode_font_medium, fill=(185,185,185))
			
	
	# d.text((counter,1200), "Βαθμός κακοκαιρίας: ", font=unicode_font_big, fill=(255,245,0))
	# d.text((counter,1250), icon[0], font=unicode_font_big, fill=(255,245,0))

	# d.line([( counter - 50, 50), ( counter - 50, img.size[1] - 50)], fill=(55,55,55), width=4)
	counter += 140
	
for i in range(0, 14):
	icon = (soup.find_all('div', attrs={'class':'icon'})[i].findChildren()[0])
	if(i%2 == 0):
		icon = re.findall(r"(\d+)",str(icon))
		week[int(i/2)] = str(icon[2])
img.save('weather.png')

counter = 15
background = Image.open("weather.png")
for x in range (0, 7):	
	foreground = Image.open("weather_conditions/"+str(week[x])+".png")
	background.paste(foreground, (counter, 100), foreground)
	counter += 142
background.save('weather.png')

counter = 50
background = Image.open("weather.png")
for x in range (0, 7):	
	foreground = Image.open("compass/"+str(compass[x])+".png")
	background.paste(foreground, (counter, 400), foreground)
	counter += 140
background.save('kairos.jpg')
