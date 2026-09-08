# Apriori Association Rule Mining

A from-scratch Python implementation of brute-force frequent-itemset mining and the Apriori algorithm. The project compares exhaustive candidate enumeration with Apriori's join-and-prune strategy and verifies that both methods produce identical association rules.

This was an individual midterm project completed by Steven Meyer for CS 634 Data Mining at the New Jersey Institute of Technology.

## Project objectives

- Implement frequent-itemset mining without external data-mining libraries.
- Generate association rules using support and confidence thresholds.
- Compare brute-force enumeration with Apriori candidate pruning.
- Verify that both algorithms return equivalent results.
- Measure the performance benefit of pruning.

## How the algorithms differ

**Brute force** enumerates every possible candidate of a given size from the complete item universe. **Apriori** generates a candidate only when its smaller subsets were already found to be frequent. This uses the downward-closure property: if an itemset is infrequent, every superset containing it must also be infrequent.

## Original experiment

The submitted project used five reproducible synthetic transaction databases. Each contained 20 transactions drawn from a 30-item retail catalog. Both algorithms used minimum support of 0.10 and minimum confidence of 0.50.

Both implementations returned identical frequent itemsets and association rules. The original single-run timings suggested that Apriori was substantially faster, but the extremely short runtimes and small datasets make those speedup estimates sensitive to timing noise. They should be treated as an illustration rather than a general performance claim.

## Portfolio improvements

The code in this repository was reconstructed from the full source included in the original report and reorganized after the course submission. The following improvements are clearly separate from the submitted experiment:

- Reusable Python modules
- Automated equivalence and validation tests
- `time.perf_counter` instead of `time.time`
- Repeated trials summarized with median runtime
- Command-line parameters for support, confidence, and repetitions

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── data/                 # Five original synthetic transaction databases
├── src/
│   ├── mining.py        # Algorithms, support, confidence, and rules
│   └── benchmark.py     # Repeatable command-line comparison
└── tests/
    └── test_mining.py   # Correctness and input-validation tests
```

## Run the benchmark

Python 3.10 or newer is recommended. No third-party packages are required.

```bash
python src/benchmark.py data/db1.txt --support 0.10 --confidence 0.50 --repeats 100
```

The script reports median runtime, frequent-itemset and rule counts, algorithm equivalence, and the median speedup ratio.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Limitations

- The original databases are synthetic and intentionally small.
- Timing results on such short-running functions vary by machine and operating conditions.
- The project compares algorithmic strategies rather than production-ready mining libraries.
- Support and confidence alone do not establish that an association is useful or causal.

Larger datasets, repeated benchmark sessions, and comparisons against established packages would be appropriate next steps.
