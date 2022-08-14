import requests
import json
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

@app.route('/api/v1/list/anime')
def anime_list():
    f = open('data/xeny/anime.json', encoding="utf8"); data = json.load(f)
    resp = Response(json.dumps(data))
    f.close()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/api/v1/list/manga')
def manga_list():
    f = open('data/xeny/manga.json', encoding="utf8"); data = json.load(f)
    resp = Response(json.dumps(data))
    f.close()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/api/v1/edit', methods=['POST', 'OPTIONS'])
def edit():
    if request.method == 'OPTIONS':
        resp = Response('')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return resp
    elif request.method == 'POST':
        data = request.get_json()
        # make so u can do deletr request and add actions to specify what to do
        media_type = data['media_type']
        media_id = data['media_id']
        progress = data['progress']
        score = data['score']
        status = data['status']
        #status = data['status'] for dropdown watching, completed, onhold, dropped

        
        with open(f'data/xeny/{media_type}.json', encoding="utf8") as f: local = json.load(f)
        for item in local:
            if item['media_id'] == media_id:
                item['progress'] = progress
                item['score'] = score
                item['status'] = status
                break

        with open(f'data/xeny/{media_type}.json', 'w', encoding="utf8") as f1: json.dump(local, f1, indent=4); f1.close()
        f.close()


    resp = Response(json.dumps({'success': True}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/v1/add_media', methods=['POST', 'OPTIONS'])
def add_media():
    if request.method == 'OPTIONS':
        resp = Response('')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return resp
    elif request.method == 'POST':
        data = request.get_json()
        # make so u can do deletr request and add actions to specify what to do
        media_id = data['media_id']
        media_type = data['media_type']
        
        postme = {"query":"query media($id:Int,$type:MediaType,$isAdult:Boolean){Media(id:$id,type:$type,isAdult:$isAdult){id title{userPreferred romaji english native}coverImage{extraLarge large}bannerImage startDate{year month day}endDate{year month day}description season seasonYear type format status(version:2)episodes duration chapters volumes genres synonyms source(version:3)isAdult isLocked meanScore averageScore popularity favourites isFavouriteBlocked hashtag countryOfOrigin isLicensed isFavourite isRecommendationBlocked isFavouriteBlocked isReviewBlocked nextAiringEpisode{airingAt timeUntilAiring episode}relations{edges{id relationType(version:2)node{id title{userPreferred}format type status(version:2)bannerImage coverImage{large}}}}characterPreview:characters(perPage:6,sort:[ROLE,RELEVANCE,ID]){edges{id role name voiceActors(language:JAPANESE,sort:[RELEVANCE,ID]){id name{userPreferred}language:languageV2 image{large}}node{id name{userPreferred}image{large}}}}staffPreview:staff(perPage:8,sort:[RELEVANCE,ID]){edges{id role node{id name{userPreferred}language:languageV2 image{large}}}}studios{edges{isMain node{id name}}}reviewPreview:reviews(perPage:2,sort:[RATING_DESC,ID]){pageInfo{total}nodes{id summary rating ratingAmount user{id name avatar{large}}}}recommendations(perPage:7,sort:[RATING_DESC,ID]){pageInfo{total}nodes{id rating userRating mediaRecommendation{id title{userPreferred}format type status(version:2)bannerImage coverImage{large}}user{id name avatar{large}}}}externalLinks{id site url type language color icon notes isDisabled}streamingEpisodes{site title thumbnail url}trailer{id site}rankings{id rank type format year season allTime context}tags{id name description rank isMediaSpoiler isGeneralSpoiler userId}mediaListEntry{id status score}stats{statusDistribution{status amount}scoreDistribution{score amount}}}}",
        "variables":{"id":media_id,"type":media_type.upper()}}

        r = requests.post("https://graphql.anilist.co", json=postme)
        resp = r.json()

        feeds = []

        with open(f"data/xeny/{media_type}.json", "r") as f:
            data = json.load(f)
            for x in data:
                feeds.append(x)

        f.close()

        _dict = {}

        _dict["title"] = resp["data"]["Media"]["title"]["english"]
        if resp["data"]["Media"]["title"]["english"] == None:
            _dict["title"] = resp["media"]["title"]["romaji"]
        _dict["media_id"] = resp["data"]["Media"]["id"]
        _dict["status"] = "planning"
        _dict["score"] = 0
        _dict["progress"] = 0
        _dict["image"] = resp["data"]["Media"]["coverImage"]["large"]
        
        feeds.append(_dict)

        with open(f"data/xeny/{media_type}.json", 'w') as json_file:
            json.dump(feeds, json_file, 
                            indent=4,  
                            separators=(',',': '))
        json_file.close()

        resp = Response(json.dumps({'title': _dict["title"], "success": True}))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
        
app.run(debug=True, host='0.0.0.0', port=2808)


