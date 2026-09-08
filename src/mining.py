"""Frequent-itemset and association-rule mining implemented from scratch."""

from itertools import combinations
from pathlib import Path


Itemset = frozenset[str]
Rule = tuple[Itemset, Itemset, float, float]


def load_transactions(path: str | Path) -> list[set[str]]:
    """Load one space-separated transaction per line."""
    with open(path, encoding="utf-8") as stream:
        return [set(line.split()) for line in stream if line.strip()]


def support_count(itemset: Itemset, transactions: list[set[str]]) -> int:
    return sum(itemset.issubset(transaction) for transaction in transactions)


def support(itemset: Itemset, transactions: list[set[str]]) -> float:
    if not transactions:
        raise ValueError("transactions must not be empty")
    return support_count(itemset, transactions) / len(transactions)


def brute_force_frequent_itemsets(
    transactions: list[set[str]], min_support: float
) -> dict[Itemset, float]:
    """Enumerate every candidate at each level until no frequent set remains."""
    _validate_inputs(transactions, min_support)
    universe = sorted(set().union(*transactions))
    frequent: dict[Itemset, float] = {}

    for size in range(1, len(universe) + 1):
        frequent_at_size: dict[Itemset, float] = {}
        for candidate in combinations(universe, size):
            itemset = frozenset(candidate)
            itemset_support = support(itemset, transactions)
            if itemset_support >= min_support:
                frequent_at_size[itemset] = itemset_support

        if not frequent_at_size:
            break
        frequent.update(frequent_at_size)

    return frequent


def apriori_candidates(previous_level: set[Itemset], size: int) -> set[Itemset]:
    """Join frequent (k-1)-itemsets and prune invalid k-itemsets."""
    ordered = sorted(tuple(sorted(itemset)) for itemset in previous_level)
    candidates: set[Itemset] = set()

    for index, left in enumerate(ordered):
        for right in ordered[index + 1 :]:
            if left[: size - 2] != right[: size - 2]:
                break
            candidate = frozenset(left) | frozenset(right)
            if len(candidate) == size:
                candidates.add(candidate)

    return {
        candidate
        for candidate in candidates
        if all(
            frozenset(subset) in previous_level
            for subset in combinations(sorted(candidate), size - 1)
        )
    }


def apriori_frequent_itemsets(
    transactions: list[set[str]], min_support: float
) -> dict[Itemset, float]:
    """Mine frequent itemsets using Apriori join-and-prune candidate generation."""
    _validate_inputs(transactions, min_support)
    universe = sorted(set().union(*transactions))
    frequent: dict[Itemset, float] = {}

    previous_level: set[Itemset] = set()
    for item in universe:
        itemset = frozenset({item})
        itemset_support = support(itemset, transactions)
        if itemset_support >= min_support:
            previous_level.add(itemset)
            frequent[itemset] = itemset_support

    size = 2
    while previous_level:
        candidates = apriori_candidates(previous_level, size)
        current_level: set[Itemset] = set()
        for candidate in candidates:
            candidate_support = support(candidate, transactions)
            if candidate_support >= min_support:
                current_level.add(candidate)
                frequent[candidate] = candidate_support
        previous_level = current_level
        size += 1

    return frequent


def generate_rules(
    frequent_itemsets: dict[Itemset, float], min_confidence: float
) -> list[Rule]:
    """Generate rules from frequent itemsets using stored support values."""
    if not 0 <= min_confidence <= 1:
        raise ValueError("min_confidence must be between 0 and 1")

    rules: list[Rule] = []
    for itemset, itemset_support in frequent_itemsets.items():
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for antecedent_tuple in combinations(sorted(itemset), size):
                antecedent = frozenset(antecedent_tuple)
                consequent = itemset - antecedent
                confidence = itemset_support / frequent_itemsets[antecedent]
                if confidence >= min_confidence:
                    rules.append(
                        (antecedent, consequent, itemset_support, confidence)
                    )
    return rules


def canonical_rules(rules: list[Rule]) -> set[tuple]:
    """Return an order-independent representation for correctness checks."""
    return {
        (
            tuple(sorted(antecedent)),
            tuple(sorted(consequent)),
            round(itemset_support, 12),
            round(confidence, 12),
        )
        for antecedent, consequent, itemset_support, confidence in rules
    }


def _validate_inputs(transactions: list[set[str]], min_support: float) -> None:
    if not transactions:
        raise ValueError("transactions must not be empty")
    if not 0 < min_support <= 1:
        raise ValueError("min_support must be greater than 0 and at most 1")
