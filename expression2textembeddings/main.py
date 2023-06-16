import numpy as np
import pandas as pd
import openai
from openai.embeddings_utils import get_embedding

from utils import HumeAIConfigs, OpenAIConfigs, split_embedding_list as sel
from Expression2Text import Expression2Text
from hume import HumeBatchClient
from hume.models.config import ProsodyConfig
from hume import TranscriptionConfig

# Initialize Hume Batch Client
client = HumeBatchClient(HumeAIConfigs.API_KEY)

# Define input data location
urls = ["https://storage.googleapis.com/hume-test-data/audio/ninth-century-laugh.mp3"]

# Configure prosody and transcription settings
prosody_config = ProsodyConfig()
transcription_config = TranscriptionConfig(language="en")

# Submit job to Hume API
job = client.submit_job(urls, [prosody_config])

print("Running the Hume API ...", job)

# Wait for job completion
job.await_complete()

print("Job completed with status:", job.get_status())

# Retrieve predictions from job
full_predictions = job.get_predictions()

# Extract relevant predictions
predictions = full_predictions[0]['results']['predictions'][0]['models']['prosody']['grouped_predictions'][0]['predictions'][0]

# Extract transcription and emotions
transcription = predictions['text']
emotions = predictions['emotions']

# Extract emotion names and scores
emotion_names = [value['name'] for value in emotions]
emotion_scores = [value['score'] for value in emotions]

# Reshape emotion scores for input
INPUT_EMOTIONS = np.array(emotion_scores).reshape(len(emotion_names), 1)

print()
print(f"Input emotions shape: {INPUT_EMOTIONS.shape}")

# Set OpenAI API key
openai.api_key = OpenAIConfigs.API_KEY

print()
print("Transforming emotion scores to description language")

# Convert emotion scores to text expressions
PHRASES = [Expression2Text(emotion) for emotion in INPUT_EMOTIONS.T]
PHRASES_JOINED = ", ".join(PHRASES)
RESULT = f"They said '{transcription}' and they sounded {PHRASES_JOINED}."
DICT_RES = {"text_output": [RESULT]}

print()
print("Expression2Text result:")
print(f"{RESULT}")
print()
print("Extracting language embedding with OpenAI")

# Create DataFrame for results
df = pd.DataFrame.from_dict(DICT_RES)

# Calculate embeddings using OpenAI
df["embedding"] = df["text_output"].apply(lambda x: get_embedding(x, engine=OpenAIConfigs.MODEL))

# Select desired columns and join with original DataFrame
df = df.apply(sel, axis=1).join(df)
df.drop("embedding", axis=1, inplace=True)

# Filter for relevant columns
df_ada = df.filter(regex="^emb_")
df_ada.insert(0, "text", df["text_output"])

# Save output to CSV file
output_file = f"{HumeAIConfigs.HUME_MODEL_TYPE}_Expression2TextEmbeddings.csv"
df_ada.to_csv(output_file, index=False)
print(f"Output embedding shape: {df_ada.shape}")
print(f"File saved as: {output_file}")