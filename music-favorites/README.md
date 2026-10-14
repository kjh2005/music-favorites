# Music Favorites & Insights
Python/SQL desktop application and Power BI report proposal.

## Run the proof of work
Requires Python 3; no third-party packages.

```bash
python3 starter.py
```
The script loads 30 synthetic songs, creates a local SQLite database, seeds
12 synthetic favorites, checks duplicate prevention and add/remove behavior,
reopens the database to verify persistence, and exports data/favorites_export.csv.
It is safe to rerun with the generated database unchanged.

## Dataset provenance
All song titles, artists, genres, and favorite dates are fictional demo data
prepared with AI assistance. They are not Apple Music records or real listening
history. catalog.csv has 30 rows and four columns. favorites_export.csv has
12 rows and five columns. No required fields are missing.

## Planned implementation
Single-user Tkinter interface: catalog, favorites, CSV export. No login or API.
Power BI: counts by artist and genre, and current favorites by date added.
A line chart does not represent listening time or favorites later removed.
The GUI and Power BI report have not been built or tested yet.

## Required next steps
Create a GitHub repository and upload these files, including this README and
starter.py. Do not upload music.db or real personal data. Add the actual repo
URL and hosted catalog.csv link to the proposal.
Run this script yourself and understand its SQL before submitting.
On a Windows computer with Power BI Desktop, import favorites_export.csv and
create one artist-count bar chart. Record what happened in proposal section 8.
