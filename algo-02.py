#!/usr/bin/env python3
from typing import Dict, List, Any
from base import run_algorithm

def algo_02_decision(
    constraints: List[Dict[str, Any]],
    attribute_statistics: Dict[str, Any],
    correlations: Dict[str, Dict[str, float]],
    admitted_count: int,
    rejected_count: int,
    next_person: Dict[str, Any],
    accepted_count: Dict[str, int]
) -> bool:
    remaining_spots = 1000 - admitted_count

    # Calculate values for each constraint attribute
    values = {}
    for constraint in constraints:
        attr_id = constraint["attribute"]
        min_count = constraint["minCount"]
        current_accepted = accepted_count.get(attr_id, 0)
        remaining_needed = min_count - current_accepted

        if remaining_needed <= 0:
            values[attr_id] = 0.0
        else:
            values[attr_id] = remaining_needed / remaining_spots

    # Sum values for attributes that the person does NOT have
    person_attributes = next_person.get("attributes", {})
    total_value = 0.0

    for attr_id in values:
        if not person_attributes.get(attr_id, False):
            total_value += values[attr_id]

    return total_value < 1.0

if __name__ == "__main__":
    run_algorithm(algo_02_decision, scenario=3, algo_name="algo_02")
