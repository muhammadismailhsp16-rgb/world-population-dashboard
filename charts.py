"""
charts.py — Chart / visualization functions using Matplotlib & Seaborn
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import pandas as pd

# ─── Consistent color palette ────────────────────────────────────────────────
PRIMARY   = "#1A5276"
ACCENT    = "#2E86C1"
HIGHLIGHT = "#F39C12"
SOFT_BG   = "#EBF5FB"
PALETTE   = ["#1A5276", "#2E86C1", "#5DADE2", "#85C1E9", "#AED6F1",
             "#D6EAF8", "#F39C12", "#E67E22", "#E74C3C", "#1ABC9C"]

sns.set_theme(style="whitegrid", palette=PALETTE)
plt.rcParams.update({
    "font.family":    "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})


def _fig(w=8, h=5):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("white")
    ax.set_facecolor(SOFT_BG)
    return fig, ax


# 1. Pie Chart ─────────────────────────────────────────────────────────────────
def pie_chart(df: pd.DataFrame):
    data = df.groupby("pop_category", observed=True)["population_2020"].sum()
    data = data[data > 0]
    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(
        data, labels=data.index, autopct="%1.1f%%",
        colors=PALETTE[:len(data)], startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=1.5)
    )
    for t in autotexts:
        t.set_fontsize(9)
    ax.set_title("Population Share by Country Size Category", fontweight="bold", pad=15)
    plt.tight_layout()
    return fig


# 2. Histogram ────────────────────────────────────────────────────────────────
def histogram(df: pd.DataFrame):
    fig, ax = _fig()
    sns.histplot(df["population_2020"], bins=30, color=ACCENT, edgecolor="white",
                 ax=ax, kde=True, line_kws={"color": HIGHLIGHT, "lw": 2})
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.0f}M"))
    ax.set_title("Population Distribution (Frequency Histogram)", fontweight="bold")
    ax.set_xlabel("Population (2020)")
    ax.set_ylabel("Number of Countries")
    plt.tight_layout()
    return fig


# 3. Line Chart ───────────────────────────────────────────────────────────────
def line_chart(df: pd.DataFrame):
    top = df.nlargest(15, "population_2020")[["country", "population_2020",
                                               "yearly_change"]].sort_values("population_2020")
    fig, ax = _fig(9, 5)
    ax.plot(top["country"], top["yearly_change"], marker="o", color=ACCENT,
            linewidth=2, markersize=7, markerfacecolor=HIGHLIGHT)
    ax.axhline(0, color="red", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.set_title("Yearly Population Change % — Top 15 Countries by Population", fontweight="bold")
    ax.set_xlabel("Country")
    ax.set_ylabel("Yearly Change (%)")
    plt.xticks(rotation=40, ha="right")
    plt.tight_layout()
    return fig


# 4. Bar Chart ────────────────────────────────────────────────────────────────
def bar_chart(df: pd.DataFrame):
    top = df.nlargest(15, "population_2020")
    fig, ax = _fig(10, 5)
    bars = ax.barh(top["country"], top["population_2020"] / 1e6,
                   color=PALETTE[:len(top)], edgecolor="white")
    ax.set_title("Top 15 Most Populous Countries (2020)", fontweight="bold")
    ax.set_xlabel("Population (Millions)")
    ax.set_ylabel("Country")
    for bar in bars:
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():.0f}M", va="center", fontsize=8)
    plt.tight_layout()
    return fig


# 5. Scatter Plot ─────────────────────────────────────────────────────────────
def scatter_plot(df: pd.DataFrame):
    sub = df.dropna(subset=["fertility_rate", "median_age"])
    fig, ax = _fig()
    sc = ax.scatter(sub["fertility_rate"], sub["median_age"],
                    c=sub["population_2020"], cmap="Blues",
                    s=80, edgecolors="white", linewidth=0.5, alpha=0.85)
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Population (2020)", fontsize=9)
    cbar.formatter = mticker.FuncFormatter(lambda x, _: f"{x/1e6:.0f}M")
    cbar.update_ticks()
    ax.set_title("Fertility Rate vs Median Age", fontweight="bold")
    ax.set_xlabel("Fertility Rate")
    ax.set_ylabel("Median Age")
    plt.tight_layout()
    return fig


# 6. Box Plot ─────────────────────────────────────────────────────────────────
def box_plot(df: pd.DataFrame):
    sub = df.dropna(subset=["median_age"])
    fig, ax = _fig(9, 5)
    order = ["<1M", "1M–10M", "10M–50M", "50M–100M", "100M–500M", ">500M"]
    order = [o for o in order if o in sub["pop_category"].values]
    sns.boxplot(data=sub, x="pop_category", y="median_age",
                order=order, hue="pop_category", palette=PALETTE[:len(order)], ax=ax,
                width=0.5, flierprops=dict(marker="o", color=HIGHLIGHT, markersize=5),
                legend=False)
    ax.set_title("Median Age Distribution by Country Population Category", fontweight="bold")
    ax.set_xlabel("Population Category")
    ax.set_ylabel("Median Age")
    plt.xticks(rotation=15)
    plt.tight_layout()
    return fig


# 7. Heatmap ──────────────────────────────────────────────────────────────────
def heatmap(df: pd.DataFrame):
    num_cols = ["population_2020", "yearly_change", "density_km2",
                "land_area_km2", "fertility_rate", "median_age",
                "urban_pop_pct", "world_share"]
    corr = df[num_cols].dropna().corr()
    labels = ["Population", "Yearly Δ%", "Density", "Land Area",
              "Fertility", "Med Age", "Urban%", "World Share"]
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues",
                xticklabels=labels, yticklabels=labels,
                ax=ax, square=True, linewidths=0.5,
                annot_kws={"size": 8})
    ax.set_title("Feature Correlation Heatmap", fontweight="bold", pad=12)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    return fig


# 8. Area Chart ───────────────────────────────────────────────────────────────
def area_chart(df: pd.DataFrame):
    top = df.nlargest(10, "population_2020").sort_values("population_2020")
    cumulative = top["population_2020"].cumsum() / 1e6
    fig, ax = _fig(9, 5)
    ax.fill_between(range(len(top)), cumulative, color=ACCENT, alpha=0.35)
    ax.plot(range(len(top)), cumulative, color=PRIMARY, linewidth=2, marker="o",
            markersize=6, markerfacecolor=HIGHLIGHT)
    ax.set_xticks(range(len(top)))
    ax.set_xticklabels(top["country"], rotation=35, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}M"))
    ax.set_title("Cumulative Population — Top 10 Countries", fontweight="bold")
    ax.set_xlabel("Country (Ordered by Population)")
    ax.set_ylabel("Cumulative Population (Millions)")
    plt.tight_layout()
    return fig


# 9. Count Plot ───────────────────────────────────────────────────────────────
def count_plot(df: pd.DataFrame):
    fig, ax = _fig(8, 5)
    order = ["<1M", "1M–10M", "10M–50M", "50M–100M", "100M–500M", ">500M"]
    order = [o for o in order if o in df["pop_category"].values]
    sns.countplot(data=df, x="pop_category", order=order, hue="pop_category",
                  palette=PALETTE[:len(order)], ax=ax, edgecolor="white", legend=False)
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())}",
                    (p.get_x() + p.get_width() / 2, p.get_height() + 0.3),
                    ha="center", fontsize=9)
    ax.set_title("Number of Countries by Population Category", fontweight="bold")
    ax.set_xlabel("Population Category")
    ax.set_ylabel("Count of Countries")
    plt.tight_layout()
    return fig


# 10. Violin Plot ─────────────────────────────────────────────────────────────
def violin_plot(df: pd.DataFrame):
    sub = df.dropna(subset=["urban_pop_pct"])
    fig, ax = _fig(8, 5)
    sns.violinplot(data=sub, x="migration_dir", y="urban_pop_pct",
                   hue="migration_dir",
                   palette={"Positive": PALETTE[0],
                             "Negative": PALETTE[8],
                             "Neutral/Unknown": PALETTE[6]},
                   ax=ax, inner="box", cut=0, legend=False)
    ax.set_title("Urban Population % by Migration Direction", fontweight="bold")
    ax.set_xlabel("Net Migration Direction")
    ax.set_ylabel("Urban Population (%)")
    plt.tight_layout()
    return fig
