import sqlite3, json 


connection = sqlite3.connect("db/list.db", check_same_thread=False)
cursor = connection.cursor()


class xenylist: 

    def initiate() -> None: 
        """ Creates all tables if they do not exist"""

        cursor.execute("""CREATE TABLE IF NOT EXISTS anime (
            title text,
            media_id int,
            status text,
            score int, 
            progress int,
            total int,
            image text,
            notes text,
            isAdult text
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS manga (
            title text,
            media_id int,
            status text,
            score int, 
            progress int,
            total int,
            image text,
            notes text,
            isAdult text
        )""")

        connection.commit()

    def get_anime_list(): 
        query = cursor.execute("SELECT * FROM anime")
        anime = []
        for entry in query.fetchall():
            data = {}
            data["title"] = entry[0]
            data["media_id"] = entry[1]
            data["status"] = entry[2]
            data["score"] = entry[3]
            data["progress"] = entry[4]
            data["total"] = entry[5]
            data["image"] = entry[6]
            data["notes"] = entry[7]
            data["isAdult"] = entry[8]
            anime.append(data)
        return anime
            
    def get_manga_list(): 
        query = cursor.execute("SELECT * FROM manga")
        manga = []
        for entry in query.fetchall():
            data = {}
            data["title"] = entry[0]
            data["media_id"] = entry[1]
            data["status"] = entry[2]
            data["score"] = entry[3]
            data["progress"] = entry[4]
            data["total"] = entry[5]
            data["image"] = entry[6]
            data["notes"] = entry[7]
            data["isAdult"] = entry[8]
            manga.append(data)
        return manga

    def update_anime(media_id, progress, score, status):
        cursor.execute(
            """UPDATE anime SET progress = ?, score = ?, status = ? WHERE media_id = ?""",
            (progress, score, status, media_id,)
        )
        connection.commit()
            
    def update_manga(media_id, progress, score, status):
        cursor.execute(
            """UPDATE manga SET progress = ?, score = ?, status = ? WHERE media_id = ?""",
            (progress, score, status, media_id,)
        )
        connection.commit()

    def delete_anime(media_id):
        cursor.execute(
            """DELETE FROM anime WHERE media_id = ?""",
            (media_id,)
        )

    def delete_manga(media_id):
        cursor.execute(
            """DELETE FROM manga WHERE media_id = ?""",
            (media_id,)
        )

    def check_anime_exists(media_id):
        rows = cursor.execute(
            """SELECT title FROM anime WHERE media_id = ? """,
            (media_id,)
            ).fetchall()
        if len(rows) >= 1:
            return True
        else:
            return False

    def check_manga_exists(media_id):
        rows = cursor.execute(
            """SELECT title FROM manga WHERE media_id = ? """,
            (media_id,)
            ).fetchall()
        if len(rows) >= 1:
            return True
        else:
            return False

    def add_media(_type, title, media_id, status, score, progress, total, image, notes, isAdult):
        cursor.execute(
            """INSERT INTO TYPE VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""".replace("TYPE", _type),
            (title, media_id, status, score, progress, total, image, notes, isAdult,)
            )
        connection.commit()
