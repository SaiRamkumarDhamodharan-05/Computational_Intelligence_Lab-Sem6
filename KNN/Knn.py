# I have used pima indian diabetes dataset




import math
import random

def distance(p1, p2, metric):
    if metric == "euclidean":
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
    else:  # manhattan
        return sum(abs(a - b) for a, b in zip(p1, p2))

def normalize(data, query):
    cols = len(query)
    norm_data = [row[:] for row in data]
    norm_query = query[:]
    mins = [min(row[i] for row in norm_data) for i in range(cols)]
    maxs = [max(row[i] for row in norm_data) for i in range(cols)]

    for row in norm_data:
        for i in range(cols):
            if maxs[i] != mins[i]:
                row[i] = (row[i] - mins[i]) / (maxs[i] - mins[i])

    for i in range(cols):
        if maxs[i] != mins[i]:
            norm_query[i] = (query[i] - mins[i]) / (maxs[i] - mins[i])

    return norm_data, norm_query

def knn():
    feature_names = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                     "Insulin", "BMI", "DPF", "Age"]

    dataset = []
    try:
        with open("data.txt") as f:
            for line in f:
                parts = line.replace(",", " ").split()
                if not parts:
                    continue
                features = list(map(float, parts[:-1]))
                label = int(parts[-1])
                dataset.append([features, label])
    except FileNotFoundError:
        print("Error: data.txt not found.")
        return

    # -------- BALANCED RANDOM SAMPLE OF 100 RECORDS --------
    class_0 = [row for row in dataset if row[1] == 0]
    class_1 = [row for row in dataset if row[1] == 1]

    sample_size = min(len(dataset),20 )
    half = sample_size // 2

    sampled_0 = random.sample(class_0, min(len(class_0), half))
    sampled_1 = random.sample(class_1, min(len(class_1), half))

    dataset = sampled_0 + sampled_1
    random.shuffle(dataset)
    # -------------------------------------------------------

    print("\nAvailable Features:")
    for i, name in enumerate(feature_names):
        print(i, "-", name)

    n = int(input("\nEnter number of features: "))
    idx = list(map(int, input("Enter feature indices: ").split()))
    sel_names = [feature_names[i] for i in idx]

    query = []
    print("\nEnter query values:")
    for i in idx:
        query.append(float(input(f"{feature_names[i]}: ")))

    query_orig = list(query)

    metric = input("\nDistance metric (euclidean/manhattan): ").lower()
    norm = input("\nApply normalization? (yes/no): ").lower()

    selected_orig = [[row[0][i] for i in idx] for row in dataset]
    labels = [row[1] for row in dataset]

    features_to_use = [row[:] for row in selected_orig]
    query_to_use = list(query_orig)

    if norm == "yes":
        features_to_use, query_to_use = normalize(features_to_use, query_to_use)

    table_data = []
    for i in range(len(dataset)):
        d = distance(features_to_use[i], query_to_use, metric)
        table_data.append({
            'orig': selected_orig[i],
            'norm': features_to_use[i],
            'dist': d,
            'label': labels[i]
        })

    sorted_by_dist = sorted(table_data, key=lambda x: x['dist'])

    # --- PRINT FULL TABLE ---
    header = ""
    for name in sel_names:
        header += f"{name:<15}"
    if norm == "yes":
        for name in sel_names:
            header += f"Norm_{name[:3]:<15}"
    header += f"{'Distance':<15} {'Rank'}"

    print("\n" + header)
    print("-" * len(header))

    for item in table_data:
        rank = sorted_by_dist.index(item) + 1
        row_str = ""
        for val in item['orig']:
            row_str += f"{val:<15.1f}"
        if norm == "yes":
            for val in item['norm']:
                row_str += f"{val:<15.3f}"
        row_str += f"{item['dist']:<15.4f} {rank}"
        print(row_str)
    count_0 = sum(1 for row in dataset if row[1] == 0)
    count_1 = sum(1 for row in dataset if row[1] == 1)

    print("\nSample Distribution (100 records):")
    print(f"Non-Diabetic (Class 0): {count_0}")
    print(f"Diabetic (Class 1): {count_1}")
    while True:
        user_input = input("\nEnter K value ('exit' to stop): ").lower()

        if user_input == "exit":
            print("\nExit")
            break

        k = int(user_input)
        vote_type = input("Voting method (weighted/unweighted): ").lower()

        neighbors = sorted_by_dist[:k]

        print(f"\n{'NEAREST NEIGHBORS':^80}")

        neigh_header = ""
        for name in sel_names:
            neigh_header += f"{name:<15}"
        neigh_header += f"{'Distance':<15} {'Class':<10}"
        if vote_type == "weighted":
            neigh_header += "Weight(1/d^2)"

        print(neigh_header)
        print("-" * len(neigh_header))

        score = {}
        weight_details = {}

        for nbr in neighbors:
            weight = 1.0 if vote_type == "unweighted" else 1 / (nbr['dist']**2 + 0.0001)
            score[nbr['label']] = score.get(nbr['label'], 0) + weight

            if vote_type == "weighted":
                weight_details.setdefault(nbr['label'], []).append(weight)

            row_str = ""
            for val in nbr['orig']:
                row_str += f"{val:<15.1f}"
            row_str += f"{nbr['dist']:<15.4f} {nbr['label']:<10}"
            if vote_type == "weighted":
                row_str += f"{weight:.6f}"

            print(row_str)

        if vote_type == "weighted":
            print("\nWeighted Calculation:")
            print("-" * 40)
            for cls in sorted(score.keys()):
                status = "Diabetic" if cls == 1 else "Non-Diabetic"
                print(f"Total Weight for Class {cls} ({status}): {score[cls]:.6f}")
                calc_expr = " + ".join(f"{w:.6f}" for w in weight_details[cls])
                print(f"Calculation: {calc_expr} = {score[cls]:.6f}")
        else:
            print("\nMajority Count:")
            for cls in sorted(score.keys()):
                status = "Diabetic" if cls == 1 else "Non-Diabetic"
                print(f"Class {cls} ({status}): {int(score[cls])}")

        result = max(score, key=score.get)

        print(f"\nThe given query is classified as "
              f"{'Diabetic(1)' if result == 1 else 'Non-Diabetic(0)'} "
              f"by {vote_type} voting.")

if __name__ == "__main__":
    knn()