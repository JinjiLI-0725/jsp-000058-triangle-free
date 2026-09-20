"""Structural checker regressions; run directly with the repository venv."""
import importlib.util
from itertools import combinations,product
from pathlib import Path
import unittest
import networkx as nx

spec=importlib.util.spec_from_file_location('zero_structure',Path(__file__).resolve().parents[1]/'scripts/analyze_zero_margin.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rspec=importlib.util.spec_from_file_location('restrictions',Path(__file__).resolve().parents[1]/'scripts/audit_zero_restrictions.py')
restrictions=importlib.util.module_from_spec(rspec);rspec.loader.exec_module(restrictions)

def blowup(sizes):
    G=nx.Graph();parts=[];n=0
    for s in sizes:parts.append(list(range(n,n+s)));n+=s
    G.add_nodes_from(range(n))
    for i in range(5):G.add_edges_from(product(parts[i],parts[(i+1)%5]))
    return G

class Checkers(unittest.TestCase):
    def test_blowup(self):
        for sizes in ([1]*5,[3]*5,[1,2,3,1,2]):
            G=blowup(sizes);parts=m.c5_blowup_parts(G)
            self.assertIsNotNone(parts);self.assertEqual(sorted(map(len,parts)),sorted(sizes))
            self.assertIsNotNone(m.c5_homomorphism(G)['mapping'])
        G=blowup([3]*5);G.remove_edge(0,3)
        self.assertIsNone(m.c5_blowup_parts(G))
        self.assertIsNotNone(m.c5_homomorphism(G)['mapping'])
        for G in (nx.path_graph(5),nx.complete_graph(3),nx.empty_graph(5),nx.disjoint_union(nx.cycle_graph(5),nx.empty_graph(1))):
            self.assertIsNone(m.c5_blowup_parts(G))
    def test_homomorphism_against_brute_force(self):
        pairs=list(combinations(range(4),2))
        for mask in range(64):
            G=nx.Graph();G.add_nodes_from(range(4));G.add_edges_from(e for i,e in enumerate(pairs)if mask>>i&1)
            brute=any(all((a[u]-a[v])%5 in (1,4)for u,v in G.edges())for a in product(range(5),repeat=4))
            self.assertEqual(m.c5_homomorphism(G)['mapping']is not None,brute)
        self.assertIsNone(m.c5_homomorphism(nx.mycielskian(nx.cycle_graph(5)))['mapping'])
    def test_shape(self):
        for G,expected in ((nx.path_graph(4),None),(nx.complete_bipartite_graph(2,3),'complete_bipartite'),(nx.empty_graph(5),'independent'),(nx.disjoint_union(nx.path_graph(2),nx.empty_graph(1)),None)):
            adj=[sum(1<<v for v in G[u])for u in G]
            self.assertEqual(m.primitive_shape((1<<len(G))-1,adj),expected)
    def test_twins(self):
        G=blowup([3]*5)
        self.assertEqual(sorted(len(c['vertices'])for c in m.neighborhood_classes(G)),[3]*5)
    def test_restriction_surjectivity(self):
        G=nx.from_graph6_bytes(b'NEL_FF_DgAeOATbBPp?')
        opt=restrictions.optimal_colorings(G)
        self.assertEqual(opt[2],8);self.assertEqual(len(opt[1]),54)
        good=restrictions.restriction_coverage(G,[0,1,2,6,8],opt)
        bad=restrictions.restriction_coverage(G,[0,1,4,10,12],opt)
        self.assertEqual(good['missing_assignments'],[])
        self.assertEqual(bad['missing_assignments'],[14,17])
        self.assertIsNone(m.c5_blowup_parts(G))
        self.assertIsNone(m.c5_homomorphism(G)['mapping'])

if __name__=='__main__':unittest.main()
