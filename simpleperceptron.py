data = []
with open("data.txt", "r") as file:
    for line in file:
        row = list(map(float, line.strip().split()))
        if row:
            data.append(row)
num_inputs = len(data[0]) - 1
epochs = int(input("Enter number of epochs: "))
weights = []
for i in range(num_inputs):
    w_val = float(input(f"Enter initial w{i+1}: "))
    weights.append(w_val)

b = float(input("Enter initial bias (b): "))
alpha = float(input("Enter learning rate (alpha): "))
theta = float(input("Enter threshold (theta): "))

def activation(yin):
    if yin > theta:
        return 1
    elif yin < -theta:
        return -1
    else:
        return 0

print("\nTraining Data from file:")
header_x = " ".join([f"x{i+1}" for i in range(num_inputs)])
print(f"{header_x} t")
for row in data:
    print(" ".join(map(str, [int(x) for x in row])))
print("\nPress ENTER to move to next step...\n")
weights_header = " | ".join([f"w{i+1}" for i in range(num_inputs)])
inputs_header = " ".join([f"x{i+1}" for i in range(num_inputs)])
#print(f"{inputs_header} t | yin | y | {weights_header} | b | status")
#print("-" * (70 + (num_inputs * 5)))
for epoch in range(epochs):
    print(f"\n--- Epoch {epoch+1} ---")
    print(f"{inputs_header} t\t | yin\t | y\t | {weights_header}\t | b ")
    print("-" * (70 + (num_inputs * 5)))
    converged = True
    for row in data:
        input()
        x_elements = row[:-1]
        t = row[-1]
        yin = b + sum(x * w for x, w in zip(x_elements, weights))
        y = activation(yin)
        if y != t:
            converged = False
            for i in range(num_inputs):
                weights[i] = weights[i] + alpha*t*x_elements[i]
            b = b + alpha * t
            status = "Updated"
        else:
            status = "No Change"
        x_str = "  ".join([str(int(x)) for x in x_elements])
        w_str = " | ".join([f"{w:.2f}" for w in weights])
        print(f"{x_str}  {int(t)} | {yin:.2f} | {y} | {w_str} | {b:.2f} ")
    if converged:
        print(f"\nSTOPPING: Model has converged (y = t for all rows).")
        break

print("\n" + "="*40)
print("TRAINING COMPLETED")
print("="*40)
print("\nFinal Weights and Bias:")
for i in range(num_inputs):
    print(f"W{i+1} = {weights[i]:.2f}")
print(f"Bias (b) = {b:.2f}")