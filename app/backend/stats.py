import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import seaborn as sns


def movies_years_histogramm(data):
    years = [d["_id"] for d in data]
    counts = [d["movie_count"] for d in data]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=years, y=counts, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    img = io.BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight")
    plt.close(fig)
    img.seek(0)
    return img


def runtime_vs_revenue_scatter(data):
    runtimes = [d["Runtime (Minutes)"] for d in data]
    revenues = [d["Revenue (Millions)"] for d in data]
    correlation = np.corrcoef(runtimes, revenues)[0, 1]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.regplot(
        x=runtimes,
        y=revenues,
        ax=ax,
        scatter_kws={"alpha": 0.5, "s": 40},
        line_kws={"color": "red", "linewidth": 1.5},
    )
    ax.set_xlabel("Durée (minutes)")
    ax.set_ylabel("Revenus (Millions $)")
    ax.set_title(f"Corrélation durée / revenus  (r = {correlation:.2f})")

    img = io.BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight")
    plt.close(fig)
    img.seek(0)
    return img


def avg_runtime_per_decade_histogramm(data):
    decades = [str(d["decennie"]) + "s" for d in data]
    avg_runtimes = [d["avg_time_length"] for d in data]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=decades, y=avg_runtimes, ax=ax)
    ax.set_xlabel("Décennie")
    ax.set_ylabel("Durée moyenne (minutes)")
    ax.set_title("Durée moyenne des films par décennie")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    img = io.BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight")
    plt.close(fig)
    img.seek(0)
    return img
