"""Build the corrected report and final hash manifest from completed artifacts."""
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('output',type=Path);p.add_argument('--report',type=Path,required=True);a=p.parse_args();out=a.output.resolve();report=a.report.resolve()
 data=json.loads((out/'summary.json').read_text());verified=json.loads((out/'independent_witnesses.json').read_text())
 assert [r['name']for r in data['rows']]==[r['name']for r in verified['records']]
 assert not report.exists() and not (out/'manifest.json').exists()
 lines=['# Corrected fixed n=15 selection audit','',
 'The previous selection-audit pass is invalid evidence. This report uses a fresh run of a corrected auditor; it does not reuse previous pass records.','',
 'The audited family is exactly independent induced subgraphs, complete bipartite induced subgraphs with two nonempty sides, and complements in H. Complements are explicitly permitted in section B of `notes/COORDINATED_FLIP_SELECTION.md`. General bipartite induced subgraphs are not included unless their complements qualify.','',
 'For every X, the auditor computes U = min over optimal core colorings c of the average over all optimal assignments a on X of min over allowed S of [b_G(c^S union a)-d(H)]. Thus M=5-U, exactly the margin in the selection note. Core reversal is quotiented in the audit; assignments include both orientations. The allowed family is closed under complementation.','',
 'Margins use integer numerator/denominator pairs. The C++ maximum uses cross-multiplication, and the reporting driver uses Python Fraction. All vertex labels below are zero-based; witness files translate local core masks to original labels.','',
 f"Completed: **{data['graphs_completed']} graphs, {data['five_sets']} five-sets**; exactly 3,003 distinct five-sets per completed graph. The fixed input has 24 distinct labeled graphs: the d=8 witness, B3, and 22 supplied non-balanced d=7 canonical representatives. Canonical completeness outside the supplied file is not claimed.",'',
 '| Graph | Max M | First maximizing X | Smallest positive M | Closest negative M | Pass |',
 '|---|---:|---|---:|---:|---|']
 def margin(r):return r['margin']if r else 'none'
 for r in data['rows']:
  lines.append(f"| {r['name']} | {r['max_margin']} | {r['maximizer']['X']} | {margin(r['smallest_positive'])} | {margin(r['closest_negative'])} | {'yes' if r['passes'] else 'NO'} |")
 b3=next((r for r in data['rows']if r['name']=='B3'),None)
 lines+=['',f"B3: all {b3['zero_margin_transversals']} transversals have margin exactly 0." if b3 else 'B3 not reached because of an earlier counterexample.','']
 failures=[r for r in data['rows']if not r['passes']]
 lines+=['First counterexample: '+(json.dumps(failures[0])if failures else 'none in the completed fixed corpus.'),'',
 'Regression tests reject P4, 2K2, an edge plus an isolated vertex, and a triangle as primitive shapes; accept independent sets and K(2,3); and distinguish an invalid shape with an allowed complement from a set with neither side allowed. A separate partition-enumeration predicate agrees for all 32 subsets of all 1,024 labeled five-vertex graphs (32,768 checks). Rational tests cover positive, negative, and tied fractions with unequal denominators, including 2/2 > 8/10.','',
 'Independent verification uses NetworkX connected bipartiteness plus the complete edge-count condition, and enumerates full-graph coloring costs directly in original labels. For each graph it checks a maximum-margin witness, the smallest positive and closest negative witnesses when present, and a minimum-margin witness, including both orientations of every optimal core coloring. It records every maximizing allowed flip for each optimal X assignment at the chosen base coloring. This is independent witness verification, not a second independent exhaustive audit of every X.','',
 'Artifacts: `all_X.tsv` contains every margin and selected base coloring; `summary.json` contains graph6 strings, all maximizing X, exact extrema, and input/source hashes; `independent_witnesses.json` contains original-label colorings and all assignment-wise maximizing flip sets for the selected extrema. `manifest.json` hashes all sources, tests, relevant notes, binaries, and output files, including this report.','',
 'Reproduce in a fresh output directory (the driver refuses existing directories):','',
 '```sh',
 'PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python scripts/audit_selection_exact.py --output results/selection_exact_reproduction',
 'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/verify_selection_exact.py results/selection_exact_reproduction',
 'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/report_selection_exact.py results/selection_exact_reproduction --report notes/SELECTION_AUDIT_REPRODUCTION.md',
 '```','',
 'Scope: this is an exhaustive audit of the specified fixed corpus only. It proves neither the universal structural selection conjecture nor Candidate A. No random search or further proof attempt was made. The protected PID 3132683 and results/candidate_A_n20_large were not modified.']
 report.write_text('\n'.join(lines)+'\n')
 files=[ROOT/'scripts/audit_selection_exact.cpp',ROOT/'scripts/audit_selection_exact.py',ROOT/'scripts/verify_selection_exact.py',Path(__file__).resolve(),ROOT/'tests/test_selection_exact.cpp',ROOT/'notes/COORDINATED_FLIP_SELECTION.md',ROOT/'results/induction_B_tight_nonbalanced_reps.g6',report]+sorted(f for f in out.iterdir()if f.is_file())
 hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()for f in files}
 (out/'manifest.json').write_text(json.dumps(dict(status='counterexample'if failures else 'fixed_corpus_passed',graphs=data['graphs_completed'],five_sets=data['five_sets'],hash_algorithm='SHA-256',files=hashes),indent=2)+'\n')
 print(report);print('manifest SHA-256:',hashlib.sha256((out/'manifest.json').read_bytes()).hexdigest())
if __name__=='__main__':main()
