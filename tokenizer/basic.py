import regex as re
from hashlib import sha256
from collections import defaultdict


def get_stats(byte_pairs):
    stats = defaultdict(int)
    for pair in byte_pairs.values():
        stats[pair] += 1
    return stats


class BasicTokenizer:
    def __init__(self):
        pass
        # a tokenizer compresses any given input text on the basis of a set of merge rules.
        # the merge rules are derived by training on a large corpus of text.
        # any text given to a tokenizer is converted to unicode,
        # after which a process recursively finds the most common byte pairs and merges them.
    
    def train(self, text, vocab_size, verbose=False):
        try:    # convert input text to byte pairs
            # prepare merge table
            self.bpe_merges = []

            # prepare the vocabulary mapping. id -> string
            self.vocab_size = vocab_size
            self.vocab = defaultdict(int)
            self.inverse_vocab = defaultdict(chr)
            for i in range(256):
                self.vocab[chr(i)] = i
                self.inverse_vocab[i] = chr(i)

            # encode the text to bytes
            text = list(map(int, text.encode('utf-8')))
            
            # prepare the byte pair object for fast lookup and merging.
            byte_pairs = {}
            byte_pair_freq = defaultdict(int)
            next_pair_ids = [i+1 for i in range(len(text)+1)]
            next_pair_ids[-1] = None
            prev_pair_ids = [i-1 for i in range(len(text)+1)]
            prev_pair_ids[0] = None

            # initialize the byte pair object
            for i in range(len(text) - 1):
                pair = tuple(text[i:i+2])
                byte_pairs[i] = pair
                byte_pair_freq[pair] += 1
            
            # train the tokenizer
            for i in range(vocab_size - len(self.vocab)):
                print(f"training tokenizer: {len(self.vocab)+1} / {vocab_size}")
                max_freq = 0
                for pair, freq in byte_pair_freq.items():
                    if freq > max_freq:
                        max_freq = freq
                        max_pair = pair
                print(f'max pair: {max_pair}')
                # add the most frequent pair to the vocabulary mapping
                new_tokenid = len(self.vocab)
                new_token = "".join([self.inverse_vocab[max_pair[0]], self.inverse_vocab[max_pair[1]]])
                self.vocab[new_token] = new_tokenid
                self.inverse_vocab[new_tokenid] = new_token
                # add the most frequent pair to the merge table
                self.bpe_merges.append(max_pair)
                
                # do the merging process iteratively
                print(f'merging process, max pair: {max_pair}, byte_pair_freq: {byte_pair_freq[max_pair]}')
                cur_idx = 0
                assert cur_idx in byte_pairs, f"0 idx is not in byte_pairs"
                while cur_idx in byte_pairs:
                    cur_pair = byte_pairs[cur_idx]
                    next_idx = next_pair_ids[cur_idx]
                    prev_idx = prev_pair_ids[cur_idx]
                    print(f'merging process, cur_idx: {cur_idx}, cur_pair: {cur_pair}, next_idx: {next_idx}, prev_idx: {prev_idx}')
                    # merge the current pair if it is the most common pair
                    if cur_pair == max_pair:
                        print(f'match!')
                        # decrement the frequency of the current pair
                        byte_pair_freq[cur_pair] -= 1
                        if prev_idx is None and next_idx is None:
                            # only one pair exists.
                            assert False, "dont know how to handle this case. lol"
                        if prev_idx is not None:
                            print(f'prev_idx is not None')
                            # prev pair exists and must be reassigned.
                            # decrement the frequency of the previous pair
                            byte_pair_freq[byte_pairs[prev_idx]] -= 1
                            # assign the new pair to the previous pair
                            byte_pairs[prev_idx] = (byte_pairs[prev_idx][0], new_tokenid)
                            # increment the frequency of the new pair
                            byte_pair_freq[byte_pairs[prev_idx]] += 1
                        if next_idx is not None:
                            print(f'next_idx is not None')
                            # next pair exists and must be reassigned.
                            byte_pairs[cur_idx] = (new_tokenid, byte_pairs[next_idx][1])
                            byte_pair_freq[byte_pairs[cur_idx]] += 1
                            byte_pair_freq[byte_pairs[next_idx]] -= 1
                            next_pair_ids[cur_idx] = next_pair_ids[next_idx]
                            byte_pairs.pop(next_idx)
                    cur_idx = next_pair_ids[cur_idx]
                errortext = f"frequency of {max_pair} is not 0 it is {byte_pair_freq[max_pair]}"
                assert byte_pair_freq[max_pair] == 0, errortext
        except Exception as e:
            raise e
            breakpoint()

    def encode(self, text):
        pass

    def decode(self, ids):
        pass



if __name__ == "__main__":
    with open("C://idfk/somebpebullshit/minbpe/tests/taylorswift.txt", "r") as f:
        text = f.read()
    tokenizer = BasicTokenizer()
    tokenizer.train(text, 256+10)
    print(tokenizer.bpe_merges)
    print(tokenizer.vocab)
