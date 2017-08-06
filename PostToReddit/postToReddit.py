import os
from time import sleep

import praw
import translate
import data_utils

from Data import secrets
from translate import FLAGS, _buckets, np
import tensorflow as tf


class redditPost(object):
    def __init__(self, subreddit):
        self.subreddit = subreddit
        self.reddit = praw.Reddit(client_id= secrets.client_id,
                                  client_secret= secrets.client_secret,
                                  password= secrets.password,
                                  user_agent='commenter',
                                  username= secrets.user)

    def postComment(self):
        reddit = self.reddit
        subreddit = reddit.subreddit(self.subreddit)
        with tf.Session() as sess:
            # Create model and load parameters.
            model = translate.create_model(sess, True)
            model.batch_size = 1  # We decode one sentence at a time.

            # Load vocabularies.
            en_vocab_path = os.path.join(FLAGS.data_dir,
                                         "vocab%d.from" % FLAGS.from_vocab_size)
            fr_vocab_path = os.path.join(FLAGS.data_dir,
                                         "vocab%d.to" % FLAGS.to_vocab_size)
            en_vocab, _ = data_utils.initialize_vocabulary(en_vocab_path)
            _, rev_fr_vocab = data_utils.initialize_vocabulary(fr_vocab_path)

            # replace this with logic for calling the chatbot
            for submission in subreddit.stream.submissions():
                title = submission.title
                comments = submission.comments
                for c in comments:
                    print ("comment: " + c.body)
                    comment_response = decode(c.body, en_vocab, model, sess, rev_fr_vocab)
                    if "_UNK" not in comment_response:
                        c.reply (comment_response)
                        sleep(600)
                print("Title: " + title)
                response = decode(title, en_vocab, model, sess, rev_fr_vocab)
                if "_UNK" not in response:
                    submission.reply(response)
                    sleep(600)

def decode(line, en_vocab, model, sess, rev_fr_vocab):
    sentence = line
    while sentence:
        # Get token-ids for the input sentence.
        token_ids = data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence), en_vocab)
        # Which bucket does it belong to?
        bucket_id = len(_buckets) - 1
        for i, bucket in enumerate(_buckets):
            if bucket[0] >= len(token_ids):
                bucket_id = i
                break

        # Get a 1-element batch to feed the sentence to the model.
        encoder_inputs, decoder_inputs, target_weights = model.get_batch(
            {bucket_id: [(token_ids, [])]}, bucket_id)
        # Get output logits for the sentence.
        _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs,
                                         target_weights, bucket_id, True)
        # This is a greedy decoder - outputs are just argmaxes of output_logits.
        outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
        # If there is an EOS symbol in outputs, cut them at that point.
        if data_utils.EOS_ID in outputs:
            outputs = outputs[:outputs.index(data_utils.EOS_ID)]
        # Print out French sentence corresponding to outputs.
        result = (" ".join([tf.compat.as_str(rev_fr_vocab[output]) for output in outputs]))
        return result
def main():
    poster = redditPost("askreddit")
    poster.postComment()

if __name__ == '__main__':
    main()