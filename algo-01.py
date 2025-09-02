#!/usr/bin/env python3
from typing import Dict, List, Any
from base import run_algorithm

def algo_01_decision(
    constraints: List[Dict[str, Any]],
    attribute_statistics: Dict[str, Any],
    correlations: Dict[str, Dict[str, float]],
    admitted_count: int,
    rejected_count: int,
    next_person: Dict[str, Any],
    accepted_count: Dict[str, int]
) -> bool:
    # Simple algorithm: accept everyone
    return True

if __name__ == "__main__":
    run_algorithm(algo_01_decision, scenario=1, algo_name="algo_01")
