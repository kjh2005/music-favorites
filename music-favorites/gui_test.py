import sqlite3
import tkinter as tk
from pathlib import Path

# Store the database beside this Python file.
db_path = Path(__file__).with_name("window_test.db")
connection = sqlite3.connect(db_path)

connection.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        song_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL
    )
""")
connection.commit()

window = tk.Tk()
window.title("Music Favorites Test")
window.geometry("380x220")

status = tk.StringVar()


def refresh():
    saved = connection.execute(
        "SELECT title FROM favorites WHERE song_id = ?",
        (1,)
    ).fetchone()

    if saved:
        status.set("Saved favorite: " + saved[0])
    else:
        status.set("No favorite saved.")


def favorite():
    connection.execute(
        "INSERT OR IGNORE INTO favorites VALUES (?, ?)",
        (1, "Demo Song 01")
    )
    connection.commit()
    refresh()


def remove():
    connection.execute(
        "DELETE FROM favorites WHERE song_id = ?",
        (1,)
    )
    connection.commit()
    refresh()


def close():
    connection.close()
    window.destroy()


tk.Label(window, text="Demo Song 01", font=("", 16)).pack(pady=15)
tk.Button(window, text="Favorite", command=favorite).pack(pady=5)
tk.Button(window, text="Remove Favorite", command=remove).pack(pady=5)
tk.Label(window, textvariable=status).pack(pady=15)

window.protocol("WM_DELETE_WINDOW", close)
refresh()
window.mainloop()
