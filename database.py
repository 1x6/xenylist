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
            data = {
                "title": entry[0],
                "media_id": entry[1],
                "status": entry[2],
                "score": entry[3],
                "progress": entry[4],
                "total": entry[5],
                "image": entry[6],
                "notes": entry[7],
                "isAdult": entry[8],
            }
            anime.append(data)
        return anime
            
    def get_manga_list(): 
        query = cursor.execute("SELECT * FROM manga")
        manga = []
        for entry in query.fetchall():
            data = {
                "title": entry[0],
                "media_id": entry[1],
                "status": entry[2],
                "score": entry[3],
                "progress": entry[4],
                "total": entry[5],
                "image": entry[6],
                "notes": entry[7],
                "isAdult": entry[8],
            }
            manga.append(data)
        return manga

    def update_anime(self, progress, score, status):
        cursor.execute(
            """UPDATE anime SET progress = ?, score = ?, status = ? WHERE media_id = ?""",
            (progress, score, status, self),
        )
        connection.commit()
            
    def update_manga(self, progress, score, status):
        cursor.execute(
            """UPDATE manga SET progress = ?, score = ?, status = ? WHERE media_id = ?""",
            (progress, score, status, self),
        )
        connection.commit()

    def delete_anime(self):
        cursor.execute("""DELETE FROM anime WHERE media_id = ?""", (self, ))

    def delete_manga(self):
        cursor.execute("""DELETE FROM manga WHERE media_id = ?""", (self, ))

    def check_anime_exists(self):
        rows = cursor.execute(
            """SELECT title FROM anime WHERE media_id = ? """, (self,)
        ).fetchall()
        return len(rows) >= 1

    def check_manga_exists(self):
        rows = cursor.execute(
            """SELECT title FROM manga WHERE media_id = ? """, (self,)
        ).fetchall()
        return len(rows) >= 1

    def add_media(_type, title, media_id, status, score, progress, total, image, notes, isAdult):
        cursor.execute(
            """INSERT INTO TYPE VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""".replace("TYPE", _type),
            (title, media_id, status, score, progress, total, image, notes, isAdult,)
            )
        connection.commit()
