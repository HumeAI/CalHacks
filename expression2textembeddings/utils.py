import pandas as pd


class OpenAIConfigs:
    API_KEY = ""
    MODEL = "text-embedding-ada-002"


class HumeAIConfigs:
    API_KEY = ""
    HUME_MODEL_TYPE = "Prosmimic"

    EMOTIONS = [
        "Admiration",
        "Adoration",
        "Aesthetic Appreciation",
        "Amusement",
        "Anger",
        "Anxiety",
        "Awe",
        "Awkwardness",
        "Boredom",
        "Calmness",
        "Concentration",
        "Contemplation",
        "Confusion",
        "Contempt",
        "Contentment",
        "Craving",
        "Determination",
        "Disappointment",
        "Disgust",
        "Distress",
        "Doubt",
        "Ecstasy",
        "Embarrassment",
        "Empathic Pain",
        "Entrancement",
        "Envy",
        "Excitement",
        "Fear",
        "Guilt",
        "Horror",
        "Interest",
        "Joy",
        "Love",
        "Nostalgia",
        "Pain",
        "Pride",
        "Realization",
        "Relief",
        "Romance",
        "Sadness",
        "Satisfaction",
        "Desire",
        "Shame",
        "Surprise (negative)",
        "Surprise (positive)",
        "Sympathy",
        "Tiredness",
        "Triumph",
    ]


def split_embedding_list(row):
    values = pd.Series(row["embedding"])
    return pd.Series(values.values, index=[f"emb_{i}" for i in range(len(values))])
