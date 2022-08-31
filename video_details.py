#import libraries
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urReq
import requests, mysql, pymongo, time, os

#Variables
DRIVERPATH = r'chromedriver.exe'

#function declaration for video details
def videodetails(videourl: str):
    driver = webdriver.Chrome()
    driver.get(videourl)