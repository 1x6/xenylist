import requests, json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
}

# update ur headers 

MEDIA_TYPE = 'anime'

data1 = {"query":"query($userId:Int,$userName:String,$type:MediaType){MediaListCollection(userId:$userId,userName:$userName,type:$type){lists{name isCustomList isCompletedList:isSplitCompletedList entries{...mediaListEntry}}user{id name avatar{large}mediaListOptions{scoreFormat rowOrder animeList{sectionOrder customLists splitCompletedSectionByFormat theme}mangaList{sectionOrder customLists splitCompletedSectionByFormat theme}}}}}fragment mediaListEntry on MediaList{id mediaId status score progress progressVolumes repeat priority private hiddenFromStatusLists customLists advancedScores notes updatedAt startedAt{year month day}completedAt{year month day}media{id title{userPreferred romaji english native}coverImage{extraLarge large}type format status(version:2)episodes volumes chapters averageScore popularity isAdult countryOfOrigin genres bannerImage startDate{year month day}}}","variables":{"userId":5964458,"type":f"{MEDIA_TYPE.upper()}"}}

response = requests.post('https://graphql.anilist.co', headers=headers, json=data1)
print(data1)
rj = response.json()
print(response.text)
# function to add to JSON
feeds = []

with open(f"data/xeny/{MEDIA_TYPE}.json", "r") as f:
    data = json.load(f)
    feeds.append(data)

for i in range(len(rj['data']['MediaListCollection']['lists'])):
    for item in rj["data"]["MediaListCollection"]["lists"][i]["entries"]:
        dic = {}
        print(item)
        dic["title"] = item["media"]["title"]["english"]
        if item["media"]["title"]["english"] == None:
            dic["title"] = item["media"]["title"]["romaji"]
        dic["media_id"] = item["mediaId"]
        dic["status"] = item["status"].lower()
        dic["score"] = item["score"]
        dic["progress"] = item["progress"]
        dic["image"] = item["media"]["coverImage"]["large"]
        feeds.append(dic)
        print(dic)
        with open(f"data/xeny/{MEDIA_TYPE}.json", 'w') as json_file:
            json.dump(feeds, json_file, 
                            indent=4,  
                            separators=(',',': '))
