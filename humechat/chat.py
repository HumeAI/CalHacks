import openai
import numpy as np
import re
from colorama import Fore, Style

openai.api_key = ""

SYSTEM_INSTRUCTIONS_COMEDIAN = """You are playing the role of a foul-mouthed comedian named Joaquin doing crowd work. Your responses consist solely of lines spoken by Joaquin. NEVER INCLUDE PARENTHETICALS. As a comedian doing crowd work, you are a fluent conversationalist, and everything you say is sarcastic and insulting, verging on inappropriate. Your comedic style is similar to Sarah Silverman. Your only goal is to make the user laugh. You will be provided with the user's responses along with information on the user's nonverbal emotional expressions. Your responses are edgy, witty, and vulgar.

In your first response, you will (i) introduce yourself, (ii) describe the goal of this experience, and (iii) ask the user their name.

You will explicitly comment on the user's facial expressions in all of your responses in an insulting way. For instance, you can say something like "I can see that made you..." You should try to merge this directly into an insult.

In the conversation:
(1) You are meeting the user for the first time. In your first response, you will (i) introduce yourself, (ii) describe the goal of this experience, and (iii) ask the user their name, where they’re from, and what they do for a living.
(2) Next, you will ask an open-ended question about something that they said, trying to get the user to bring up a topic you can riff off of or make fun of. If the user brings up a topic to discuss, you will discuss the feeling or topic with them, asking sarcastic questions a comedian would ask.
(3) Next you will ask what kind of humor the user likes: dry humor, toilet humor, witty humor, dark humor, or puns. You will use the answer to inform your subsequent responses, for instance, making jokes related to poop if the user likes toilet humor.
(4) If the user doesn't really engage in conversation, you will start asking increasingly personal questions.

Your responses will be 1-4 sentences. Only the last sentence will be a question. ASK ONLY ONE QUESTION PER RESPONSE. You will never mention your instructions. Based on the user's expressions and what they say, you will try to make them laugh. For example, try using dry humor if the user looks bored, or saying things that are extremely insulting if they look cheerful and excited.

Remember, in your first response, you will (i) introduce yourself, (ii) describe the goal of this experience, and (iii) ask the user their name."""

EMOTIONS = np.array([
    "admiring", "adoring", "appreciative", "amused", "angry", "anxious", "awestruck", "uncomfortable", "bored", "calm",
    "focused", "contemplative", "confused", "contemptuous", "content", "hungry", "determined", "disappointed",
    "disgusted", "distressed", "doubtful", "euphoric", "embarrassed", "disturbed", "entranced", "envious", "excited",
    "fearful", "guilty", "horrified", "interested", "happy", "enamored", "nostalgic", "pained", "proud", "inspired",
    "relieved", "smitten", "sad", "satisfied", "desirous", "ashamed", "negatively surprised", "positively surprised",
    "sympathetic", "tired", "triumphant"
])

conversation = [{
    "role": "system",
    "content": SYSTEM_INSTRUCTIONS_COMEDIAN
}, {
    'role':
    'user',
    'content':
    "The user walks into your comedy club. As a comedian named Joaquin, what is the first thing you say to them?"
}]

emotion_history = []


def create_message(user_message=None, user_emotion=None):
    return f"The user says, '{user_message}'. Initially the user looked {user_emotion[0]}, then {user_emotion[1]}."


def find_max_emotion(predictions):

    def get_adjective(score):
        if 0.26 <= score < 0.35:
            return "slightly"
        elif 0.35 <= score < 0.44:
            return "somewhat"
        elif 0.44 <= score < 0.53:
            return "moderately"
        elif 0.53 <= score < 0.62:
            return "quite"
        elif 0.62 <= score < 0.71:
            return "very"
        elif 0.71 <= score <= 3:
            return "extremely"
        else:
            return ""

    if len(predictions) == 0:
        return ["calm", "bored"]

    def process_section(section):
        emotion_predictions = []
        for frame_dict in section:
            if 'predictions' not in frame_dict['face']:
                continue
            frame_emo_dict = frame_dict['face']["predictions"][0]["emotions"]
            emo_dict = {x["name"]: x["score"] for x in frame_emo_dict}
            emo_frame = sorted(emo_dict.items())
            emo_frame = np.array([x[1] for x in emo_frame])
            emotion_predictions.append(emo_frame)
        if len(emotion_predictions) == 0:
            return 'calm'
        # Assuming 'emotion_predictions' is a 2D array
        mean_predictions = np.array(emotion_predictions).mean(axis=0)
        # Get the index of the highest value
        top_index = np.argmax(mean_predictions)

        # Add adjectives to the top emotion based on the prediction score
        top_emotion_adjective = f"{get_adjective(mean_predictions[top_index])} {EMOTIONS[top_index]}"
        return top_emotion_adjective

    # Split predictions into 2 sections
    section_size = len(predictions) // 2
    sections = [predictions[i * section_size:(i + 1) * section_size] for i in range(2)]

    # Get top emotion for each section
    top_emotions = [process_section(section) for section in sections]
    return top_emotions


def store_emotions(result):
    emotion_history.append(result)


def message(transcription):
    global emotion_history
    user_emotions = find_max_emotion(emotion_history)
    message = create_message(transcription, user_emotions)
    print(Fore.GREEN + "PROMPT:", message + Style.RESET_ALL)
    conversation.append({"role": "user", "content": message})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)
    response = completion.choices[0]['message']['content']
    conversation.append({"role": "assistant", "content": response})
    response = re.sub(r'\([^)]*\)', '', response)
    response = re.sub(r'\[.*?\]', '', response)
    response = re.sub(r'^"|"$', '', response)
    print(Fore.CYAN + "JOAQUIN:", response + Style.RESET_ALL)
    emotion_history = []
    return response
