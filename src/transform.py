"""Loads and transforms player stats from data/players_stats.csv."""

import os
import pandas as pd


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "players_stats.csv")

STAT_COLUMNS = ["points", "assists", "rebounds"]


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Load player stats from CSV into a DataFrame.

    Args:
        path: Path to the CSV file. Defaults to data/players_stats.csv.

    Returns:
        Raw DataFrame as stored on disk.

    Raises:
        FileNotFoundError: If the CSV does not exist (run fetch_data.py first).
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Stats file not found at '{path}'. Run 'python src/fetch_data.py' first."
        )
    return pd.read_csv(path)


def clean_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with missing values in key stat or identifier columns.

    Args:
        df: Raw player stats DataFrame.

    Returns:
        DataFrame with null-containing rows dropped and index reset.
    """
    required = ["player_name", "team", "games_played"] + STAT_COLUMNS
    return df.dropna(subset=required).reset_index(drop=True)


def round_per_game_averages(df: pd.DataFrame, decimals: int = 1) -> pd.DataFrame:
    """Round per-game stat columns to a consistent number of decimal places.

    The CSV already contains per-game averages as fetched from the API.
    This function normalises their precision for display and comparison.

    Args:
        df: Player stats DataFrame with points, assists, and rebounds columns.
        decimals: Number of decimal places to round to. Defaults to 1.

    Returns:
        DataFrame with stat columns rounded to the specified precision.
    """
    return df.assign(**{col: df[col].round(decimals) for col in STAT_COLUMNS})


def filter_by_team(df: pd.DataFrame, team: str) -> pd.DataFrame:
    """Return only the rows matching a given team abbreviation.

    Args:
        df: Player stats DataFrame with a 'team' column.
        team: NBA team abbreviation (e.g. 'LAL', 'GSW'). Case-insensitive.

    Returns:
        Filtered DataFrame containing only players on the specified team.
    """
    return df[df["team"].str.upper() == team.upper()].reset_index(drop=True)


def get_top_scorers(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N players ranked by points per game.

    Args:
        df: Player stats DataFrame with a 'points' column.
        n: Number of players to return. Defaults to 10.

    Returns:
        DataFrame of the top N scorers, sorted descending by points.
    """
    return df.nlargest(n, "points").reset_index(drop=True)


def get_prepared_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Load, clean, and round player stats in one step.

    Convenience function used by dashboard.py to get analysis-ready data.

    Args:
        path: Path to the CSV file. Defaults to data/players_stats.csv.

    Returns:
        Cleaned and rounded DataFrame ready for visualisation.
    """
    df = load_data(path)
    df = clean_nulls(df)
    df = round_per_game_averages(df)
    return df
