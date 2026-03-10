# Sports Statistics Dashboard

A portfolio project for a Data Engineer / Data Analyst. Interactive dashboard built with Python and Streamlit, pulling live NBA stats via the `nba_api` package and visualizing them with Plotly.

## Project Purpose
Showcase data engineering and analytics skills: data ingestion, transformation, and interactive visualization — all in one deployable app.

## Tech Stack
- **Python 3.11+**
- **Streamlit** — dashboard UI
- **nba_api** — data source (NBA player & team stats)
- **pandas** — data transformation
- **Plotly** — charts and visualizations
- **DuckDB** — lightweight local data storage (optional, for caching)

## Project Structure
```
sports-dashboard/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── players_stats.csv       # cached data fetched from nba_api
└── src/
    ├── fetch_data.py            # pulls data from nba_api and saves to data/
    ├── transform.py             # cleans and enriches the raw data
    └── dashboard.py             # Streamlit app — main entry point
```

## Commands
- `pip install -r requirements.txt` — install dependencies
- `python src/fetch_data.py` — fetch fresh NBA data (saves to data/)
- `streamlit run src/dashboard.py` — launch the dashboard locally

## Data Flow
1. `fetch_data.py` calls nba_api → saves raw CSV to `data/`
2. `transform.py` cleans nulls, calculates per-game averages, filters active players
3. `dashboard.py` loads the CSV, renders filters and charts via Streamlit + Plotly

## Dashboard Features to Build
- Sidebar filters: Season, Team, Position
- KPI cards: League leaders in PTS, AST, REB
- Bar chart: Top 10 scorers
- Scatter plot: Points vs Assists (colored by team)
- Sortable stats table with all players

## Important Notes
- NEVER commit the `data/` folder contents to GitHub (add to .gitignore) — data should be fetched fresh
- NEVER hardcode API keys — nba_api does not require a key, but keep this rule for good practice
- Keep `fetch_data.py` and `dashboard.py` separate — don't fetch data inside the Streamlit app (it will re-fetch on every page interaction)
- All chart colors should use a consistent color palette — use Plotly's "Set2" palette

## Style Guidelines
- Use pandas for all data manipulation — no raw loops over DataFrames
- Function names should be descriptive: `get_top_scorers()`, `filter_by_team()`, etc.
- Add a short docstring to every function
- Keep dashboard.py readable — move heavy logic into transform.py