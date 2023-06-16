# Hume AI Expressions to Text to Language Embeddings Usage Guide

Our Expressions2Text tool takes emotion scores from the Hume API and transforms them into descriptive text, which can be further transformed into a language embedding. In this example code, we provide functionality for feeding the text-based expression scores to OpenAI's ADA embeddings.

## Prerequisites

Make sure you have the following tools installed on your system:

- Anaconda or Miniconda
- Python 3.9
- pip (included with conda)

## Installation Steps

Follow the steps below to set up and activate a Python environment for HumeE2T:

1. `conda create --name humeE2T python=3.9` (This creates a new conda environment named 'humeE2T' with Python 3.9)
2. `conda activate humeE2T` (This activates the 'humeE2T' environment)

Next, install the required Python packages using the provided `requirements.txt` file:

3. `pip install -r requirements.txt`

## Configuration

To obtain language embeddings from the expressive text, you need to configure the OpenAI API keys:

1. Open the `utils.py` file and replace 'API_KEY' with your actual OpenAI key.

## Usage
1. Replace `url=[]` in `main.py' with your audio location. 
1. Run the main script with the command: `python main.py`

The example uses a single audio file over a grouped prediction. See the [HumeAI SDK](https://github.com/HumeAI/hume-python-sdk) for more details on the various output option. 
