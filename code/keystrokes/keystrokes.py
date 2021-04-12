

class Keystrokes():
    """
    Keystrokes are simply a list of keystroke tuples 
    (keycode, t_down, t_up)
    Where keycode is the integer reported by showkey,
    t_down and t_up are time stamps for when the key was pressed and released.

    Note that Keystrokes are only valid if, for any entry (i, t_down, t_up), if the keycode i
    appears in any subsequent entry (i, t2_down, t2_up), then t2_down >= t_up

    Any entries without t_down or t_up (that were half-logged before or after the recording window)
    are discarded
    """

    def __init__(self, filename):
        self.strokes = Keystrokes._init_from_txt(filename)

    @staticmethod
    def _init_from_txt(filename):
        """
        For our purposes it's easiest to store keylogs in a human readable txt file (since we're not
        doing anything massive). So read keystrokes as line seperated items e.g.
        keycode t_down t_up
        keycode t_down t_up
        ...
        keycode t_down t_up
        where the three items are space separated and all positive integers
        """
        rv = []
        with open(filename, 'r') as f:
            for line in f:
                # this assumes proper format (described in docstring) 
                rv.append(list(map(int, line.strip().split(' '))))
        return rv
    
    @staticmethod
    def write_to_txt(keystrokes, filename):
        """
        Write keystrokes to a txt file (overwritten if existent) in the needed format
        """
        with open(filename, 'w') as f:
            for s in keystrokes:
                f.write(f"{s[0]} {s[1]} {s[2]}\n")

    @staticmethod
    def clean_and_validate(keystrokes):
        """
        Remove any keystrokes without both timestamps, or remove any keystrokes which begin before
        a keystroke of the same key ends (releases)
        """
        pressed_keys = {}
        for i, s in enumerate(keystrokes):
            if s[1] is None or s[2] is None:
                keystrokes.pop(i)
                continue

            # if keycode s[0] has been previously pressed
            if s[0] in pressed_keys:
                # if s[0] is pressed after previously released
                if s[1] >= pressed_keys[s[0]][2]:
                    # update last pressed s[0]
                    pressed_keys[s[0]] = s
                else:
                    # else invalid, so remove s
                    keystrokes.pop(i)
            else:
                pressed_keys[s[0]] = s

class ngrams():

    latencies = {}
    durations = {}
    
    def __init__(self, n, *keystrokes, cutoff=2500):
        """
        calculate the ngrams of a set of keystrokes, where an ngram is
        [{ (k1,k2,...,kn) : [count, mean, variance] }, { ki : count, avg_duration }]
        for a given n (we'll probably stick to digrams)

        These are two collections: 
        - latencies is a mapping from an ordered tuple of n keys
        - count is the frequency of that sequence of keys in the keystrokes
        - mean is the /latency/: the average time between the first key-down and the last key-down
        of the sequence 
        - variance is the sample variance of the latency (the one with denom n - 1)
        
        - durations is a mapping from individual keys to their count and avg_duration. A count is
        kept so that the duration averages (how long the keys are held down) can be updated
        - durations does not depend on n, and we lose some detail in not measuring the duration of
        each key press within the context of its ngram. But I'm not sure how powerful of a biometric
        profile the durations of distinct keys even are.

        cutoff is the number of milliseconds between key_down events to "atomize" keystrokes
        by. That is, if there are more than cutoff milliseconds between two separate key down
        events, we consider that the end of a sequence of typing and stop considering it when
        building ngrams.
        """
        for ks in keystrokes:
            i = 0
            strokes = ks.strokes
            # TODO: clean this mess into
            # i = find_first_ngram()
            # add durations for keys i, i+1, ... , i+n-2
            # do add_ngram while key i+n and i+n-1 within latency cutoff
            # if not done JMP to TODO:
            while i + n <= len(strokes):
                
                # keep a flag if we're starting an ngram chain to avoid overcounting
                # individual key durations within the chain
                fresh = True
                j = i
                # for j = i, i+1, ... i+n-2, find the first n keys where all digram latencies are
                # within the cutoff
                while j + 1 < len(strokes) and j < i + n - 1:
                    # Check that the latency between key j+1 and j is within the cutoff
                    if strokes[j+1][1] - strokes[j][1] > cutoff:
                        # if not, reset i to the next key and restart
                        i = j + 1
                        j = i
                    else:
                        j += 1
                # now we have an ngram within the cutoff, and as long as the next key doesn't break
                # that, we can keep adding ngrams from this sequence to the pool
                while i + n <= len(strokes):
                    # note this looks very nested but it's really just a messy jump
                    self.add_ngram(strokes[i:i+n], fresh)
                    fresh = False

                    # break out of this and "restart" the ngram window if the next key would break
                    # the latency cutoff
                    if i + n < len(strokes) and strokes[i+n][1] - strokes[i+n-1][1] > cutoff:
                        i = i+n
                        break
                    # else move the sliding window over and grab the next ngram
                    i += 1

    def add_ngram(self, keys, fresh):
        """
        keys is a sequence of keystrokes of length n
        fresh is a boolean flag indicating whether to count all durations in the n-gram or only the
        last
        
        performs an online update of the ngram statistics (frequency, mean, sample variance) using
        https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Welford's_online_algorithm
        """
        # first add duration(s), if this ngram is "fresh", add all three durations, else add only
        # the last duration to avoid overcounting any overlapping keys
        for i in ([2],[0,1,2])[fresh]:
            if keys[i][0] not in self.durations:
                self.durations[keys[i][0]] = 1
            else:
                self.durations[keys[i][0]] += 1

        keyseq = tuple([key[0] for key in keys])
        new_latency = keys[-1][1] - keys[0][1]
        if keyseq not in self.latencies:
            self.latencies[keyseq] = [1, new_latency, 0]
        else:
            # find the (unsquared) error from the old mean
            err = new_latency - self.latencies[keyseq][1]
            n = self.latencies[keyseq][0]
            # update the mean
            self.latencies[keyseq][1] += err / (n + 1)
            # update the variance
            var = self.latencies[keyseq][2]
            self.latencies[keyseq][2] = \
                (var * (n - 1) + err * (new_latency - self.latencies[keyseq][1])) / n
            # update the count
            self.latencies[keyseq][0] += 1
        
