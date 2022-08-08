import requests
import json
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

@app.route('/api/v1/watching')
def watching():
    f = open('data/xeny/anime.json', encoding="utf8"); data = json.load(f)
    resp = Response(json.dumps(data))
    f.close()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/api/v1/edit', methods=['POST'])
def add():
    data = request.get_json()
    # make so u can do deletr request and add actions to specify what to do

    action = data['action']
    mediaId = data['mediaId']
    progress = data['progress']
    with open('data/xeny/anime.json', encoding="utf8") as f: local = json.load(f)
    for item in local:
        if item['mediaId'] == mediaId:
            item['progress'] = progress
            break
    with open('data/xeny/anime.json', 'w', encoding="utf8") as f1: json.dump(local, f1, indent=4); f1.close()
    f.close()
    return jsonify({'success': True})


@app.route('/api/v1/info', methods=['GET'])
def add():
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


