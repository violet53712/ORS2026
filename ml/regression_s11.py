import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# Load your data
df = pd.read_csv('goodata2.csv')

# Define your four input parameters (X) and target variable (y)
# Replace these column names with your actual column names
X = df[["dw [mm]", "w_inset [mm]","d []", "w [mm]"]]
y = df["s11_min_dB"]

# Create and fit the regression model
model = LinearRegression()
model.fit(X, y)

# Make predictions
y_pred = model.predict(X)

# Display results
print("="*50)
print("REGRESSION RESULTS")
print("="*50)

print("\nCoefficients:")
for i, col in enumerate(X.columns):
    print(f"  {col}: {model.coef_[i]:.4f}")

print(f"\nIntercept: {model.intercept_:.4f}")

print("\nModel Performance:")
print(f"  R² Score: {r2_score(y, y_pred):.4f}")
print(f"  RMSE: {np.sqrt(mean_squared_error(y, y_pred)):.4f}")

print("\n" + "="*50)
print("EQUATION:")
equation = f"y = {model.intercept_:.4f}"
for i, col in enumerate(X.columns):
    equation += f" + ({model.coef_[i]:.4f} × {col})"
print(equation)
print("="*50)

# Show first few predictions vs actual
print("\nPredictions vs Actual:")
comparison = pd.DataFrame({
    'Actual': y.values,
    'Predicted': y_pred,
    'Difference': y.values - y_pred
})
print(comparison.to_string(index=False))

# Optional: Make predictions on new data
# new_data = pd.DataFrame({
#     'param1': [1.0],
#     'param2': [2.0],
#     'param3': [3.0],
#     'param4': [4.0]
# })
# new_prediction = model.predict(new_data)
# print(f"\nNew prediction: {new_prediction[0]:.4f}")