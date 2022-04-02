# imports
import math
import requests
import json
import time
from requests.auth import HTTPBasicAuth
from PIL import Image
import numpy as np
from tqdm import tqdm
import itertools
from webdriver_manager.chrome import ChromeDriverManager
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class placeBotV2:
	def __init__(self,image):
		self.colors = {
				"#be0039",
				"#FF4500",
				"#FFA800",
				"#FFD635",
				"#00A368",
				"#00cc78",
				"#7EED56",
				"#00756f",
				"#009eaa",
				"#2450A4",
				"#3690EA",
				"#51E9F4",
				"#493ac1",
				"#6a5cff",
				"#811E9F",
				"#B44AC0",
				"#ff3881",
				"#FF99AA",
				"#6d482f",
				"#9C6926",
				"#000000",
				"#898D90",
				"#D4D7D9",
				"#FFFFFF",
		}
		self.accFile = "accs.json"
		self.x = 1323
		self.y = 362
		self.art = str(image)
		self.accountcycle = itertools.cycle(self.loadAccs())
		self.proxies = itertools.cycle(self.loadProxies())
		self.loadImage()
		self.convertImage()
		self.bot()

	def getColorTabs(self,color):
		# color = ((str(color).replace("[", "").replace("]","").split()))
		# color = [int(i) for i in color]
		color = self.rgbToHex(tuple([int(i) for i in (str(color).replace("[", "").replace("]","").split())]))
		idDict = {
			"#be0039":"1",
			"#FF4500":"2",
			"#FFA800":"3",
			"#FFD635":"4",
			"#00A368":"5",
			"#00cc78":"6",
			"#7EED56":"7",
			"#00756f":"8",
			"#009eaa":"9",
			"#2450A4":"10",
			"#3690EA":"11",
			"#51E9F4":"12",
			"#493ac1":"13",
			"#6a5cff":"14",
			"#811E9F":"15",
			"#B44AC0":"16",
			"#ff3881":"17",
			"#FF99AA":"18",
			"#6d482f":"19",
			"#9C6926":"20",
			"#000000":"21", 
			"#898D90":"22",
			"#D4D7D9":"23",
			"#FFFFFF":"24"
		}
		return idDict[color]
			
		
	def bot(self):
		for x in tqdm(range(self.image.shape[0])):
			for y in range(self.image.shape[1]):
				x = x + self.x
				y = y + self.y
				account = next(self.accountcycle)
				proxy = next(self.proxies)
				#Setting up the browser
				chrome_options = Options()
				#chrome_options.add_argument("--headless")
				chrome_options.add_argument("log-level=3")
				chrome_options.add_argument("--deny-permission-prompts")
				chrome_options.add_argument('--proxy-server=%s' % proxy)
				driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
				#LOGIN
				driver.get("https://www.reddit.com/login")
				driver.find_element_by_name("username").send_keys(account["username"])
				driver.find_element_by_name("password").send_keys(account["password"])
				redditloginbutton = WebDriverWait(driver, 10).until(
				EC.visibility_of_element_located((By.XPATH, '/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button')))
				redditloginbutton.click()
				#open coordinate
				time.sleep(5)
				driver.get(f"https://www.reddit.com/r/place/?cx={x}&cy={y}&px=5")
				time.sleep(5)
				driver.get(f"https://www.reddit.com/r/place/?cx={x}&cy={y}&px=5")
				#maximize canvas
				driver.find_element(By.CSS_SELECTOR, ".moeaZEzC0AbAvmDwN22Ma").click()
				try:
					driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/section/div/section/section/form[1]/button").click()
				except NoSuchElementException:
					print("No Cookie Thing")
				time.sleep(5)
				actions = ActionChains(driver) 
				actions.send_keys(Keys.TAB * 20)
				actions.send_keys(Keys.ENTER)
				actions.perform()
				tabs = int(self.getColorTabs(self.image[x - self.x][y - self.y]))
				time.sleep(5)
				actions = ActionChains(driver) 
				actions.send_keys(Keys.TAB * tabs)
				actions.send_keys(Keys.ENTER)
				actions.perform()
				tabs = 27 - tabs
				time.sleep(5)
				actions = ActionChains(driver) 
				actions.send_keys(Keys.TAB * tabs)
				actions.send_keys(Keys.ENTER)
				actions.perform()
				time.sleep(5)
				driver.quit()



	def loadAccs(self):
		try:
			with open(self.accFile,"r") as accountsFile:
				return json.load(accountsFile)
		except json.decoder.JSONDecodeError:
			print("yo there is a error while loading accounts ")

	def loadProxies(self):
		try:
			with open("proxies.json","r") as proxiesFile:
				return json.load(proxiesFile)
		except json.decoder.JSONDecodeError:
			print("yo there is a error while loading proxies")

	def hexToRgb(self, hex):
		return tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

	def rgbToHex(self, rgb):
		return ('#%02x%02x%02x' % rgb).upper()

	def closestColor(self, color, colorPallete):
		color = (str(color).replace("[", "").replace("]","").split())
		r = int(color[0].strip()) 
		g = int(color[1].strip()) 
		b = int(color[2].strip()) 
		colorDiffs = []
		for color in colorPallete:
			color = self.hexToRgb(color)
			palleteR = int(color[0]) 
			palleteG = int(color[1]) 
			palleteB = int(color[2]) 
			colorDiff = math.sqrt((r - palleteR) ** 2 + (g - palleteG) ** 2 + (b - palleteB) ** 2)
			colorDiffs.append((colorDiff, color))
		return min(colorDiffs)[1]

	def loadImage(self):
		self.image = np.array(Image.open(self.art).convert("RGB"))

	def getPixel(x,y):
		return self.image[x,y]

	def convertImage(self):
		for x in tqdm(range(self.image.shape[0])):
			for y in range(self.image.shape[1]):
				self.image[x,y] = self.closestColor(self.image[x,y], self.colors)


if __name__ == '__main__':
	Bot = placeBotV2("pp-rplace.png")
	Bot.convertImage()
	time.sleep(1)
	print(Bot.image)
