"""Fetches current season NBA player stats from nba_api and saves to data/."""

import os
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_PATH = os.path.join(DATA_DIR, "players_stats.csv")

COLUMNS = {
    "PLAYER_NAME": "player_name",
    "TEAM_ABBREVIATION": "team",
    "GP": "games_played",
    "PTS": "points",
    "AST": "assists",
    "REB": "rebounds",
}


def fetch_player_stats(season: str = "2024-25") -> pd.DataFrame:
    """Fetch per-game player stats for all players in the given season.

    Args:
        season: NBA season string in 'YYYY-YY' format. Defaults to 2024-25.

    Returns:
        DataFrame with raw stats for all players.
    """
    response = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed="PerGame",
    )
    return response.get_data_frames()[0]


def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only the relevant columns and rename them to snake_case.

    Args:
        df: Raw DataFrame returned by the nba_api endpoint.

    Returns:
        DataFrame with a reduced, renamed set of columns.
    """
    return df[list(COLUMNS.keys())].rename(columns=COLUMNS)


def save_to_csv(df: pd.DataFrame, path: str = OUTPUT_PATH) -> None:
    """Save a DataFrame to CSV, creating parent directories if needed.

    Args:
        df: DataFrame to persist.
        path: Destination file path. Defaults to data/players_stats.csv.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} player records to {path}")


def main() -> None:
    """Fetch current season player stats and write them to data/players_stats.csv."""
    print("Fetching NBA player stats...")
    raw = fetch_player_stats()
    df = select_columns(raw)
    save_to_csv(df)


if __name__ == "__main__":
    main()
