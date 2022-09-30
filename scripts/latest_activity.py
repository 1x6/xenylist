import pymongo
import json
import requests
import time

def conf(key):
    try:
        with open("config.json") as f:
            li_conf = json.load(f)
        return li_conf.get(key)
    except:
        pass

myclient = pymongo.MongoClient(conf("mongodb"))


def send(id, progress, media):

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
