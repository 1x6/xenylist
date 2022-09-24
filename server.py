from flask import Flask, render_template, request, Response, send_file
from flask_cors import CORS
import os
import requests
import json
import threading
import pymongo
import time


def conf(key):
    try:
        with open("config.json") as f:
            li_conf = json.load(f)
        return li_conf.get(key)
    except:
        pass


template_dir = os.path.abspath("frontend/")
static_dir = os.path.abspath("frontend/static")
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
cors = CORS(app, resources={r"/api/*": {"origins": conf("allowed_origins")}})
myclient = pymongo.MongoClient(conf("mongodb"))

#################################
# WEB SERVER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/anime")
def anime():
    return render_template("anime.html")


@app.route("/manga")
def manga():
    return render_template("manga.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/favicon.ico")
def favicon():
    return send_file("frontend/static/favicon.ico")


#################################
# API


def latest_activity(id, progress, media):

    postme = {
        "query": "query media($id:Int,$type:MediaType,$isAdult:Boolean){Media(id:$id,type:$type,isAdult:$isAdult){id title{userPreferred romaji english native}coverImage{extraLarge large}bannerImage startDate{year month day}endDate{year month day}description season seasonYear type format status(version:2)episodes duration chapters volumes genres synonyms source(version:3)isAdult isLocked meanScore averageScore popularity favourites isFavouriteBlocked hashtag countryOfOrigin isLicensed isFavourite isRecommendationBlocked isFavouriteBlocked isReviewBlocked nextAiringEpisode{airingAt timeUntilAiring episode}relations{edges{id relationType(version:2)node{id title{userPreferred}format type status(version:2)bannerImage coverImage{large}}}}characterPreview:characters(perPage:6,sort:[ROLE,RELEVANCE,ID]){edges{id role name voiceActors(language:JAPANESE,sort:[RELEVANCE,ID]){id name{userPreferred}language:languageV2 image{large}}node{id name{userPreferred}image{large}}}}staffPreview:staff(perPage:8,sort:[RELEVANCE,ID]){edges{id role node{id name{userPreferred}language:languageV2 image{large}}}}studios{edges{isMain node{id name}}}reviewPreview:reviews(perPage:2,sort:[RATING_DESC,ID]){pageInfo{total}nodes{id summary rating ratingAmount user{id name avatar{large}}}}recommendations(perPage:7,sort:[RATING_DESC,ID]){pageInfo{total}nodes{id rating userRating mediaRecommendation{id title{userPreferred}format type status(version:2)bannerImage coverImage{large}}user{id name avatar{large}}}}externalLinks{id site url type language color icon notes isDisabled}streamingEpisodes{site title thumbnail url}trailer{id site}rankings{id rank type format year season allTime context}tags{id name description rank isMediaSpoiler isGeneralSpoiler userId}mediaListEntry{id status score}stats{statusDistribution{status amount}scoreDistribution{score amount}}}}",
        "variables": {"id": id, "type": media.upper()},
    }

    r = requests.post("https://graphql.anilist.co", json=postme)
    resp = r.json()

    title = resp["data"]["Media"]["title"]["english"]
    if resp["data"]["Media"]["title"]["english"] is None:
        title = resp["media"]["title"]["romaji"]

    data = {
        "media_id": id,
        "progress": progress,
        "media": media,
        "title": title,
        "time": round(time.time() * 1000),
    }

    mydb = myclient["latest"]
    mycol = mydb["latest"]
    query = {}
    newval = {"$set": data}
    mycol.update_one(query, newval, upsert=True)


@app.route("/api/v1/latest")
def latest():
    mydb = myclient["latest"]
    mycol = mydb["latest"]
    data = mycol.find({})
    l = []
    for x in data:
        x.pop("_id")
        l.append(x)
    resp = Response(json.dumps(l))

    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route("/api/v1/rating_type")
def rating_type():
    resp = Response(json.dumps({"rating_type": conf("rating_type")}))
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route("/api/v1/list/anime")
def anime_list():
    mydb = myclient["lists"]
    mycol = mydb["anime"]
    data = []
    for x in mycol.find():
        x.pop("_id")
        data.append(x)
    resp = Response(json.dumps(data))
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route("/api/v1/list/manga")
def manga_list():
    mydb = myclient["lists"]
    mycol = mydb["manga"]
    data = []
    for x in mycol.find():
        x.pop("_id")
        data.append(x)
    resp = Response(json.dumps(data))
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route("/api/v1/edit", methods=["POST"])
def edit():
    data = request.get_json()
    media_type = data["media_type"]
    media_id = data["media_id"]
    progress = data["progress"]
    score = data["score"]
    status = data["status"]

    if media_type == "anime":
        mydb = myclient["lists"]
        mycol = mydb["anime"]
        myquery = {"media_id": media_id}
        newvalues = {
            "$set": {"progress": progress, "score": score, "status": status}
        }
        mycol.update_one(myquery, newvalues)
        threading.Thread(
            target=latest_activity, args=[media_id, progress, media_type]
        ).start()

    elif media_type == "manga":
        mydb = myclient["lists"]
        mycol = mydb["manga"]
        myquery = {"media_id": media_id}
        newvalues = {
            "$set": {"progress": progress, "score": score, "status": status}
        }
        mycol.update_one(myquery, newvalues)
        threading.Thread(
            target=latest_activity, args=[media_id, progress, media_type]
        ).start()

    resp = Response(json.dumps({"success": True}))
    return resp


@app.route("/api/v1/delete", methods=["POST"])
def delete():
    data = request.get_json()
    media_type = data["media_type"]
    media_id = data["media_id"]

    if media_type == "anime":
        mydb = myclient["lists"]
        mycol = mydb["anime"]
        myquery = {"media_id": media_id}
        mycol.delete_one(myquery)

    elif media_type == "manga":
        mydb = myclient["lists"]
        mycol = mydb["manga"]
        myquery = {"media_id": media_id}
        mycol.delete_one(myquery)

    resp = Response(json.dumps({"success": True}))
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route("/api/v1/add_media", methods=["POST"])
def add_media():
    data = request.get_json()
    # make so u can do deletr request and add actions to specify what to do
    media_id = data["media_id"]
    media_type = data["media_type"]

    if media_type == "anime":
        mycol = myclient["lists"]["anime"]
        query = {"media_id": media_id}
        if mycol.find_one(query) is not None:
            resp = Response(json.dumps({"error": "Already in list"}))
            resp.headers["Content-Type"] = "application/json"
            return resp
    if media_type == "manga":
        mycol = myclient["lists"]["manga"]
        query = {"media_id": media_id}
        if mycol.find_one(query) is not None:
            resp = Response(json.dumps({"error": "Already in list"}))
            resp.headers["Content-Type"] = "application/json"
            return resp

    postme = {
        "query": "query media($id:Int,$type:MediaType,$isAdult:Boolean){Media(id:$id,type:$type,isAdult:$isAdult){id title{userPreferred romaji english native}coverImage{extraLarge large}bannerImage startDate{year month day}endDate{year month day}description season seasonYear type format status(version:2)episodes duration chapters volumes genres synonyms source(version:3)isAdult isLocked meanScore averageScore popularity favourites isFavouriteBlocked hashtag countryOfOrigin isLicensed isFavourite isRecommendationBlocked isFavouriteBlocked isReviewBlocked nextAiringEpisode{airingAt timeUntilAiring episode}relations{edges{id relationType(version:2)node{id title{userPreferred}format type status(version:2)bannerImage coverImage{large}}}}characterPreview:characters(perPage:6,sort:[ROLE,RELEVANCE,ID]){edges{id role name voiceActors(language:JAPANESE,sort:[RELEVANCE,ID]){id name{userPreferred}language:languageV2 image{large}}node{id name{userPreferred}image{large}}}}staffPreview:staff(perPage:8,sort:[RELEVANCE,ID]){edges{id role node{id name{userPreferred}language:languageV2 image{large}}}}studios{edges{isMain node{id name}}}reviewPreview:reviews(perPage:2,sort:[RATING_DESC,ID]){pageInfo{total}nodes{id summary rating ratingAmount user{id name avatar{large}}}}recommendations(perPage:7,sort:[RATING_DESC,ID]){pageInfo{total}nodes{id rating userRating mediaRecommendation{id title{userPreferred}format type status(version:2)bannerImage coverImage{large}}user{id name avatar{large}}}}externalLinks{id site url type language color icon notes isDisabled}streamingEpisodes{site title thumbnail url}trailer{id site}rankings{id rank type format year season allTime context}tags{id name description rank isMediaSpoiler isGeneralSpoiler userId}mediaListEntry{id status score}stats{statusDistribution{status amount}scoreDistribution{score amount}}}}",
        "variables": {"id": media_id, "type": media_type.upper()},
    }

    r = requests.post("https://graphql.anilist.co", json=postme)
    resp = r.json()

    _dict = {}

    _dict["title"] = resp["data"]["Media"]["title"]["english"]
    if resp["data"]["Media"]["title"]["english"] is None:
        _dict["title"] = resp["data"]["Media"]["title"]["romaji"]
    _dict["media_id"] = resp["data"]["Media"]["id"]
    _dict["status"] = "planning"
    _dict["score"] = 0
    _dict["progress"] = 0
    if media_type == "anime":
        _dict["total"] = resp["data"]["Media"]["episodes"]
    elif media_type == "manga":
        _dict["total"] = resp["data"]["Media"]["chapters"]
    _dict["image"] = resp["data"]["Media"]["coverImage"]["large"]
    _dict["notes"] = ""
    _dict["isAdult"] = resp["data"]["Media"]["isAdult"]

    mydb = myclient["lists"]
    if media_type == "anime":
        mycol = mydb["anime"]
    elif media_type == "manga":
        mycol = mydb["manga"]

    mycol.insert_one(_dict)

    resp = Response(json.dumps({"title": _dict["title"], "success": True}))
    return resp


@app.route("/api/v1/search")
def search():
    query = request.args["query"]

    graphql = {
        "query": "query($search: String){anime:Page(perPage:12){results:media(type:ANIME,search:$search){id type title{english romaji} coverImage{medium} format startDate{year}}}manga:Page(perPage:12){results:media(type:MANGA,search:$search){id type title{english romaji} coverImage{medium} format startDate{year}}}}",
        "variables": {"search": query},
    }

    r = requests.post("https://graphql.anilist.co", json=graphql)

    resp = Response(json.dumps(r.json()))
    return resp


if __name__ == "__main__":
    app.run(port=2808)
