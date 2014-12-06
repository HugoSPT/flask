import ConfigParser
import pickle

__author__ = 'fabiim'

import time
import random

config = ConfigParser.ConfigParser()
config.read('../../../config.cfg')

import backend.feed.util.QueueHandler as QueueHandler
from twython import TwythonStreamer

RABBIT_MQ_IP = config.get("System", "rabbit")
QUEUE_FEED = config.get("Queue", "feed")

def search_words():
    with open("./resources/EffectWordNet.tff") as f:
        def split_line(x):
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
                                         retry_in, client_args, handlers, chunk_size)
        self._n = 0
        self.queue_handler = QueueHandler.RabbitQueueHandler()
        self.publisher = self.queue_handler.pub_register(QUEUE_FEED)

    def on_success(self, data):
        if 'text' in data:
            print(data)
            self.publisher.publish_task(data=pickle.dumps(data), keys=QUEUE_FEED)

    def on_error(self, status_code, data):
        print "Error code: " + str(status_code) + " - " + str(data)
        if status_code == 420:
            time.sleep((2 ** self._n) + (random.randint(0, 1000) / 1000))
            self._n += 1


def run_feed_listener(trace_words):
        stream = MyStreamer("vYn0ES5AIqaxtl582gcQrfozZ", "S22Tah9Plo4vlJzQ1WgZYt4ML8FoacQ9QMTa1KjvHiZTs3DkMF",
                        "296786432-hI6eoypFeXRYjpKzSo1QMsgoVh1iNC8Qmn2Bgya0",
                        "3vcmBuleaxirMfU3amLDGAIUUQDT0CutAtDoM1De8Xm8t")

        stream.statuses.filter(lang="en", track=trace_words)

def main():
    positives, negatives = search_words()

    def word_size(x): return len(x) + 1000 if "_" in x else 0

    positives = sorted(positives, lambda x, y: word_size(x) - word_size(y))
    negatives = sorted(negatives, lambda x, y: word_size(x) - word_size(y))

    positives, negatives = set(positives[:200]), set(negatives[:200])

    trace_words = ",".join(positives) + ",".join(negatives)

    run_feed_listener(trace_words)


        # except Exception:
        #     continue

    # auth = OAuthHandler(ckey, csecret)
    # auth.set_access_token(atoken, asecret)
    # twitterStream = Stream(auth, listener())
    # twitterStream.filter(track=trace_words.split(", "))


if __name__ == '__main__':
    main()