import re

ASPECT_KEYWORDS = {
    "delivery": [
        "late", "delay", "delayed", "slow delivery", "delivery", "arrived late", "fast delivery"
    ],
    "taste": [
        "taste", "tasty", "flavour", "flavor", "delicious", "spicy", "fresh", "quality"
    ],
    "app_issue": [
        "app", "crash", "bug", "error", "login", "ads", "ui", "update", "feature"
    ],
    "service": [
        "behaviour", "behavior", "rude", "polite", "staff", "service"
    ],
    "packaging": [
        "packaging", "leak", "box", "sealed", "packing"
    ],
    "price": [
        "expensive", "cheap", "price", "overprice"
    ],
    "response": [
        "didnt respond", "didn't respond", "no reply", "no response"
    ]
}


def extract_aspect(text):
    text = text.lower()

    for aspect, keywords in ASPECT_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return aspect

    return "other"
