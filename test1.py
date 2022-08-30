#import Libraries

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urReq
from selenium import webdriver
import requests
import mysql, pymongo

app = Flask(__name__)
CORS(app, support_credentials=True)
DRIVER_PATH = r'chromedriver.exe'


@app.route("/",methods = ['GET'])
@cross_origin(support_credentials = True)
def home():
    """
    This is home function for render homepage
    Return: render ./templates/home.html 
    """
    return render_template("home.html")


@app.route("/search", methods =['GET','POST'])
@cross_origin(support_credentials = True)
def searchKeyString():
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    if request.method == 'POST':
        try:
            driver = webdriver.Chrome()
            searchText = request.form.get('searchtext').replace(" ","+")
            url = ("https://www.youtube.com/results?search_query={}".format(searchText))
            driver.get(url)
            content = driver.page_source.encode('utf-8').strip()
            soup = bs(content,'html.parser')
            findChannelSection = soup.find_all('div',id="content-section")
            for tag in findChannelSection:
                channelLink = tag.div.a['href']
            channelEmbeddedURL = "https://www.youtube.com{}/videos?view=0&sort=dd&flow=grid".format(channelLink)
            driver.get(channelEmbeddedURL)
            findChannelPage = driver.page_source.encode('utf-8').strip()
            pageSoup = bs(findChannelPage,'lxml')
            titles = pageSoup.findAll('a',id="video-title")
            views = pageSoup.findAll('span',class_="style-scope ytd-grid-video-renderer")
            channel_details = []
            i, j = 0, 0
            for title in titles:
                d = {"videoTitle":title.text,"totalViews":views[i].text,"videoURL":"https://www.youtube.com"+title.get('href')}
                # print(d)
                channel_details.append(d)
                i +=2
                j +=1
            # print(len(channel_details))
            return render_template("results.html",channel_details = channel_details)
        except Exception as exp:
            print('Exception Called', exp)
            return "something went wrong"
    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug = True)
# searchKeyString("krishnaik")