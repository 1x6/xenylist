import sqlite3, json, time

connection = sqlite3.connect("db/list.db", check_same_thread=False)
cursor = connection.cursor()

LIST = "anime"


def importx():
    title = "TEST SUBJECT"
    media_id = 999
    status = "MEOWWWWW"
    score = 9999
    progress = 9999
    total = 9999
    image = "ZZZZZZ"
    notes = "CAT"
    isAdult = "TRUE"
    cursor.execute(
        "INSERT INTO ? VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (LIST, title, media_id, status, score, progress, total, image, notes, isAdult),
    )
    connection.commit()


importx()
