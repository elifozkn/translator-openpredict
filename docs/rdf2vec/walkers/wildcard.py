import itertools

from rdf2vec.graph import Vertex
from rdf2vec.walkers import RandomWalker


class WildcardWalker(RandomWalker):
    def __init__(self, depth, walks_per_graph, wildcards=[1]):
        super().__init__(depth, walks_per_graph)
        self.wildcards = wildcards

    def extract(self, graph, instances):
        canonical_walks = set()
        for instance in instances:
            walks = self.extract_random_walks(graph, Vertex(str(instance)))
            for walk in walks:
                canonical_walks.add(tuple(x.name for x in walk))

                for wildcard in self.wildcards:
                    combinations = itertools.combinations(range(1, len(walk)),
                                                          wildcard)
                    for idx in combinations:
                        new_walk = []
                        for ix, hop in enumerate(walk):
                            if ix in idx:
                                new_walk.append(Vertex('*'))
                            else:
                                new_walk.append(hop.name)
                        canonical_walks.add(tuple(new_walk))
        return canonical_walks
