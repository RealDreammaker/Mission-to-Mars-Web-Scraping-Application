from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrapper_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    scraped_data = mongo.db.mars_mission.find_one()
    return render_template("index.html", scraped_data = scraped_data)

@app.route("/scrape")
def scraper():
    mars_mission = mongo.db.mars_mission
    scraped_data = scrapper_mars.scrape()
    mars_mission.update_one({}, {"$set": scraped_data}, upsert=True)
    return redirect("/", code =302 )

if __name__ == "__main__":
    app.run(debug=True)