from time import time
import json
from re import findall
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from sklearn import svm


class DeepTextAnalyzer(object):
    def __init__(self, word2vec_model):
        """
        Construct a DeepTextAnalyzer using the input Word2Vec model
        :param word2vec_model: a trained Word2Vec model
        """
        self._model = word2vec_model

    def txt2vectors(self, txt, is_html):
        """
        Convert input text into an iterator that returns the corresponding vector representation of each
        word in the text, if it exists in the Word2Vec model
        :param txt: input text
        :param is_html: if True, then extract the text from the input HTML
        :return: iterator of vectors created from the words in the text using the Word2Vec model.
        """
        words = txt2words(txt)
        words = [w for w in words if w in self._model]
        if len(words) != 0:
            for w in words:
                yield self._model[w]

    def txt2avg_vector(self, txt, is_html):
        """
        Calculate the average vector representation of the input text
        :param txt: input text
        :param is_html: is the text is a HTML
        :return the average vector of the vector representations of the words in the text
        """
        vectors = self.txt2vectors(txt, is_html=is_html)
        vectors_sum = next(vectors, None)
        if vectors_sum is None:
            return None
        count = 1.0
        for v in vectors:
            count += 1
            vectors_sum = np.add(vectors_sum, v)

        # calculate the average vector and replace +infy and -inf with numeric values
        avg_vector = np.nan_to_num(vectors_sum / count)
        return avg_vector


def txt2words(inputString):
    return findall(r'(?u)\w+', inputString)


def w2v_load_model(fname):
    return KeyedVectors.load_word2vec_format(fname, binary=True)


def load_tweets(fname):
    """Place tweets into a list, loading from a JSON file"""
    tweets = []
    for line in open(fname):
        tweets.append(json.loads(line))
    return tweets


def w2v_vector(dta, text):
    vector = dta.txt2avg_vector(text, is_html=False)
    if vector is None:
        return
    return [0.0 if v is None else str(v) for v in vector]


def load_data():
    """Returns the trained tweets, evaluated tweets, and the w2v model"""
    t = time()
    print 'loading tweets, please wait...'
    trained_tweets = load_tweets('training_dataset')
    eval_tweets = load_tweets('evaluation_dataset')
    print 'Time taken {}'.format(time() - t)
    t = time()
    print 'loading w2v model, please wait...'
    model = w2v_load_model('GoogleNews-vectors-negative300.bin')
    print 'Time taken {}'.format(time() - t)
    return trained_tweets, eval_tweets, model


def build_sf(dta, clf, trained_tweets):
    """Build samples and features arrays and returns them"""
    X = []  # samples
    y = []  # features
    for tweet in trained_tweets:
        vector = w2v_vector(dta, tweet['text'])
        if vector is not None:  # ValueError: setting an array element with a sequence :')
            X.append(vector)
            y.append(tweet['label'])
    return X, y


def predict_and_analyze(dta, clf, eval_tweets):
    """Predict our evaluated tweets then generate the metrics.
    Metrics include True Positives (tp), False Positives (fp),
    True Negatives (tn), False Negatives (fn), Precision, Recall,
    and F1 score
    Returns the metrics as a dictionary."""
    for tweet in eval_tweets:
        tweet['prediction'] = clf.predict([w2v_vector(dta, tweet['text'])])[0]

    metrics = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0,
               'precision': 0, 'recall': 0, 'f1': 0}
    for tweet in eval_tweets:
        actual_label = tweet['label']
        prediction = tweet['prediction']
        if actual_label == prediction:
            if prediction == 'relevant':
                metrics['tp'] += 1
            else:
                metrics['tn'] += 1
        else:
            if prediction == 'relevant':
                metrics['fp'] += 1
            else:
                metrics['fn'] += 1
    metrics['precision'] = float(metrics['tp']) / (metrics['tp'] + metrics['fp'])
    metrics['recall'] = float(metrics['tp']) / (metrics['tp'] + metrics['fn'])
    metrics['f1'] = 2 * ((metrics['precision'] * metrics['recall']) /
                         (metrics['precision'] + metrics['recall']))
    return metrics


def generate_report(metrics, tweets):
    with open('report.txt', 'w') as f:
        f.write('True positives: {}\tFalse positives: {}\tTrue negatives: {}\tFalse negatives: {}\n'.format(
            metrics['tp'], metrics['fp'], metrics['tn'], metrics['fn']))
        f.write('Precision: {}\tRecall: {}\tF1-score: {}\n'.format(
            metrics['precision'], metrics['recall'], metrics['f1']))
        for t in tweets:
            f.write('{}\t{}\n'.format(t['id_str'], t['label']))


if __name__ == '__main__':
    # Load tweets and model
    trained_tweets, eval_tweets, model = load_data()

    dta = DeepTextAnalyzer(model)
    clf = svm.SVC()

    # Get samples and features
    X, y = build_sf(dta, clf, trained_tweets)

    # Classify
    clf.fit(X, y)

    # Retrieve metrics from predictions
    metrics = predict_and_analyze(dta, clf, eval_tweets)

    generate_report(metrics, eval_tweets)

    print 'Check report.txt for results'
