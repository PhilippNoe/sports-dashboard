"""Streamlit dashboard for NBA player statistics."""

import streamlit as st
import plotly.express as px
import pandas as pd

from transform import get_prepared_data, filter_by_team, get_top_scorers


PALETTE = px.colors.qualitative.Set2


# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="NBA Stats Dashboard",
    page_icon="🏀",
    layout="wide",
)


# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and prepare player stats, cached so Streamlit doesn't reload on interaction.

    Returns:
        Cleaned and rounded DataFrame from data/players_stats.csv.
    """
    return get_prepared_data()


# ── Sidebar filters ───────────────────────────────────────────────────────────

def build_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar filters and return the filtered DataFrame.

    Applies Team and Position filters. Position filter is shown only when
    a 'position' column is present in the data.

    Args:
        df: Full prepared player stats DataFrame.

    Returns:
        DataFrame filtered by the user's sidebar selections.
    """
    st.sidebar.title("Filters")

    teams = sorted(df["team"].unique())
    selected_teams = st.sidebar.multiselect(
        "Team",
        options=teams,
        default=[],
        placeholder="All teams",
    )

    selected_positions = []
    if "position" in df.columns:
        positions = sorted(df["position"].dropna().unique())
        selected_positions = st.sidebar.multiselect(
            "Position",
            options=positions,
            default=[],
            placeholder="All positions",
        )

    filtered = df.copy()
    if selected_teams:
        filtered = pd.concat(
            [filter_by_team(filtered, t) for t in selected_teams],
            ignore_index=True,
        )
    if selected_positions:
        filtered = filtered[filtered["position"].isin(selected_positions)].reset_index(drop=True)

    return filtered


# ── KPI cards ─────────────────────────────────────────────────────────────────

def render_kpi_cards(df: pd.DataFrame) -> None:
    """Display KPI cards for the league leader in points, assists, and rebounds.

    Args:
        df: Filtered player stats DataFrame.
    """
    stats = {
        "Points": ("points", "🏆"),
        "Assists": ("assists", "🎯"),
        "Rebounds": ("rebounds", "💪"),
    }

    cols = st.columns(len(stats))
    for col, (label, (stat, icon)) in zip(cols, stats.items()):
        if df.empty:
            col.metric(f"{icon} {label} Leader", "—")
        else:
            leader_row = df.loc[df[stat].idxmax()]
            col.metric(
                label=f"{icon} {label} Leader",
                value=f"{leader_row[stat]} {label[0:3].upper()}",
                delta=leader_row["player_name"],
                delta_color="off",
            )


# ── Bar chart ─────────────────────────────────────────────────────────────────

def render_top_scorers_bar(df: pd.DataFrame) -> None:
    """Render a horizontal bar chart of the top 10 scorers.

    Args:
        df: Filtered player stats DataFrame.
    """
    st.subheader("Top 10 Scorers")

    if df.empty:
        st.info("No data for the current filter selection.")
        return

    top = get_top_scorers(df, n=10).sort_values("points")

    fig = px.bar(
        top,
        x="points",
        y="player_name",
        orientation="h",
        text="points",
        color="team",
        color_discrete_sequence=PALETTE,
        labels={"points": "Points per Game", "player_name": "Player", "team": "Team"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        showlegend=True,
        yaxis_title=None,
        xaxis_title="Points per Game",
        margin={"t": 20},
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Scatter plot ──────────────────────────────────────────────────────────────

def render_pts_ast_scatter(df: pd.DataFrame) -> None:
    """Render a scatter plot of points vs assists, coloured by team.

    Args:
        df: Filtered player stats DataFrame.
    """
    st.subheader("Points vs Assists")

    if df.empty:
        st.info("No data for the current filter selection.")
        return

    fig = px.scatter(
        df,
        x="assists",
        y="points",
        color="team",
        hover_name="player_name",
        hover_data={"rebounds": True, "games_played": True, "team": False},
        color_discrete_sequence=PALETTE,
        labels={
            "assists": "Assists per Game",
            "points": "Points per Game",
            "team": "Team",
            "rebounds": "Rebounds",
            "games_played": "GP",
        },
    )
    fig.update_traces(marker={"size": 7, "opacity": 0.75})
    fig.update_layout(margin={"t": 20})
    st.plotly_chart(fig, use_container_width=True)


# ── Stats table ───────────────────────────────────────────────────────────────

def render_stats_table(df: pd.DataFrame) -> None:
    """Render a sortable stats table for all players in the filtered dataset.

    Args:
        df: Filtered player stats DataFrame.
    """
    st.subheader("Player Stats")

    if df.empty:
        st.info("No data for the current filter selection.")
        return

    display_cols = ["player_name", "team", "games_played", "points", "assists", "rebounds"]
    if "position" in df.columns:
        display_cols.insert(2, "position")

    st.dataframe(
        df[display_cols].sort_values("points", ascending=False).reset_index(drop=True),
        use_container_width=True,
        column_config={
            "player_name": st.column_config.TextColumn("Player"),
            "team": st.column_config.TextColumn("Team"),
            "position": st.column_config.TextColumn("Pos"),
            "games_played": st.column_config.NumberColumn("GP"),
            "points": st.column_config.NumberColumn("PTS", format="%.1f"),
            "assists": st.column_config.NumberColumn("AST", format="%.1f"),
            "rebounds": st.column_config.NumberColumn("REB", format="%.1f"),
        },
        hide_index=True,
    )


# ── Main layout ───────────────────────────────────────────────────────────────

def main() -> None:
    """Entry point: build the full Streamlit dashboard layout."""
    st.title("NBA Stats Dashboard")
    st.caption("Per-game averages · Current season")

    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    filtered_df = build_sidebar(df)

    render_kpi_cards(filtered_df)

    st.divider()

    left, right = st.columns(2)
    with left:
        render_top_scorers_bar(filtered_df)
    with right:
        render_pts_ast_scatter(filtered_df)

    st.divider()

    render_stats_table(filtered_df)


if __name__ == "__main__":
    main()
