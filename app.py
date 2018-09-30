# Dependencies
from flask import Flask, render_template, jsonify, redirect
import pymongo
from pymongo import MongoClient
import scrape_mars_test

# create instance of Flask app
app = Flask(__name__)

# use flask_pymongo to set up mongo connection

# client = MongoClient("mongodb://localhost:27017")

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.nasa_news_mars_db


collection = db.nasa_news_mars

@app.route("/")
def index():
    mars = db.nasa_news_mars.find_one()
    return render_template("index.html", mars=mars)


@app.route('/scrape')
def scrape():
    mars = db.nasa_news_mars
    data = scrape_mars_test.scrape()

    print(data) 
    mars.update({}, data, upsert=True)

    return redirect("http://localhost:5000/", code=302)
   
if __name__ == "__main__":
    app.run(debug=True)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True