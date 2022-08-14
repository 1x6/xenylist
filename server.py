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
def add():
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

        if media_type == 'anime':
            with open('data/xeny/anime.json', encoding="utf8") as f: local = json.load(f)
            for item in local:
                if item['media_id'] == media_id:
                    item['progress'] = progress
                    item['score'] = score
                    item['status'] = status
                    break

            with open('data/xeny/anime.json', 'w', encoding="utf8") as f1: json.dump(local, f1, indent=4); f1.close()
            f.close()

        if media_type == 'manga':
            with open('data/xeny/manga.json', encoding="utf8") as f: local = json.load(f)
            for item in local:
                if item['media_id'] == media_id:
                    item['progress'] = progress
                    item['score'] = score
                    break

            with open('data/xeny/manga.json', 'w', encoding="utf8") as f1: json.dump(local, f1, indent=4); f1.close()
            f.close()

    resp = Response(json.dumps({'success': True}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/v1/info', methods=['GET'])
def info():
    data = request.get_json()

    _type = data['_type']
    mediaId = data['mediaId']
    if _type == 'anime':
        with open('data/xeny/anime.json', encoding="utf8") as f: local = json.load(f)
        for item in local:
            if item['mediaId'] == mediaId:
                return jsonify(item)
    
    elif _type == 'manga':
        with open('data/xeny/manga.json', encoding="utf8") as f: local = json.load(f)
        for item in local:
            if item['mediaId'] == mediaId:
                return jsonify(item)

    else:
        return jsonify({'error': 'bad request??'}, 400)
        
app.run(debug=True, host='0.0.0.0', port=2808)


