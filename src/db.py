import sqlite3
import translator

con = sqlite3.connect("english.db")
cur = con.cursor()

def initialize_db() -> None:
    res = cur.execute("SELECT name FROM sqlite_master WHERE name='users'")

    if res.fetchone() is None:
        cur.execute("CREATE TABLE users(id)")

    res = cur.execute("SELECT name FROM sqlite_master WHERE name='words'")

    if res.fetchone() is None:
        cur.execute("CREATE TABLE words(user_id, word, translation, count)")


async def write_word(user_id: int, word: str) -> None:
    res = cur.execute(f"SELECT * FROM words where user_id = {user_id} and word = '{word}'")

    translation = await translator.translate_text(word)

    if res.fetchone() is None:
        cur.execute(f"INSERT INTO words VALUES ({user_id}, '{word}', '{translation}', 1)")
    else:
        cur.execute(f"UPDATE words SET count = count + 1")

    con.commit()

    return translation


def show_words(user_id: int) -> None:
    res = cur.execute(f"SELECT word, count FROM words WHERE user_id = {user_id}")
    return res.fetchall()
