# HumeChat Setup and Usage Guide

HumeChat is a powerful chat interface leveraging Hume's emotion detection technology and OpenAI's language model to facilitate engaging, dynamic, and emotion-aware conversations.

## Prerequisites

Ensure that you have the following tools installed on your system:

- Anaconda or Miniconda
- Python 3.8
- pip (included with conda)

## Installation Steps

Follow the steps below to set up and activate a Python environment for HumeChat:

1. `conda create --name humechat python=3.8` (This creates a new conda environment named 'humechat' with Python 3.8)
2. `conda activate humechat` (This activates the 'humechat' environment)

Next, install the required Python packages using the provided `requirements.txt` file:

3. `pip install -r requirements.txt`

4. Make sure you allow access to both your built-in webcam and keyboard inputs.

## Configuration

Before you can use HumeChat, you need to configure your Hume and OpenAI API keys:

1. Open the `main.py` file and replace 'HUME_API_KEY' with your actual Hume API key.
2. Open the `chat.py` file and replace 'openai.api_key' with your actual OpenAI key.

## Usage

To use HumeChat, follow these steps:

1. Run the main script with the command: `python main.py`
2. Press the space bar once to start speaking.
3. Press the space bar again when you're done speaking.

HumeChat will analyze your emotions during your speech and generate a dynamic response based on your emotions.
