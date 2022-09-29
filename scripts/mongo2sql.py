import sqlite3, json

"""Export your mongodb as a json file, excluding the _id field."""

connection = sqlite3.connect("db/list.db", check_same_thread=False)
cursor = connection.cursor()

def importx(json):
    title = json["title"]
    media_id = int(json["media_id"])
    status = json["status"]
    score = int(json["score"])
    progress = int(json["progress"])
    total = json["total"]
    image = json["image"]
    notes = json["notes"]
    isAdult = json["isAdult"]
    cursor.execute("INSERT INTO manga VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (title, media_id, status, score, progress, total, image, notes, isAdult))
    connection.commit()

def main():
    with open('manga.json', encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        entry.pop("_id")
        importx(entry)


main()