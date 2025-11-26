# eq_engine.py — FINAL VERSION (Balanced + Accurate)

from transformers import pipeline
from functools import lru_cache
import numpy as np


# --------------------------
# 1. Load models only once
# --------------------------

@lru_cache(maxsize=1)
def sentiment_model():
    return pipeline("sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    truncation=True)


@lru_cache(maxsize=1)
def emotion_model():
    return pipeline("text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base",
                    top_k=None,
                    truncation=True)


# --------------------------
# 2. Final EQ Engine
# --------------------------

class EQEngine:

    EMOTION_TO_EQ = {
        "joy":     {"self_awareness": 0.40, "motivation": 0.45, "social_skills": 0.40},
        "neutral": {"self_awareness": 0.20},
        "surprise": {"self_awareness": 0.10},

        "sadness": {"motivation": -0.10, "self_awareness": +0.10},
        "fear": {"emotional_regulation": -0.20},
        "disgust": {"social_skills": -0.30},
        "anger": {"conflict_resolution": -0.35, "emotional_regulation": -0.35},
    }

    BASE_SCORES = {
        "self_awareness": 60,
        "emotional_regulation": 60,
        "empathy": 60,
        "conflict_resolution": 60,
        "motivation": 60,
        "social_skills": 60,
    }

    LOW_EQ_PATTERNS = {
        "emotional_regulation": ["irritated", "angry", "frustrated", "react quickly"],
        "empathy": ["don't care", "don't bother", "not my job"],
        "conflict_resolution": ["not my problem", "do it my way", "handle it themselves"],
        "social_skills": ["don't want to talk", "avoid discussion", "fight"]
    }

    HIGH_EQ_PATTERNS = {
        "emotional_regulation": ["stay calm", "regulate", "steady tone", "manage my emotions"],
        "empathy": ["understand their perspective", "empathy", "validate", "active listening"],
        "conflict_resolution": ["collaboration", "shared goals", "compromise", "resolve"],
        "social_skills": ["respectful", "communication", "open tone"],
    }

    def validate(self, text):
        w = len(text.split())
        if w < 5:
            return -0.10
        if w < 10:
            return -0.05
        return 0.0

    def analyze_text(self, text):
        s_model = sentiment_model()
        e_model = emotion_model()

        sentiment = s_model(text[:512])[0]
        polarity = sentiment["score"] if sentiment["label"] == "POSITIVE" else -sentiment["score"]

        emotions = e_model(text[:512])[0]
        top = sorted(emotions, key=lambda x: x["score"], reverse=True)[0]

        return polarity, top["label"], top["score"]

    def compute(self, responses):
        scores = self.BASE_SCORES.copy()
        total_qp = 0

        for text in responses:
            polarity, emotion, intensity = self.analyze_text(text)
            lower = text.lower()

            # sentiment boosts
            scores["empathy"] += polarity * 8
            scores["social_skills"] += polarity * 6
            scores["conflict_resolution"] += polarity * 5
            scores["emotional_regulation"] += polarity * 5

            # emotion boosts
            if emotion in self.EMOTION_TO_EQ:
                for cat, weight in self.EMOTION_TO_EQ[emotion].items():
                    scores[cat] += weight * (intensity * 50)

            # pattern penalties
            for cat, words in self.LOW_EQ_PATTERNS.items():
                if any(w in lower for w in words):
                    scores[cat] -= 10

            # pattern BOOSTS for high EQ
            for cat, words in self.HIGH_EQ_PATTERNS.items():
                if any(w in lower for w in words):
                    scores[cat] += 8

            # quality
            total_qp += self.validate(text)

        # apply quality
        for k in scores:
            scores[k] *= (1 + total_qp)

        # clamp
        for k in scores:
            scores[k] = int(min(100, max(0, scores[k])))

        scores["overall"] = int(np.mean(list(scores.values())))
        return scores