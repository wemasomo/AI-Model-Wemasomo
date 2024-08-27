import string
from main_local import prompt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def cleaning(prompt):

    # Basic cleaning
    question = prompt.strip() ## remove whitespaces
    question = question.lower() ## lowercase
    question = ''.join(char for char in question if not char.isdigit()) ## remove numbers

    # Advanced cleaning
    for punctuation in string.punctuation:
        question = question.replace(punctuation, '') ## remove punctuation

    tokenized_sentence = word_tokenize(question) ## tokenize
    stop_words = set(stopwords.words('english')) ## define stopwords

    tokenized_sentence_cleaned = [ ## remove stopwords
        w for w in tokenized_sentence if not w in stop_words
    ]

    lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "v")
        for word in tokenized_sentence_cleaned
    ]

    cleaned_sentence = ' '.join(word for word in lemmatized)

    return cleaned_sentence


def response_logic():
    question_keywords = prompt.apply(cleaning)

    if question_keywords etcetcetc:
        return












# def question_keyword():
#   get prompt (user input),
#   remove stopwords,
#   extract keywords
#   compare keywords with keywords from the text database
#   if keyword match is succesful:
#       return summary + link
#       and return question: does that answer your question?
#           if yes: return "Good reading"
#           else: show 2 extra articles
#   else:
#       return "We couldnt understand your question.
#       You can ask a different question or browse through these topics (buttons to 10 categories)"

# st.link_button("Cancer", "https://www.wemasomo.com/explore/cancer")
# st.link_button("Contraception", "https://www.wemasomo.com/explore/contraception")
# st.link_button("Endometriosis", "https://www.wemasomo.com/explore/endometriosis")
# st.link_button("Sexually Transmitted Diseases", "https://www.wemasomo.com/explore/hiv")
# st.link_button("Male Specific Content", "https://www.wemasomo.com/explore/male%20specific%20content")
# st.link_button("Menstruation", "https://www.wemasomo.com/explore/menstruation")
# st.link_button("Mpox", "https://www.wemasomo.com/explore/mpox")
# st.link_button("Parenting", "https://www.wemasomo.com/explore/parenting")
# st.link_button("Pregnancy", "https://www.wemasomo.com/explore/pregnancy-guide")
# st.link_button("Vaccination", "https://www.wemasomo.com/explore/vaccination")
