import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target
X = df.iloc[:, :-1]
y = df.iloc[:, -1]
n_trees = int(input("Enter number of decision trees: "))
metric=input("entropy or gini impurity:")
splits = {
    "70-30": 0.3,
    "60-40": 0.4,
    "75-25": 0.25
}
results = []
conf_matrices = {}
for split_name, test_size in splits.items():
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    if(metric=="entropy"):
        model = RandomForestClassifier(n_estimators=n_trees, criterion='entropy',random_state=42)
    else:
        model = RandomForestClassifier(n_estimators=n_trees,random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    results.append([split_name, acc, prec, rec, f1])
    cm = confusion_matrix(y_test, y_pred)
    TN, FP, FN, TP = cm.ravel()
    conf_matrices[split_name] = (TN, FP, FN, TP)
print("\nFinal Results Table:\n")
print("{:<10} {:<10} {:<12} {:<10} {:<10}".format(
    "Split", "Accuracy", "Precision", "Recall", "F1-score"
))
for row in results:
    print("{:<10} {:.4f}     {:.4f}       {:.4f}     {:.4f}".format(*row))
print("\nConfusion Matrices:\n")
for split_name, (TN, FP, FN, TP) in conf_matrices.items():
    print(f"{split_name} Split:")
    print("            Predicted")
    print(f"Actual    TP={TP}   FN={FN}")
    print(f"          FP={FP}   TN={TN}\n")