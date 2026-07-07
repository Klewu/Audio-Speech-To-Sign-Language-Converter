import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from django.contrib.staticfiles import finders

def process_text(text):
    text = text.lower()
    words = word_tokenize(text)
    tagged = nltk.pos_tag(words)

    tense = {
        "future": len([word for word in tagged if word[1] == "MD"]),
        "present": len([word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]]),
        "past": len([word for word in tagged if word[1] in ["VBD", "VBN"]]),
        "present_continuous": len([word for word in tagged if word[1] in ["VBG"]])
    }

    # Use NLTK stopwords instead of hardcoded list
    stop_words = set(stopwords.words('english'))

    lr = WordNetLemmatizer()
    filtered_text = []

    for w, p in zip(words, tagged):
        if w not in stop_words:
            if p[1] in ['VBG', 'VBD', 'VBZ', 'VBN', 'NN']:
                filtered_text.append(lr.lemmatize(w, pos='v'))
            elif p[1] in ['JJ', 'JJR', 'JJS', 'RBR', 'RBS']:
                filtered_text.append(lr.lemmatize(w, pos='a'))
            else:
                filtered_text.append(lr.lemmatize(w))

    # Add the specific word to specify tense
    temp = []
    for w in filtered_text:
        if w.lower() == 'i':
            temp.append('Me')
        else:
            temp.append(w.capitalize())

    words = temp
    probable_tense = max(tense, key=tense.get)

    if probable_tense == "past" and tense["past"] >= 1:
        words = ["Before"] + words
    elif probable_tense == "future" and tense["future"] >= 1:
        if "Will" not in words:
            words = ["Will"] + words
    elif probable_tense == "present":
        if tense["present_continuous"] >= 1:
            words = ["Now"] + words

    final_words = []
    for w in words:
        path = w + ".mp4"
        f = finders.find(path)
        # Split the word if its animation is not present in database
        if not f:
            for c in w:
                final_words.append(c.upper())
        else:
            final_words.append(w)

    return final_words
