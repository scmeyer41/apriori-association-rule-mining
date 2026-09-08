"""Repeatable command-line benchmark for brute force and Apriori."""

import argparse
from pathlib import Path
from statistics import median
from time import perf_counter

from mining import (
    apriori_frequent_itemsets,
    brute_force_frequent_itemsets,
    canonical_rules,
    generate_rules,
    load_transactions,
)


def timed_run(function, transactions, min_support, repeats):
    durations = []
    result = None
    for _ in range(repeats):
        start = perf_counter()
        result = function(transactions, min_support)
        durations.append(perf_counter() - start)
    return result, median(durations)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=Path, help="Transaction database text file")
    parser.add_argument("--support", type=float, default=0.10)
    parser.add_argument("--confidence", type=float, default=0.50)
    parser.add_argument("--repeats", type=int, default=100)
    args = parser.parse_args()

    transactions = load_transactions(args.data)
    brute_sets, brute_time = timed_run(
        brute_force_frequent_itemsets, transactions, args.support, args.repeats
    )
    apriori_sets, apriori_time = timed_run(
        apriori_frequent_itemsets, transactions, args.support, args.repeats
    )

    brute_rules = generate_rules(brute_sets, args.confidence)
    apriori_rules = generate_rules(apriori_sets, args.confidence)
    identical = canonical_rules(brute_rules) == canonical_rules(apriori_rules)

    print(f"Transactions: {len(transactions)}")
    print(f"Frequent itemsets: {len(apriori_sets)}")
    print(f"Association rules: {len(apriori_rules)}")
    print(f"Rules identical: {identical}")
    print(f"Brute-force median: {brute_time:.6f} seconds")
    print(f"Apriori median: {apriori_time:.6f} seconds")
    print(f"Median speedup: {brute_time / apriori_time:.2f}x")


if __name__ == "__main__":
    main()
