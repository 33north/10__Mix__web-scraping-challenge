from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

# # Create connection variable
# conn = 'mongodb://localhost:27017'

# # Pass connection to the pymongo instance.
# client = pymongo.MongoClient(conn)

# # Connect to a database. Will create one if not already available.
# db = client.mars_info_scraping

# # Drops collection if available to remove duplicates
# db.mars.drop()

# # Store the entire team collection in a list
# teams = db.team.find()

# # Creates a collection in the database and inserts two documents
# db.team.insert_one(data)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_info_scraping_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    print(mars_data)
    return render_template("index.html", mars_data = mars_data)


@app.route("/scrape")
def scrape():
    # mars_db = mongo.db.mars_data
    data = scrape_mars.scrape_mars_info()
    # mars_db.drop_collection("mars_data")
    # mars_db.insert_one(data)
    mongo.db.mars_data.update_one({}, {"$set": data}, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
