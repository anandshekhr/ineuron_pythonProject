#import Libraries

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urReq
from selenium import webdriver
import requests
import mysql, pymongo


DRIVER_PATH = r'chromedriver.exe'


def searchKeyString(searchText: str):
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    # try:
    searchText = searchText.replace(" ","+")
    driver = webdriver.Chrome()
    url = ("https://www.youtube.com/results?search_query={}".format(searchText))
    driver.get(url)
    content = driver.page_source.encode('utf-8').strip()
    soup = bs(content,'html.parser')
    findChannelSection = soup.find_all('div',id="content-section")
    # print(len(findChannelSection))
    box = findChannelSection[0]
    print(box)
    # print(soup.prettify())
    


searchKeyString('krish naik')
