from flask import Flask, render_template, request, Response, send_file
from flask_cors import CORS
import os
import requests
import json
import threading
from database import xenylist

PUSH_ACTIVITY_TO_MONGO = False
if PUSH_ACTIVITY_TO_MONGO:
    from scripts import latest_activity


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


@app.route("/api/rating_type")
def rating_type():
    resp = Response(json.dumps({"rating_type": conf("rating_type")}))
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route("/api/list/anime")
def anime_list():
    data = xenylist.get_anime_list()
    resp = Response(json.dumps(data))
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route("/api/list/manga")
def manga_list():
    data = xenylist.get_manga_list()
    resp = Response(json.dumps(data))
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route("/api/edit", methods=["POST"])
def edit():
    data = request.get_json()
    media_type = data["media_type"]
    media_id = data["media_id"]
    progress = data["progress"]
    score = data["score"]
    status = data["status"]

    if media_type == "anime":
        xenylist.update_anime(media_id, progress, score, status)
        if PUSH_ACTIVITY_TO_MONGO:
            threading.Thread(
                target=latest_activity.send, args=[media_id, progress, media_type]
            ).start()

    elif media_type == "manga":
        xenylist.update_manga(media_id, progress, score, status)
        if PUSH_ACTIVITY_TO_MONGO:
            threading.Thread(
                target=latest_activity.send, args=[media_id, progress, media_type]
            ).start()

    return Response(json.dumps({"success": True}))


@app.route("/api/delete", methods=["POST"])
def delete():
    data = request.get_json()
    media_type = data["media_type"]
    media_id = data["media_id"]

    if media_type == "anime":
        xenylist.delete_anime(media_id)

    elif media_type == "manga":
        xenylist.delete_manga(media_id)

    resp = Response(json.dumps({"success": True}))
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route("/api/add_media", methods=["POST"])
def add_media():
    data = request.get_json()
    # make so u can do deletr request and add actions to specify what to do
    media_id = data["media_id"]
    media_type = data["media_type"]

    if (
        media_type == "anime"
        and xenylist.check_anime_exists(media_id)
        or media_type != "anime"
        and media_type == "manga"
        and xenylist.check_manga_exists(media_id)
    ):
        resp = Response(json.dumps({"error": "Already in list"}))
        resp.headers["Content-Type"] = "application/json"
        return resp
    postme = {
        "query": "query media($id:Int,$type:MediaType,$isAdult:Boolean){Media(id:$id,type:$type,isAdult:$isAdult){id title{userPreferred romaji english native}coverImage{extraLarge large}bannerImage startDate{year month day}endDate{year month day}description season seasonYear type format status(version:2)episodes duration chapters volumes genres synonyms source(version:3)isAdult isLocked meanScore averageScore popularity favourites isFavouriteBlocked hashtag countryOfOrigin isLicensed isFavourite isRecommendationBlocked isFavouriteBlocked isReviewBlocked nextAiringEpisode{airingAt timeUntilAiring episode}relations{edges{id relationType(version:2)node{id title{userPreferred}format type status(version:2)bannerImage coverImage{large}}}}characterPreview:characters(perPage:6,sort:[ROLE,RELEVANCE,ID]){edges{id role name voiceActors(language:JAPANESE,sort:[RELEVANCE,ID]){id name{userPreferred}language:languageV2 image{large}}node{id name{userPreferred}image{large}}}}staffPreview:staff(perPage:8,sort:[RELEVANCE,ID]){edges{id role node{id name{userPreferred}language:languageV2 image{large}}}}studios{edges{isMain node{id name}}}reviewPreview:reviews(perPage:2,sort:[RATING_DESC,ID]){pageInfo{total}nodes{id summary rating ratingAmount user{id name avatar{large}}}}recommendations(perPage:7,sort:[RATING_DESC,ID]){pageInfo{total}nodes{id rating userRating mediaRecommendation{id title{userPreferred}format type status(version:2)bannerImage coverImage{large}}user{id name avatar{large}}}}externalLinks{id site url type language color icon notes isDisabled}streamingEpisodes{site title thumbnail url}trailer{id site}rankings{id rank type format year season allTime context}tags{id name description rank isMediaSpoiler isGeneralSpoiler userId}mediaListEntry{id status score}stats{statusDistribution{status amount}scoreDistribution{score amount}}}}",
        "variables": {"id": media_id, "type": media_type.upper()},
    }

    r = requests.post("https://graphql.anilist.co", json=postme)
    resp = r.json()

    title = resp["data"]["Media"]["title"]["english"]
    if resp["data"]["Media"]["title"]["english"] is None:
        title = resp["data"]["Media"]["title"]["romaji"]
    media_id = resp["data"]["Media"]["id"]
    status = "planning"
    score = 0
    progress = 0
    if media_type == "anime":
        total = resp["data"]["Media"]["episodes"]
    elif media_type == "manga":
        total = resp["data"]["Media"]["chapters"]
    image = resp["data"]["Media"]["coverImage"]["large"]
    notes = ""
    isAdult = resp["data"]["Media"]["isAdult"]

    if media_type == "anime":
        xenylist.add_media(
            "anime",
            title,
            media_id,
            status,
            score,
            progress,
            total,
            image,
            notes,
            isAdult,
        )
    elif media_type == "manga":
        xenylist.add_media(
            "manga",
            title,
            media_id,
            status,
            score,
            progress,
            total,
            image,
            notes,
            isAdult,
        )

    resp = Response(json.dumps({"title": title, "success": True}))
    return resp


@app.route("/api/search")
def search():
    query = request.args["query"]

    graphql = {
        "query": "query($search: String){anime:Page(perPage:12){results:media(type:ANIME,search:$search){id type title{english romaji} coverImage{medium} format startDate{year}}}manga:Page(perPage:12){results:media(type:MANGA,search:$search){id type title{english romaji} coverImage{medium} format startDate{year}}}}",
        "variables": {"search": query},
    }

    r = requests.post("https://graphql.anilist.co", json=graphql)

    return Response(json.dumps(r.json()))


if __name__ == "__main__":
    xenylist.initiate()
    app.run(port=2808)
