from pathlib import Path

import matplotlib.pyplot as plt
from pybaseball import statcast_pitcher


PLAYER_ID = 694973
START_DATE = "2025-03-01"
END_DATE = "2025-11-01"

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)


def save_bar_chart(data, x_col, y_col, title, ylabel, filename):
    plt.figure(figsize=(10, 6))
    plt.bar(data[x_col], data[y_col])
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Pitch Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUTS / filename, dpi=300)
    plt.close()


def save_summary_table(data):
    display_data = data.copy()
    display_data["usage_rate"] = display_data["usage_rate"].map(lambda value: f"{value:.1%}")
    display_data["avg_velocity"] = display_data["avg_velocity"].map(lambda value: f"{value:.1f} mph")
    display_data["whiff_rate"] = display_data["whiff_rate"].map(lambda value: f"{value:.1%}")
    display_data["strike_rate"] = display_data["strike_rate"].map(lambda value: f"{value:.1%}")

    display_data = display_data[
        ["pitch_name", "usage_rate", "avg_velocity", "whiff_rate", "strike_rate"]
    ].rename(
        columns={
            "pitch_name": "Pitch",
            "usage_rate": "Usage",
            "avg_velocity": "Avg Velo",
            "whiff_rate": "Whiff",
            "strike_rate": "Strike",
        }
    )

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis("off")
    ax.set_title(
        "Paul Skenes 2025 Pitch Arsenal Summary",
        fontsize=20,
        fontweight="bold",
        pad=24,
    )

    table = ax.table(
        cellText=display_data.values,
        colLabels=display_data.columns,
        cellLoc="center",
        colLoc="center",
        loc="center",
        bbox=[0, 0.08, 1, 0.78],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.8)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#d9e2ec")
        if row == 0:
            cell.set_facecolor("#172033")
            cell.set_text_props(color="white", weight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#f5f7fa")
        else:
            cell.set_facecolor("white")

    fig.text(
        0.5,
        0.02,
        "Data: Statcast via pybaseball | Metrics grouped by pitch type",
        ha="center",
        fontsize=10,
        color="#52606d",
    )
    plt.savefig(OUTPUTS / "skenes_pitch_arsenal_summary.png", dpi=300, bbox_inches="tight")
    plt.close()


df = statcast_pitcher(START_DATE, END_DATE, PLAYER_ID)

cols = [
    "game_date", "pitch_type", "pitch_name", "release_speed",
    "description", "events", "zone", "plate_x", "plate_z",
    "batter", "stand", "p_throws", "balls", "strikes"
]

skenes = df[cols].copy()
skenes = skenes.dropna(subset=["pitch_type", "release_speed"])

pitch_summary = (
    skenes.groupby(["pitch_type", "pitch_name"])
    .agg(
        pitches=("pitch_type", "count"),
        avg_velocity=("release_speed", "mean")
    )
    .reset_index()
)
pitch_summary["usage_rate"] = pitch_summary["pitches"] / pitch_summary["pitches"].sum()
pitch_summary = pitch_summary.sort_values("pitches", ascending=False)

swinging_strikes = ["swinging_strike", "swinging_strike_blocked"]
whiff_summary = (
    skenes.assign(is_whiff=skenes["description"].isin(swinging_strikes))
    .groupby(["pitch_type", "pitch_name"])
    .agg(
        pitches=("pitch_type", "count"),
        whiffs=("is_whiff", "sum"),
        avg_velocity=("release_speed", "mean")
    )
    .reset_index()
)
whiff_summary["whiff_rate"] = whiff_summary["whiffs"] / whiff_summary["pitches"]
whiff_summary = whiff_summary.sort_values("whiff_rate", ascending=False)

strike_descriptions = [
    "called_strike", "swinging_strike", "swinging_strike_blocked",
    "foul", "foul_tip", "foul_bunt", "missed_bunt", "bunt_foul_tip",
    "hit_into_play"
]
strike_summary = (
    skenes.assign(is_strike=skenes["description"].isin(strike_descriptions))
    .groupby(["pitch_type", "pitch_name"])
    .agg(
        pitches=("pitch_type", "count"),
        strikes=("is_strike", "sum"),
        avg_velocity=("release_speed", "mean")
    )
    .reset_index()
)
strike_summary["strike_rate"] = strike_summary["strikes"] / strike_summary["pitches"]
strike_summary = strike_summary.sort_values("strike_rate", ascending=False)

summary_table = (
    pitch_summary.merge(
        whiff_summary[["pitch_type", "pitch_name", "whiff_rate"]],
        on=["pitch_type", "pitch_name"],
    )
    .merge(
        strike_summary[["pitch_type", "pitch_name", "strike_rate"]],
        on=["pitch_type", "pitch_name"],
    )
    .sort_values("pitches", ascending=False)
)

save_bar_chart(
    pitch_summary.sort_values("avg_velocity", ascending=False),
    "pitch_name",
    "avg_velocity",
    "Paul Skenes Average Velocity by Pitch",
    "Average Velocity (mph)",
    "skenes_velocity.png",
)
save_bar_chart(
    whiff_summary,
    "pitch_name",
    "whiff_rate",
    "Paul Skenes Whiff Rate by Pitch",
    "Whiff Rate",
    "skenes_whiff_rate.png",
)
save_bar_chart(
    strike_summary,
    "pitch_name",
    "strike_rate",
    "Paul Skenes Strike Rate by Pitch",
    "Strike Rate",
    "skenes_strike_rate.png",
)
save_summary_table(summary_table)

print("Created chart files:")
print(OUTPUTS / "skenes_velocity.png")
print(OUTPUTS / "skenes_whiff_rate.png")
print(OUTPUTS / "skenes_strike_rate.png")
print(OUTPUTS / "skenes_pitch_arsenal_summary.png")
