# *Context Tree Weighting*
#
# goals: compression, prediction
#
# keywords: prediction suffix trees, Krichevsky-Trofimov estimator



class WeightedContextTree:

    # Initialize a weighted context tree given a past, a sequence and a depth

    def __init__(self, past, sequence, depth, verbose=False):
        self.alphabet = set(past + sequence)
        self.maxdepth = depth
        self.past = past
        self.sequence = sequence
        self.verbose = verbose
        self.root = self.buildNode("")

    def KT(self, sequence, symbol = None):
        if symbol is None:
            # Compute the probability of 'string' under the KT estimator
            p = 1
            for idx, symbol in enumerate(sequence):
                p *= self.KT(sequence[:idx], symbol)
            return p
        else:
            # Compute the probability assigned to 'symbol'
            occ = sum(map(lambda x: 1 if x == symbol else 0, sequence))
            return (occ + 1.0 / len(self.alphabet)) / (len(sequence) + 1.0)

    def collect(self, context):
        k = len(context)
        string = (past[-k:] + self.sequence) if k > 0 else self.sequence
        result = ""
        for i in range(k, len(string)):
            if string[i-k:i] == context:
                result = result + string[i]
        if self.verbose:
            print("Searched %s in %s and got %s." % (context, string, result))
        return result

    def buildNode(self, context):
        node = {}
        sc = self.collect(context)
        if self.verbose:
            print("%5s -> %s" % (context, sc))
        node["kt"] = self.KT(sc)
        ctw = 1.0
        if len(context) < self.maxdepth:
            for x in self.alphabet:
                node[x] = self.buildNode(x + context)
                ctw *= node[x]["ctw"]
            node["ctw"] = 0.5 * node["kt"] + 0.5 * ctw
        else:
            node["ctw"] = node["kt"]

        node["context"] = context
        return node

    def nodeToString(self, node):
        pattern = "%%%ds -> kt = %%2.5f; ctw = %%2.5f\n" % (self.maxdepth)
        return pattern % (node["context"], node["kt"], node["ctw"])

    def __str__(self, node=None):
        if node is None:
            node = self.root
        s = self.nodeToString(node)
        for symbol in self.alphabet:
            if symbol in node:
                s = s + self.__str__(node[symbol])
        return s

past = "10"
seq = "1011010"
depth = 2
ctw = WeightedContextTree(past, seq, depth, False)

print(ctw)
