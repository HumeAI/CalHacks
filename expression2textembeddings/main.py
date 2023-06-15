import numpy as np
import pandas as pd
import openai
from openai.embeddings_utils import get_embedding

from utils import HumeAIConfigs
from utils import OpenAIConfigs
from utils import split_embedding_list as sel 
from Expression2Text import Expression2Text


print("Running Hume AI Expression2TextEmbeddings")

EMOTIONS = (
    HumeAIConfigs.EMOTIONS
)  # Check Hume AI model type for correct list of emotions.

# Generate synthetic input emotions (replace with Hume API output)
INPUT_EMOTIONS = np.random.uniform(0, 1, size=len(EMOTIONS)).reshape(len(EMOTIONS), 1)
print(f"Input emotions shape: {INPUT_EMOTIONS.shape}")

openai.api_key = OpenAIConfigs.API_KEY

# Convert emotion scores to text expressions
PHRASES = [Expression2Text(emotion) for emotion in INPUT_EMOTIONS.T]
PHRASES_JOINED = ", ".join(PHRASES)
RESULT = f"They seem to be {PHRASES_JOINED}."
DICT_RES = {"text_output": [RESULT]}

df = pd.DataFrame.from_dict(DICT_RES)
df["embedding"] = df["text_output"].apply(
    lambda x: get_embedding(x, engine=OpenAIConfigs.MODEL)
)
df = df.apply(sel, axis=1).join(df)
df.drop("embedding", axis=1, inplace=True)
df_ada = df.filter(regex="^emb_")
df_ada.insert(0, "text", df["text_output"])

output_file = f"{HumeAIConfigs.HUME_MODEL_TYPE}_Expression2TextEmbeddings.csv"
df_ada.to_csv(output_file, index=False)
print(f"Output embedding shape {df_ada.shape}")
print(f"File saved as {output_file}")
