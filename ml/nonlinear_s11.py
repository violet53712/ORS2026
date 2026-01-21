import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import pandas as pd


df = pd.read_csv('goodata2.csv')

# Define your four input parameters (X) and target variable (y)
# Replace these column names with your actual column names
X = df[["dw [mm]", "w_inset [mm]","d []", "w [mm]"]]
y = df["s11_min_dB"]

model = Pipeline([
    ("poly", PolynomialFeatures(degree=3, include_bias=False)),
    ("linreg", LinearRegression())
])

model.fit(X, y)

poly = model.named_steps["poly"]
linreg = model.named_steps["linreg"]

feature_names = poly.get_feature_names_out(["dw [mm]", "w_inset [mm]","d []", "w [mm]"])

for name, coef in zip(feature_names, linreg.coef_):
    print(f"{coef:.3f} * {name}")

print("Intercept:", linreg.intercept_)

y_pred = model.predict(X)

# Show first few predictions vs actual
print("\nPredictions vs Actual:")
comparison = pd.DataFrame({
    'Actual': y.values,
    'Predicted': y_pred,
    'Difference': y.values - y_pred
})
print(comparison.to_string(index=False))