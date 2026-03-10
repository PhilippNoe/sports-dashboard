# NBA Stats Dashboard

An interactive sports statistics dashboard built with Python and Streamlit, pulling live NBA player data via the `nba_api` package and visualising it with Plotly.

> **Portfolio project** — built to demonstrate data engineering and analytics skills: API ingestion, data transformation, and interactive visualisation in a single deployable app.

---

## Features

- **KPI cards** — league leaders in points, assists, and rebounds
- **Top 10 scorers** — horizontal bar chart ranked by points per game
- **Points vs Assists** — scatter plot with per-team colouring
- **Full stats table** — sortable by any column
- **Sidebar filters** — filter by team (and position when available)

## Tech Stack

| Layer | Library |
|---|---|
| Dashboard UI | [Streamlit](https://streamlit.io) |
| Data source | [nba_api](https://github.com/swar/nba_api) |
| Data transformation | [pandas](https://pandas.pydata.org) |
| Charts | [Plotly](https://plotly.com/python/) |

## Project Structure

```
sports-dashboard/
├── README.md
├── requirements.txt
├── .gitignore
├── data/                        # gitignored — populated by fetch_data.py
│   └── players_stats.csv
└── src/
    ├── fetch_data.py            # pulls per-game stats from nba_api → CSV
    ├── transform.py             # cleans, filters, and aggregates data
    └── dashboard.py             # Streamlit app — main entry point
```

## Setup

**1. Clone and create a virtual environment**

```bash
git clone <repo-url>
cd sports-dashboard
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Fetch NBA data**

```bash
python src/fetch_data.py
```

This calls the NBA Stats API and writes current-season per-game averages to `data/players_stats.csv`. Re-run any time you want fresh data.

**4. Launch the dashboard**

```bash
streamlit run src/dashboard.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## Data Flow

```
nba_api  →  fetch_data.py  →  data/players_stats.csv
                                       ↓
                             transform.py  (clean, filter, aggregate)
                                       ↓
                             dashboard.py  (Streamlit + Plotly)
```

## Notes

- No API key required — `nba_api` is a free, unofficial wrapper around the public NBA Stats website.
- Data is intentionally kept out of version control. Always fetch fresh stats before running the app.
- Fetch and display are decoupled: `fetch_data.py` is a standalone script and is never called from inside the Streamlit app.
