#import Libraries

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urReq
from selenium import webdriver
import requests, mysql, pymongo, time, os

#import additional
from src import mysqlquery
from src.youtube_api.videoDetails import ytube_api
import psycopg2

app = Flask(__name__)
CORS(app, support_credentials=True)
# DRIVER_PATH = os.path.join(os.getcwd(),"/static/chromedriver")

#linux driver path
# GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
# CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

#chrome option
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_PATH")

chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

#mysql connection for all
# mcc = mysqlquery.mysqlConnection('localhost','root','Shekhar123#')
# mcc.mydbConnect()

#api_key youtube developer
api_key = "AIzaSyC7dDNkWQpzsfqMgzVcf9AU2vqW4hkgTkg"


#mongodb client
mymongoclient = pymongo.MongoClient('MONGODB_URI')
mydb = mymongoclient.get_database('ineuronproject_db')
details = mydb.video_details



#
# DATABASE_URL = os.environ.get(‘DATABASE_URL’)
# con = psycopg2.connect(DATABASE_URL)
# cur = con.cursor()

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
            chName = request.form.get('searchtext')
            searchText = chName.replace(" ","+")
            url = ("https://www.youtube.com/results?search_query={}".format(searchText))
            driver.get(url)
            driver.execute_script("window.scrollTo(0,2000);")
            time.sleep(1)
            content = driver.page_source.encode('utf-8').strip()
            soup = bs(content,'html.parser')
            findChannelSection = soup.find_all('div',id="content-section")
            for tag in findChannelSection:
                channelLink = tag.div.a['href']
            channelEmbeddedURL = "https://www.youtube.com{}/videos?view=0&sort=dd&flow=grid".format(channelLink)
            driver.get(channelEmbeddedURL)
            driver.execute_script("window.scrollTo(0,2000);")
            time.sleep(1)
            # dbname = mcc.createdatabase("ineuronpythonprojectdb")
            # tablename = mcc.createtablewithschema('(id int,videotitle varchar(255),totalviews varchar(255),videourl varchar(255),thumbnail varchar(255))',tablename='youtuberstable')
            findChannelPage = driver.page_source.encode('utf-8').strip()
            pageSoup = bs(findChannelPage,'lxml')
            titles = pageSoup.findAll('a',id="video-title")
            views = pageSoup.findAll('span',class_="style-scope ytd-grid-video-renderer")
            thumbnail = pageSoup.findAll('img',class_="style-scope yt-img-shadow")
            thumb_list = []
            for thumb in thumbnail[6:]:
                thumb_list.append(thumb.get('src'))
            channel_details = []
            i, j = 0, 0
            if chName == "krish naik" or chName == "Krish Naik":
                for title in titles[:50]:
                    d = {"channelName":chName,"videoTitle":title.text,"totalViews":views[i].text,"videoURL":"https://www.youtube.com"+title.get('href'),"thumbnail":thumb_list[j+1]}
                    # dtable = "({},'{}','{}','https://www.youtube.com{}','{}')".format(j,title.text,views[i].text,title.get('href'),thumb_list[j])
                    # insertintotable = mcc.insertintotable(tablename='youtuberstable',values = dtable)
                    details.insert_one(d)
                    channel_details.append(d)
                    i +=2
                    j +=1
                # print(len(channel_details))
                return render_template("results.html",channel_details = channel_details)
            
            elif len(titles) > 50:
                for title in titles[:50]:
                    d = {"channelName":chName,"videoTitle":title.text,"totalViews":views[i].text,"videoURL":"https://www.youtube.com"+title.get('href'),"thumbnail":thumb_list[j]}
                    dtable = "({},'{}','{}','https://www.youtube.com{}','{}')".format(j,title.text,views[i].text,title.get('href'),thumb_list[j])
                    insertintotable = mcc.insertintotable(tablename='youtuberstable',values = dtable)
                    details.insert_one(d)
                    channel_details.append(d)
                    i +=2
                    j +=1
                # print(len(channel_details))
                return render_template("results.html",channel_details = channel_details)
            else:
                for title in titles:
                    d = {"channelName":chName,"videoTitle":title.text,"totalViews":views[i].text,"videoURL":"https://www.youtube.com"+title.get('href'),"thumbnail":thumb_list[j]}
                    channel_details.append(d)
                    # dtable = "({},'{}','{}','https://www.youtube.com{}','{}')".format(j,title.text,views[i].text,title.get('href'),thumb_list[j])
                    # insertintotable = mcc.insertintotable(tablename='youtuberstable',values=dtable)
                    details.insert_one(d)
                    # print(insertintotable)
                    i +=2
                    j +=1
                # print(len(channel_details))
                return render_template("results.html",channel_details = channel_details)
        except Exception as exp:
            print('Exception Called', exp)
            return "something went wrong"
    else:
        return render_template("home.html")

@app.route("/aboutme", methods =['GET'])
@cross_origin(support_credentials = True)
def aboutMe():
    return render_template("portfolio.html")

@app.route("/getvideodetails",methods = ['GET','POST'])
@cross_origin(supports_credentials=True)
def videoCommentsDetails():
    if request.method == 'GET':
        try:
            channel = request.args.get('chname')
            vURL = request.args.get('url')
            title = request.args.get('videotitle')
            yobj = ytube_api(link=vURL,apikey=api_key)
            datas = yobj.extractfromresponses()
            context = {'channel':channel,'title':title,'datas':datas}
            return render_template("vdetailing_page.html",datas=datas,title=title,channel=channel)
        except:
            return "something went wrong"
