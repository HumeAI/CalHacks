import numpy as np


def Expression2Text(emotion_scores):
    emotion_ranges = [
        (0.26, 0.35),
        (0.35, 0.44),
        (0.44, 0.53),
        (0.53, 0.62),
        (0.62, 0.71),
        (0.71, 10),
    ]
    adverbs = ["slightly", "somewhat", "moderately", "quite", "very", "extremely"]

    adjectives = [
        "admiring",
        "adoring",
        "appreciative",
        "amused",
        "angry",
        "anxious",
        "awestruck",
        "uncomfortable",
        "bored",
        "calm",
        "focused",
        "contemplative",
        "confused",
        "contemptuous",
        "content",
        "hungry",
        "determined",
        "disappointed",
        "disgusted",
        "distressed",
        "doubtful",
        "euphoric",
        "embarrassed",
        "disturbed",
        "entranced",
        "envious",
        "excited",
        "fearful",
        "guilty",
        "horrified",
        "interested",
        "happy",
        "enamored",
        "nostalgic",
        "pained",
        "proud",
        "inspired",
        "relieved",
        "smitten",
        "sad",
        "satisfied",
        "desirous",
        "ashamed",
        "negatively surprised",
        "positively surprised",
        "sympathetic",
        "tired",
        "triumphant",
    ]

    if all(emotion_score < emotion_ranges[0][0] for emotion_score in emotion_scores):
        expression_text = "neutral"
    else:
        phrases = [""] * len(emotion_scores)
        for i, (range_min, range_max) in enumerate(emotion_ranges):
            indices = [
                index
                for index, emotion_score in enumerate(emotion_scores)
                if range_min < emotion_score < range_max
            ]
            for index in indices:
                phrases[index] = f"{adverbs[i]} {adjectives[index]}"

        sorted_indices = np.argsort(emotion_scores)[::-1]
        phrases = [phrases[i] for i in sorted_indices if phrases[i] != ""]

        if len(phrases) > 1:
            expression_text = ", ".join(phrases[:-1]) + ", and " + phrases[-1]
        else:
            expression_text = phrases[0]

    return expression_text
