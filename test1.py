#import Libraries

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urReq
import requests
import mysql, pymongo

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/",methods = ['GET'])
@cross_origin(support_credentials = True)
def home():
    """
    This is home function for render homepage
    Return: render ./templates/home.html 
    """
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug = True)