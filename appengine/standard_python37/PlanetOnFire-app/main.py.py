import os
from flask import Flask, render_template, redirect, jsonify, json, abort, url_for
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask_pymongo import PyMongo
#import scrapePd
import pandas as pd
from sqlalchemy.ext.automap import automap_base
import psycopg2
import psycopg2.extras
import json as simplejsonpythi
import datetime as dt
from bson import json_util
# import Twitter_LocationSearchTweets
#from Twitter_LocationSearchTweets import scraped_time




# Create an instance of Flask
application = app = Flask(__name__)

# from bs4 import BeautifulSoup
# from splinter import Browser
# import requests
# import pandas as pd
# #from selenium import webdriver
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy_utils import create_database, database_exists, drop_database
# from sqlalchemy import Column, Integer, String, Float
# import datetime as dt  
# import pandas as pd


# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)
# #browser = Browser('chrome', headless=True)

# todaysDate = str(dt.date.today())
# Base = declarative_base()
# connection_string = "postgres:Yatish28$@localhost:5432/planetOnFire_db"
# engine = create_engine(f'postgresql+psycopg2://{connection_string}')

# # connection_string = 'root:12345678@mydb.cpzsszr6n1nw.us-east-2.rds.amazonaws.com:5432/planetOnFire_db'
# # engine = create_engine(f'postgresql+psycopg2://{connection_string}')

# #connection_string = "prmpgujo:cSBQxTa1lkKY0hsb4c1OGgAZOqIX6bc4@drona.db.elephantsql.com:5432/prmpgujo"
# #engine = create_engine(f'postgresql+psycopg2:// {connection_string}')


# if database_exists(engine.url):
#     # Delete PostgreSQL database 
#     #drop_database(engine.url)
#     # Create empty PostgreSQL database
#     #create_database(engine.url)
#     print ("db exists")
# # Otherwise
# else:
#     # Create empty PostgreSQL database
#     create_database(engine.url)

# # try:
# #     pd.read_sql('CREATE TABLE IF NOT EXISTS my_new_df (first_name varchar (255))',con = engine)
# # #pd.read_sql('CREATE TABLE IF NOT EXISTS my_df ( first_name varchar(255), city_name varchar(255),age int)',con=engine)
# # except:
# #     print("error gone")
# # print(pd.read_sql_query('select * from my_df', con=engine).head())

# url = "https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/active-fire-data#ed-firms-archive"


# def scrape_data():

#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     #print(soup.prettify())

#     #grab third table (TXT data)
#     table = soup.find_all('table')[2]
#     #print(table)

#     #grab link for 7 days data in the second column (with MODIS 1 km data)
#     link = table.find_all('a', text='7d')[0]['href']
#     #print(link)
    
#     df = pd.read_csv(link)
    
#     cleaned_df = df.drop(columns=["scan","track","acq_time","satellite","confidence","version","frp","daynight"])
    
#     cleaned_df.to_sql('cleaned_df', con=engine, if_exists='replace', index=False)
    
#     #df = pd.read_csv(link)
#     #print(df.head())
#     print("worked")

# Base.metadata.create_all(engine)
# tables = engine.table_names()
# print(tables)

# if ("cleaned_df" in tables):
#     date_df = pd.read_sql_query('select acq_date from cleaned_df', con=engine)
#     date_check = date_df["acq_date"].iloc[-1]

#     if ((date_check)!=todaysDate):

#         scrape_data()

#         print ("scraped")

#     else:
#         print("table exists")
# else:
    
#     scrape_data()
#     print("data upto date")


connection_string = 'postgres:Yatish28$@localhost:5432/planetOnFire_db'
engine = create_engine(f'postgresql+psycopg2://{connection_string}')

# connection_string = 'root:12345678@mydb.cpzsszr6n1nw.us-east-2.rds.amazonaws.com:5432/planetOnFire_db'
# engine = create_engine(f'postgresql+psycopg2://{connection_string}')


mydata = pd.read_sql_query('select * from cleaned_df', con=engine)
myJsonData = mydata.to_json(orient='records')

print("working")

@app.route("/")
def home():    
   return render_template("index.html") 

@app.route("/news")
def news():    
   return render_template("news.html") 


@app.route("/stats")
def stats():    
   return render_template("stats.html") 

@app.route("/developers")
def developers():    
   return render_template("developers.html")

@app.route("/api")
def myData():

   return (myJsonData)

@app.route("/refresh")
def refreshData():
   print("abc")

   scrape_data()

   return render_template("index.html")

@app.route("/api/australia/2015")
def historic_data_au_2015():
   import Historic_data_au
   return Historic_data_au.mongoData_2015()

@app.route("/api/australia/2016")
def historic_data_au_2016():
   import Historic_data_au
   return Historic_data_au.mongoData_2016()

@app.route("/api/australia/2017")
def historic_data_au_2017():
   import Historic_data_au
   return Historic_data_au.mongoData_2017()

@app.route("/api/australia/2018")
def historic_data_au_2018():
   import Historic_data_au
   return Historic_data_au.mongoData_2018()

@app.route("/api/australia/2019")
def historic_data_au_2019():
   import Historic_data_au
   return Historic_data_au.mongoData_2019()


@app.route("/api3")
def myTwitterData():
   #mongo = PyMongo(app, uri="mongodb://localhost:27017/TwitterData")
   mongo = PyMongo(app, uri="mongodb+srv://Yatish:1234@cluster0-4l19n.mongodb.net/TwitterData?retryWrites=true&w=majority")
   current_time = dt.datetime.now()
   try:
      import Twitter_LocationSearchTweets
      from Twitter_LocationSearchTweets import scraped_time

      mongoTwitterData =[]
      mongoDict = {} 
      mongoTwitter = (mongo.db.TwitterMyData)   
      
   
      if (current_time - Twitter_LocationSearchTweets.scraped_time).seconds/60 > 20:
         try:
            Twitter_LocationSearchTweets.scrapeTwitter()
            print("twitter scraped")
         except:
            print ("all good")

      else:
         print("new scrape not required")
         #return twitterData
   except:
      print("no more delays")
   mongoTwitterData =[]
   mongoDict = {} 
   mongoTwitter = (mongo.db.TwitterMyData)   
   for x in mongoTwitter.find({}):
      x.pop('_id')
      mongoTwitterData.append(x)
   mongoDict["url"] = mongoTwitterData
   return mongoDict

print ("Data loading complate...")
if __name__ == "__main__":
    app.run(debug=True)