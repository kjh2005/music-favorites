# Music Favorites browser demo

Unzip the folder. In Terminal, type `cd ` (with a trailing space), drag the extracted folder in, and press Enter. Run `python3 demo.py`, then open http://127.0.0.1:8000 in your browser. Keep Terminal running. If the port is busy, run `python3 demo.py --port 8001` and open http://127.0.0.1:8001.

Search for Pink Skies, save it with the heart, open My Favorites, and refresh to demonstrate persistence. Tap the filled heart to remove it. All 12 songs are fictional. No packages or online accounts are required.

When you click a heart, the browser sends POST or DELETE to /api/favorites/<song_id>. Python adds or removes that ID in SQLite. GET /api/songs reads saved IDs when the page opens. Supabase sign-in is a future step.

This demo uses its own local database, browser_favorites.sqlite3. If you add the demo to GitHub, commit demo.py, index.html, and this README, and leave the generated database out. Your Tkinter prototype can stay in the repository.
