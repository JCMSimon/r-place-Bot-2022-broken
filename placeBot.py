import pathlib
from PIL import Image
import json
import webdriver_manager
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import itertools
import time

current_path = pathlib.Path(__file__).parent.absolute()

#-load image and get colors (seperate by colors (duchess pls make uwu?))
#duches pls uwu

#multithread that biatch to have 2 or 3 placing at the same time while its running in single mode

class placeBot:
	def __init__(self):
		self.accFile = pathlib.Path(f"{current_path}/accs.json")
		self.x = 0
		self.y = 0
		self.accounts = self.loadAccs()
		self.colorsRGB = {
			"black" : "[0, 0, 0, 255]" ,
			"purple" : "[180, 74, 192, 255]" ,
			"orange" : "[255, 69, 0, 255]" ,
			"dark_yellow" : "[255, 168, 0, 255]" ,
			"light_yellow" : "[255, 214, 53, 255]", 
			"turquoise" : "[0, 163, 104, 255]" ,
			"light_blue" : "[81, 233, 244, 255]" ,
			"white" : "[255, 255, 255, 255]"
		}



		# colors are very complicated to locate with selenium
		# use special selectors to find the colors
		pixel_list = self.loadimageJanky()
		#self.bot(pixel_list)

	def loadimage(self):
		#open the image with numpy
		self.image = np.array(Image.open(f"{current_path}/pp-rplace.png").convert("RGB"))
		for color,code in self.colorsRGB.items():
			indices = np.where(np.all(self.image == code),axis=-1) #duchess pls halp
			color = list(zip(indices[1], indices[0]))
			# add all colors into a list
			return pixel_list

		# Janky Method	 
	def loadimageJanky(self): #you are not even calling this method dummy
		#convert image to list of lists
		#for each pixel in the list, check if its in the list of colors
		#if it is, add it to the list of pixels to place
		#if not, ignore it
		image = Image.open(f"{current_path}/pp-rplace.png").convert("RGB")
		imageNP = np.asarray(self.image)
		width, height = image.size
		
		mergedlist = []
		imagelist = [get_ID_from_rgb(y) for x in imageNP for y in x]

		# print(imagelist)
		Image = list(self.chunks(imagelist, width))
		for idx, x in enumerate(Image):
			for idy, colour in enumerate(x):
				mergedlist.append([idx+self.x, idy+self.y, colour])
		return mergedlist

	def get_ID_from_rgb(rgb):
		for x in ENUM:
			if (rgb[0], rgb[1], rgb[2], rgb[3]) == x.rgb:
				return x.index
		return -1

	def bot(self, pixel_list):
		self.colorsElement = {
			"black" : driver.findElement(By.xpath("//*[@data-color='27']")),
			"purple" : driver.findElement(By.xpath("//*[@data-color='19']")),
			"orange" : driver.findElement(By.xpath("//*[@data-color='2']")),
			"dark_yellow" : driver.findElement(By.xpath("//*[@data-color='3']")),
			"light_yellow" : driver.findElement(By.xpath("//*[@data-color='4']")),
			"turquoise" : driver.findElement(By.xpath("//*[@data-color='6']")),
			"light_blue" : driver.findElement(By.xpath("//*[@data-color='14']")),
			"white" : driver.findElement(By.xpath("//*[@data-color='31']")),
		}
		accountcycle = itertools.cycle(self.accounts)
		submit = "selenium elemnt"
		while len(pixel_list) > 0:
			x, y, color = pixel_list.pop() #color should be the html thing to click
			account = next(accountcycle)
			#lets setup selenium
			chrome_options = Options()
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("log-level=3")
			driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
			driver.get("https://www.reddit.com/login")
			redditusernamefield = driver.find_element_by_name("username")
			redditpasswordfield = driver.find_element_by_name("password")
			redditloginbutton = WebDriverWait(driver, 10).until(
			EC.visibility_of_element_located((By.XPATH, '/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button')))
			redditusernamefield.send_keys(account["username"])
			redditpasswordfield.send_keys(account["password"])
			redditloginbutton.click()
			driver.get(f"https://www.reddit.com/r/place/?cx={x}&cy={y}&px=5")
			#wait a bit 
			time.sleep(2)
			try:
				color.click() #color from list #what 
				time.sleep(0.5)
				submit.click()
			except "elemnt not found thing": #here 
				print("too early to place, trying next account")
				pass	
			time.sleep(2)
			driver.delete_all_cookies()


			#@almos dont you like know how to delete cookiees instead of closing and reopening?

	#keep this
	def loadAccs(self):
		try:
			with open(self.accFile,"r") as accountsFile:
				return json.load(accountsFile)
		except json.decoder.JSONDecodeError:
			print("yo there is a error while loading")

if __name__ == "__main__":
	Bot = placeBot()