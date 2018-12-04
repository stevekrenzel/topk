# TODO In Rust impl, make sure we modify value in place via references
# rather than setting/getting in the hashmap all over again.

class TopK(object):

    def __init__(self):
        self.ordered = []
        self.keys = {}
        self.freqs = {}

    def inc(self, key):
        ordered, keys, freqs = self.ordered, self.keys, self.freqs

        key_index, key_freq = keys.get(key, (None, 0))
        freq_start, freq_count = freqs.get(key_freq, (len(ordered), 0))
        keys[key] = (freq_start, key_freq + 1)

        if key_index is None:
            ordered.append(key)
        elif freq_start != key_index:
            head = ordered[freq_start]
            ordered[freq_start], ordered[key_index] = key, head
            keys[head] = (key_index, key_freq)

        if freq_count > 1:
            freqs[key_freq] = (freq_start + 1, freq_count - 1)
        elif freq_count == 1:
            del freqs[key_freq]

        freq_start, freq_count = freqs.get(key_freq + 1, (freq_start, 0))
        freqs[key_freq + 1] = (freq_start, freq_count + 1)

    def dec(self, key):
        ordered, keys, freqs = self.ordered, self.keys, self.freqs

        if key not in keys: return

        key_index, key_freq = keys.get(key)
        freq_start, freq_count = freqs.get(key_freq)
        freq_end = freq_start + freq_count - 1
        keys[key] = (freq_end, key_freq - 1)

        if freq_end != key_index:
            tail = ordered[freq_end]
            ordered[freq_end], ordered[key_index] = key, tail
            keys[tail] = (key_index, key_freq)

        if freq_count > 1:
            freqs[key_freq] = (freq_start, freq_count - 1)
        elif freq_count == 1:
            del freqs[key_freq]

        if key_freq == 1:
            ordered.pop() # Delete last element
            del keys[key]
        else:
            freq_start, freq_count = freqs.get(key_freq - 1, (freq_end + 1, 0))
            freqs[key_freq - 1] = (freq_start - 1, freq_count + 1)

    def counts(self):
        return dict((x, self.keys[x][1]) for x in self.ordered)

    def __iter__(self):
        return (x for x in self.ordered)
