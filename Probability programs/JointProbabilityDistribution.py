from itertools import product

def parse_condition(cond):
    cond = cond.strip().lower()
    if cond.startswith('~'):
        return cond[1:], False
    return cond, True

def check_conditions(row, conditions):
    for var, val in conditions:
        if var not in row:
            continue
        if row[var] != val:
            return False
    return True

def normalize_kb(kb):
    """Convert counts -> probabilities if needed"""
    total = sum(row['prob'] for row in kb)
    if total == 0:
        raise ValueError("Total probability/count cannot be zero.")
    for row in kb:
        row['prob'] /= total

def row_to_condition_string(row, variables):
    return ", ".join(f"{v}={'T' if row[v] else 'F'}" for v in variables)

def conditions_to_string(conditions):
    if not conditions:
        return "True"
    return ", ".join(f"{'~' if not val else ''}{var}" for var, val in conditions)

def print_kb_table(kb, variables):
    headers = [v.upper() for v in variables] + ["PROB"]
    col_widths = [max(len(h), 5) for h in headers]

    rows = []
    for row in kb:
        vals = [('T' if row[v] else 'F') for v in variables] + [f"{row['prob']:.4f}"]
        rows.append(vals)
        for i, val in enumerate(vals):
            col_widths[i] = max(col_widths[i], len(val))

    def format_row(vals):
        return " | ".join(val.ljust(col_widths[i]) for i, val in enumerate(vals))

    sep = "-+-".join("-" * w for w in col_widths)

    print("\nNormalized Knowledge Base (Truth Table):")
    print(format_row(headers))
    print(sep)
    for vals in rows:
        print(format_row(vals))

def compute_probability_detailed(kb, variables, query_conditions, given_conditions=None):
    if given_conditions is None:
        # P(A)
        print(f"\nCalculating P({conditions_to_string(query_conditions)})")
        numerator = 0.0

        print("Rows satisfying query:")
        found = False
        for row in kb:
            if check_conditions(row, query_conditions):
                found = True
                print(f"  + {row_to_condition_string(row, variables)}  -> {row['prob']:.4f}")
                numerator += row['prob']

        if not found:
            print("  (none)")

        print(f"Numerator sum = {numerator:.4f}")
        print(f"Result = {numerator:.4f}")
        return round(numerator, 4)

    else:
        # P(A | B) = P(A and B) / P(B)
        print(f"\nCalculating P({conditions_to_string(query_conditions)} | {conditions_to_string(given_conditions)})")

        numerator = 0.0
        denominator = 0.0

        print("\nRows satisfying given condition B (for denominator P(B)):")
        found_b = False
        for row in kb:
            if check_conditions(row, given_conditions):
                found_b = True
                print(f"  + {row_to_condition_string(row, variables)}  -> {row['prob']:.4f}")
                denominator += row['prob']

        if not found_b:
            print("  (none)")

        print(f"Denominator P(B) = {denominator:.4f}")

        print("\nRows satisfying both A and B (for numerator P(A and B)):")
        found_ab = False
        combined = query_conditions + given_conditions
        for row in kb:
            if check_conditions(row, combined):
                found_ab = True
                print(f"  + {row_to_condition_string(row, variables)}  -> {row['prob']:.4f}")
                numerator += row['prob']

        if not found_ab:
            print("  (none)")

        print(f"Numerator P(A and B) = {numerator:.4f}")

        if denominator == 0:
            print("Since P(B)=0, result is set to 0.")
            return 0.0

        result = numerator / denominator
        print(f"Result = P(A and B)/P(B) = {numerator:.4f}/{denominator:.4f} = {result:.4f}")
        return round(result, 4)

def main():
    num_vars = int(input("Enter number of variables: ").strip())

    variables = []
    print("Enter variable names:")
    for _ in range(num_vars):
        variables.append(input().strip().lower())

    combinations = list(product([True, False], repeat=num_vars))
    kb = []

    print("\nEnter probabilities OR counts for each combination:")
    for comb in combinations:
        row = {}
        display_parts = []

        for i, val in enumerate(comb):
            row[variables[i]] = val
            display_parts.append(f"{variables[i]}={'T' if val else 'F'}")

        print(", ".join(display_parts))
        row['prob'] = float(input("Value: "))
        kb.append(row)

    normalize_kb(kb)

    # Print table before query section
    print_kb_table(kb, variables)

    print("\n--- Query Section ---")
    print("Examples: P(a), P(a|b), P(a,~b|c)")

    while True:
        raw_query = input("\nEnter query (or 'exit'): ").strip().lower()
        if raw_query == 'exit':
            break

        clean_query = raw_query.replace("p(", "").replace(")", "").strip()

        if '|' in clean_query:
            left, right = clean_query.split('|')
            query_vars = [parse_condition(c) for c in left.split(',') if c.strip()]
            given_vars = [parse_condition(c) for c in right.split(',') if c.strip()]
            result = compute_probability_detailed(kb, variables, query_vars, given_vars)
        else:
            query_vars = [parse_condition(c) for c in clean_query.split(',') if c.strip()]
            result = compute_probability_detailed(kb, variables, query_vars)

        print(f"Final Answer = {result:.4f}")

if __name__ == "__main__":
    main()