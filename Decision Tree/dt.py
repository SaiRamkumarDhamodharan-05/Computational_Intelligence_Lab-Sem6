import csv
import math
import random
from collections import Counter

# ---------- READ DATA ----------
def read_dataset(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        # Sniff the delimiter (handles commas, tabs, semicolons)
        content = file.read(2048)
        dialect = csv.Sniffer().sniff(content)
        file.seek(0)

        reader = csv.reader(file, dialect)
        raw_data = [row for row in reader if row] # skip empty lines

    # Clean whitespace from every cell to ensure consistency
    data = [[cell.strip() for cell in row] for row in raw_data]

    attributes = data[0][:-1]
    dataset = data[1:]
    return attributes, dataset

# ---------- ENTROPY (print only, returns value) ----------
def entropy(data, label="S"):
    if not data:
        return 0
    labels = [row[-1] for row in data]
    total = len(labels)
    counts = Counter(labels)
    ent = 0
    for cls in counts:
        p = counts[cls] / total
        contribution = p * math.log2(p) if p > 0 else 0
        ent -= contribution
    return ent

def print_entropy(data, label="S"):
    if not data:
        return 0
    labels = [row[-1] for row in data]
    total = len(labels)
    counts = Counter(labels)

    print(f"\n  Entropy( {label} )")
    print(f"    Total Instances : {total}")
    ent = 0
    parts = []
    for cls in counts:
        p = counts[cls] / total
        contribution = p * math.log2(p) if p > 0 else 0
        ent -= contribution
        parts.append(f"-({counts[cls]}/{total}) * log2({counts[cls]}/{total})")
        print(f"    P({cls:<6}) = {counts[cls]:>3} / {total} = {p:.4f}   =>  contribution = {-contribution:.4f}")
    print(f"    Entropy = {' + '.join(parts)}")
    print(f"    Entropy( {label} ) = {ent:.4f}")
    return ent

# ---------- SPLIT ----------
def split_data(data, attr_index, value):
    return [row for row in data if row[attr_index] == value]

# -----------------------------------------------------------------------
# PHASE 1 : Print class split tables for ALL features
# -----------------------------------------------------------------------
def phase1_class_splits(data, attributes):
    print("\n+----------------------------------------------------------+")
    print("|              PHASE 1 : CLASS SPLIT TABLES               |")
    print("+----------------------------------------------------------+")
    classes = sorted(set(row[-1] for row in data))
    for i, attr in enumerate(attributes):
        values = sorted(set(row[i] for row in data))
        col_w = max(8, max(len(v) for v in values) + 2)
        cls_w = 7
        header = f"  {'Value':<{col_w}}" + "".join(f"  {c:<{cls_w}}" for c in classes) + "   Total"
        sep = "  " + "-" * (len(header) - 2)
        print(f"\n  Attribute : {attr}")
        print(sep)
        print(header)
        print(sep)
        for v in values:
            subset = split_data(data, i, v)
            counts = Counter(row[-1] for row in subset)
            row_str = f"  {v:<{col_w}}" + "".join(f"  {counts.get(c, 0):<{cls_w}}" for c in classes)
            print(f"{row_str}   {len(subset)}")
        print(sep)

# -----------------------------------------------------------------------
# PHASE 2 : Print entropy + weighted entropy for each feature
# -----------------------------------------------------------------------
def phase2_entropy_weighted(data, attributes):
    print("\n+----------------------------------------------------------+")
    print("|         PHASE 2 : ENTROPY & WEIGHTED ENTROPY            |")
    print("+----------------------------------------------------------+")

    total_entropy = entropy(data)
    # Print overall entropy
    print(f"\n  Overall Entropy(S) for {len(data)} instances:")
    print_entropy(data, "S")

    gains = {}
    for i, attr in enumerate(attributes):
        values = sorted(set(row[i] for row in data))
        print(f"\n  {'='*54}")
        print(f"  Feature : {attr}")
        print(f"  {'='*54}")

        weighted = 0
        sub_entropies = {}
        for v in values:
            subset = split_data(data, i, v)
            w = len(subset) / len(data)
            se = print_entropy(subset, f"{attr}={v}")
            sub_entropies[v] = (w, se)
            weighted += w * se

        print(f"\n  Weighted Entropy Summary for '{attr}':")
        print(f"  {'  Value':<18}  Weight       SubEntropy   Weighted")
        print(f"  {'-'*58}")
        for v, (w, se) in sub_entropies.items():
            print(f"  {v:<18}  {w:.4f}       {se:.4f}       {w*se:.4f}")
        print(f"  {'-'*58}")
        print(f"  Total Weighted Entropy  =  {weighted:.4f}")

        ig = total_entropy - weighted
        gains[attr] = ig

    return gains

# -----------------------------------------------------------------------
# PHASE 3 : Information Gain Summary + Best Root
# -----------------------------------------------------------------------
def phase3_summary(gains):
    best = max(gains, key=gains.get)
    width = 44
    print("\n+" + "-"*width + "+")
    print("|" + " PHASE 3 : INFORMATION GAIN SUMMARY ".center(width) + "|")
    print("+" + "-"*width + "+")
    print("|" + f"  {'Feature':<18}  {'Info Gain':>10}".ljust(width) + "|")
    print("|" + ("-"*(width-2)).center(width) + "|")
    for attr, ig in gains.items():
        line = f"  {attr:<18}  {ig:.4f}"
        print("|" + line.ljust(width) + "|")
    print("+" + "-"*width + "+")
    print("|" + f"  Best Root Node  =>  {best}".ljust(width) + "|")
    print("+" + "-"*width + "+")
    return best

# ---------- FIND ROOT ----------
def find_root(data, attributes):
    phase1_class_splits(data, attributes)
    gains = phase2_entropy_weighted(data, attributes)
    best  = phase3_summary(gains)
    return best

# ---------- SILENT HELPERS (used only for recursive tree building) ----------
def _entropy_silent(data):
    if not data:
        return 0
    labels = [row[-1] for row in data]
    total = len(labels)
    counts = Counter(labels)
    ent = 0
    for cls in counts:
        p = counts[cls] / total
        ent -= p * math.log2(p) if p > 0 else 0
    return ent

def _ig_silent(data, attr_index):
    total_entropy = _entropy_silent(data)
    values = set(row[attr_index] for row in data)
    weighted = 0
    for v in values:
        subset = split_data(data, attr_index, v)
        weighted += (len(subset) / len(data)) * _entropy_silent(subset)
    return total_entropy - weighted

def majority_class(data):
    labels = [row[-1] for row in data]
    return Counter(labels).most_common(1)[0][0]

# ---------- BUILD FULL TREE (recursive, silent) ----------
def build_tree(data, attributes, attr_indices):
    if not data:
        return "Unknown"
    labels = [row[-1] for row in data]
    if len(set(labels)) == 1:
        return labels[0]
    if not attributes:
        return majority_class(data)

    gains = {attr: _ig_silent(data, attr_indices[i]) for i, attr in enumerate(attributes)}
    best_attr = max(gains, key=gains.get)
    best_pos = attributes.index(best_attr)
    best_idx = attr_indices[best_pos]

    remaining_attrs   = [a   for i, a   in enumerate(attributes)   if i != best_pos]
    remaining_indices = [idx for i, idx in enumerate(attr_indices) if i != best_pos]

    tree = {best_attr: {}}
    for v in sorted(set(row[best_idx] for row in data)):
        subset = split_data(data, best_idx, v)
        tree[best_attr][v] = build_tree(subset, remaining_attrs, remaining_indices) if subset else majority_class(data)

    return tree

# ---------- PRINT TREE (Level by Level) ----------
def print_tree(tree):
    from collections import deque
    # Each item: (subtree, depth, branch_label)
    queue = deque()
    queue.append((tree, 0, ""))
    current_depth = -1

    while queue:
        node, depth, label = queue.popleft()

        if depth != current_depth:
            current_depth = depth
            print(f"\nDecision Tree (Level {depth})")
            print("-" * 30)

        if isinstance(node, str):
            prefix = f"  {label}  -->  " if label else "  "
            print(f"{prefix}[{node}]  (Leaf)")
        else:
            for attr, branches in node.items():
                prefix = f"  {label}  -->  " if label else "  "
                print(f"{prefix}[{attr}]")
                for value, subtree in sorted(branches.items()):
                    queue.append((subtree, depth + 1, f"{attr} = {value}"))

# ---------- MAIN ----------
def main():
    try:
        filename = input("Enter file name (e.g., data.csv or data.txt): ").strip()
        attributes, data = read_dataset(filename)

        """if len(data) > 10:
            data = random.sample(data, 10)
        else:
            random.shuffle(data)"""

        print(f"\nDataset loaded: {len(attributes)} attributes, {len(data)} rows (randomly sampled).")
        print("Attributes found:", attributes)

        if not data:
            print("Error: The dataset contains no records.")
            return

        # Display sampled rows as a table
        col_w = 10
        header_row = " | ".join(f"{a[:col_w]:<{col_w}}" for a in attributes + ["Class"])
        sep = "-" * len(header_row)
        print(f"\n  Randomly Sampled {len(data)} Rows:")
        print("  " + sep)
        print("  " + header_row)
        print("  " + sep)
        for row in data:
            print("  " + " | ".join(f"{str(v)[:col_w]:<{col_w}}" for v in row))
        print("  " + sep)

        # Check if all rows are the same class
        all_labels = [row[-1] for row in data]
        if len(set(all_labels)) == 1:
            print(f"\n  Note: All 50 sampled rows belong to class '{all_labels[0]}'.")
            print("  Cannot build a meaningful tree. Try running again for a different sample.")
            return

        root = find_root(data, attributes)

        print("\n+----------------------------------------+")
        print("|       BUILDING FULL DECISION TREE      |")
        print("+----------------------------------------+")
        attr_indices = list(range(len(attributes)))
        tree = build_tree(data, attributes, attr_indices)

        print("\n+----------------------------------------+")
        print("|            FULL DECISION TREE          |")
        print("+----------------------------------------+")
        print_tree(tree)

    except FileNotFoundError:
        print("Error: File not found. Please check the filename.")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()