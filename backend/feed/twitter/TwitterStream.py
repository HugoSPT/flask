__author__ = 'fabiim'

import time
import random

from twython import TwythonStreamer

def search_words():
    with open("/Users/Fabio/Downloads/effectwordnet/EffectWordNet.tff") as f:
        def split_line(x)   :
            return x.split("\t")
        effects_and_words = [(split_line(x)[1], split_line(x)[2].split(",")) for x in f.readlines()]

        positives = []
        negatives = []
        for type_of_effect, words in effects_and_words:
            if type_of_effect == "+Effect":
                positives.extend(words)
            elif type_of_effect == "-Effect":
                negatives.extend(words)

        return (positives, negatives)


class MyStreamer(TwythonStreamer):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret, timeout=300, retry_count=None, retry_in=10,
                 client_args=None, handlers=None, chunk_size=1):
        super(MyStreamer, self).__init__(app_key, app_secret, oauth_token, oauth_token_secret, timeout, retry_count,
                                         retry_in, client_args, handlers, 1000)
        self._n = 0

    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print "Error code: " + str(status_code) + " - " + str(data)
        if status_code == 420:
            time.sleep((2 ** self._n) + (random.randint(0, 1000) / 1000))
            self._n += 1


def main():
    positives, negatives = search_words()

    def word_size(x): return len(x) + 1000 if "_" in x else 0
    positives = sorted(positives, lambda x, y: word_size(x) - word_size(y))
    negatives = sorted(negatives, lambda x, y: word_size(x) - word_size(y))

    positives, negatives = set(positives[:200]), set(negatives[:200])

    trace_words = ",".join(positives) + ",".join(negatives)

    stream = MyStreamer("vYn0ES5AIqaxtl582gcQrfozZ", "S22Tah9Plo4vlJzQ1WgZYt4ML8FoacQ9QMTa1KjvHiZTs3DkMF",
                        "296786432-hI6eoypFeXRYjpKzSo1QMsgoVh1iNC8Qmn2Bgya0",
                        "3vcmBuleaxirMfU3amLDGAIUUQDT0CutAtDoM1De8Xm8t")

    stream.statuses.filter(lang="en", track=trace_words)


if __name__ == '__main__':
    main()