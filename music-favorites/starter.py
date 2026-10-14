"""Runnable proof of work: synthetic catalog -> SQLite -> favorites CSV."""
import csv, json, sqlite3
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def main():
    with (ROOT/'data/catalog.csv').open(newline='') as f:
        songs = list(csv.DictReader(f))
    assert len(songs) == 30 and len({s['song_id'] for s in songs}) == 30
    assert all(all(v.strip() for v in s.values()) for s in songs)
    con = sqlite3.connect(ROOT/'music.db')
    con.execute('PRAGMA foreign_keys = ON')
    con.executescript('''CREATE TABLE IF NOT EXISTS songs (
      song_id INTEGER PRIMARY KEY, title TEXT NOT NULL, artist TEXT NOT NULL,
      genre TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS favorites (
      song_id INTEGER PRIMARY KEY REFERENCES songs(song_id), favorited_at TEXT NOT NULL);''')
    for s in songs:
        con.execute('INSERT OR IGNORE INTO songs VALUES (?,?,?,?)', tuple(s.values()))
    for i in range(1,13):
        con.execute('INSERT OR IGNORE INTO favorites VALUES (?,?)',
                    (i, f'2026-{7+(i-1)//4:02d}-{1+(i-1)%4:02d}'))
    con.commit()
    before=con.execute('SELECT COUNT(*) FROM favorites').fetchone()[0]
    con.execute("INSERT OR IGNORE INTO favorites VALUES (1,'2026-10-14')")
    assert con.execute('SELECT COUNT(*) FROM favorites').fetchone()[0] == before
    con.execute("INSERT INTO favorites VALUES (30,'2026-10-14')")
    con.execute('DELETE FROM favorites WHERE song_id=30');con.commit()
    rows=con.execute('SELECT s.song_id,s.title,s.artist,s.genre,f.favorited_at FROM songs s JOIN favorites f ON s.song_id=f.song_id ORDER BY s.song_id').fetchall()
    with (ROOT/'data/favorites_export.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['song_id','title','artist','genre','favorited_at']);w.writerows(rows)
    con.close()
    con=sqlite3.connect(ROOT/'music.db')
    assert con.execute('SELECT COUNT(*) FROM favorites').fetchone()[0] == 12
    con.close()
    print(json.dumps({'catalog_rows':len(songs),'favorites_rows':len(rows),'missing_fields':0,
      'duplicate_favorites_blocked':True,'add_remove_checked':True,'persistence_checked':True,
      'power_bi_import_tested':False},indent=2))
if __name__=='__main__':main()
