from flask import Flask, render_template, request
import sys
import logging
import threading
from collectData import *
from pipeline import *
from selenium import webdriver

app = Flask(__name__)

@app.route('/args')
def render():
    if 'kw' in request.args:
        driver_path = os.getcwd()
        keywords = request.args.get('kw')
        keywords = keywords.replace('.',' ')
        links = list()
        links = get_links(keywords,2,driver_path)
        pipeline_run(links) 
        return keywords
    else:
        return "No input specified"

if __name__=='__main__':
    app.run(debug=True)
#http://localhost:5000/args?kw=nba.houston.rockets
