import seaborn as sns
import matplotlib.pyplot as plt
import io


def movies_years_histogramm(data):

    years = [d["_id"] for d in data]
    counts = [d["movie_count"] for d in data]

    plt.figure(figsize=(10, 5))
    sns.barplot(x=years, y=counts)

    plt.xticks(rotation=45)
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    plt.close()
    img.seek(0)

    return img
