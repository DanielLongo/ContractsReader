from sklearn.feature_extraction.text import CountVectorizer


def count_vectorizer(text, max_features=5000):
    text = " ".join(text)
    # text = " ".join(" ".join(x) for x in text)
    # text = [item for sublist in text for item in sublist]
    vectoizer = CountVectorizer(max_features=max_features)
    vectoizer.fit([text])
    return vectoizer
