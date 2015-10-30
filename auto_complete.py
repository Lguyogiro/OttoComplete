class AutoCompleter(object):
    """
    Simple implementation of a trie for auto-complete, in python.
    Functionality:
        -insert a word into dictionary
        -check if the dict contains your word
        -given a prefix, suggest autocompletes, ranked by frequency of selection
        -select a word given a prefix
        -get count of words in dictionary
    """
    def __init__(self, end_token='<end>'):
        self.trie = dict()
        self.end_token = end_token
        self.count = 0

    def insert(self, *words):
        for word in words:
            self.count += 1
            current_dict = self.trie
            for letter in word:
                current_dict = current_dict.setdefault(letter, {})
            current_dict[self.end_token] = {}

    def contains(self, word):
        root = self.trie
        for char in word:
            if char in root:
                root = root[char]
            else:
                return False
        return True

    def suggest(self, prefix):
        words = []

        def nest(d, nested_prefix):
            for char in d:
                if char == self.end_token:
                    if prefix not in d[char]:
                        d[char][prefix] = 1
                    words.append((nested_prefix, d[char][prefix]))
                else:
                    new_prefix = nested_prefix + char
                    nest(d[char], new_prefix)

        root = self.trie
        for char in prefix:
            if char in root:
                root = root[char]
        for char in root.keys():
            nested_prefix = prefix
            nested_prefix += char
            nest(root[char], nested_prefix)
        return [w[0] for w in sorted([w for w in words],
                                     key=lambda t: t[1],
                                     reverse=True)]

    def select(self, prefix, word):
        if not self.contains(word):
            return "Word not in dictionary"
        root = self.trie
        for char in word:
            root = root[char]
        if prefix in root[self.end_token]:
            root[self.end_token][prefix] += 1
        else:
            root[self.end_token][prefix] = 1

if __name__ == '__main__':
    import time
    c = AutoCompleter()
    words = [word.strip('\n') for word in open('/usr/share/dict/words', 'r')]
    start = time.time()
    c.insert(*words)
    print "Insert took %s seconds" % (time.time() - start)
    words = c.suggest("piz")
    print words
    c.select("piz", words[-1])
    print c.suggest("piz")

