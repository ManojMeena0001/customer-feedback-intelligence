print("DEBUG: cleaner.py is executing...")
import re
import html
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load stopwords for aggressive cleaning
STOP_WORDS = set(stopwords.words("english"))


def clean_text_basic(text):
    """
    Light cleaning: best for BERT, embeddings, BERTopic.
    Keeps meaning.
    """

    # convert to string if not already
    if not isinstance(text, str):
        text = str(text)

    # convert HTML symbols: &amp; -> &
    text = html.unescape(text)

    # remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # remove @mentions and #hashtags
    text = re.sub(r"[@#]\w+", "", text)

    # remove unwanted symbols (keep letters, numbers, basic punctuation)
    text = re.sub(r"[^a-zA-Z0-9\s\.\,\!\?]", " ", text)

    # lowercase
    text = text.lower()

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def clean_text_aggressive(text):
    """
    Strong cleaning: removes stopwords, punctuation, etc.
    Good for rule-based processing.
    """

    if not isinstance(text, str):
        text = str(text)

    text = html.unescape(text)
    text = text.lower()

    # remove urls
    text = re.sub(r"http\S+|www\S+", "", text)

    # keep only letters & spaces
    text = re.sub(r"[^a-z\s]", " ", text)

    # tokenize
    words = word_tokenize(text)

    # remove stopwords
    words = [w for w in words if w not in STOP_WORDS]

    return " ".join(words)

