from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json, sqlite3, re

ROOT = Path(__file__).resolve().parent
DB = ROOT / 'browser_favorites.sqlite3'
SONGS = [
    ("Snooze", "SZA", "R&B"),
    ("Damage", "H.E.R.", "R&B"),
    ("On & On", "Erykah Badu", "Old School R&B"),
    ("Weak", "SWV", "Old School R&B"),
    ("Can We Talk", "Tevin Campbell", "Old School R&B"),
    ("Get You", "Daniel Caesar feat. Kali Uchis", "R&B"),
    ("Alright", "Kendrick Lamar", "Hip-Hop/Rap"),
    ("Work It", "Missy Elliott", "Hip-Hop/Rap"),
    ("Ms. Jackson", "Outkast", "Hip-Hop/Rap"),
    ("Levitating", "Dua Lipa", "Pop"),
    ("Espresso", "Sabrina Carpenter", "Pop"),
    ("Style", "Taylor Swift", "Pop"),
    ("Dreams", "Fleetwood Mac", "Rock"),
    ("Everlong", "Foo Fighters", "Rock"),
    ("Misery Business", "Paramore", "Rock"),
]
def query(sql, args=()):
    with sqlite3.connect(DB) as db:
        return db.execute(sql,args).fetchall()

class Handler(BaseHTTPRequestHandler):
    def send(self, status, body, kind='application/json'):
        data = json.dumps(body).encode() if kind=='application/json' else body
        self.send_response(status)
        self.send_header('Content-Type',kind)
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store')
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        if self.path=='/':
            self.send(200,(ROOT/'index.html').read_bytes(),'text/html; charset=utf-8')
        elif self.path=='/api/songs':
            saved = {row[0] for row in query('SELECT song_id FROM favorites')}
            self.send(200,[dict(id=i,title=t,artist=a,genre=g,saved=i in saved)
                for i,(t,a,g) in enumerate(SONGS,1)])
        else:
            self.send(404,{'error':'Not found'})
    def change(self, save):
        match=re.fullmatch(r'/api/favorites/(\d{1,2})',self.path)
        if not match or not 1<=int(match[1])<=len(SONGS):
            return self.send(404,{'error':'Song not found'})
        sql = 'INSERT OR IGNORE INTO favorites(song_id) VALUES (?)' if save else 'DELETE FROM favorites WHERE song_id=?'
        query(sql,(int(match[1]),))
        self.send(200,{'saved':save})
    def do_POST(self): self.change(True)
    def do_DELETE(self): self.change(False)

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=8000)
    args=parser.parse_args()
    query('CREATE TABLE IF NOT EXISTS favorites(song_id INTEGER PRIMARY KEY)')
    server = HTTPServer(('127.0.0.1',args.port), Handler)
    print(f'Music Favorites: http://127.0.0.1:{args.port}',flush=True)
    server.serve_forever()
