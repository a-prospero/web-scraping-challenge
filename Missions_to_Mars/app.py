from flask import Flask, render_template, redirect
import mission_to_mars
from pymongo import MongoClient

mongo = MongoClient('mongodb://localhost:27017/mars_db')
app = Flask (__name__)

@app.route('/')
def index_page():
    mars_collect = mongo.db.mars_collect.find_one()
    return render_template('index.html', mars=mars_collect)

@app.route('/scrape')
def scraping_info():
    mars_collect = mongo.db.mars_collect
    scrape_data = mission_to_mars.scrape()
    mars_collect.update({}, scrape_data, upsert=True)
    return redirect('/', code=302)
app.run(debug=True)


