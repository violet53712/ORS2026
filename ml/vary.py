import pandas as pd
import numpy as np

# Load your CSV file
df = pd.read_csv("optim.csv")
#df = df.drop(["Freq [GHz]","dB(St(port1_T1,port1_T1)) []"], axis=1)
# Display basic info about the dataset
print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\n" + "="*50)

# Analyze numeric columns only
numeric_cols = df.iloc[:, :-2].columns
print(numeric_cols)

if len(numeric_cols) == 0:
    print("No numeric columns found in the dataset.")
else:
    # Calculate variance for each numeric column
    variances = df[numeric_cols].var()
    
    # Calculate coefficient of variation (std/mean) for better comparison
    # This normalizes variance by the mean, useful when columns have different scales
    cv = df[numeric_cols].std() / df[numeric_cols].mean().abs()
    
    # Create summary dataframe
    summary = pd.DataFrame({
        'Column': numeric_cols,
        'Variance': variances.values,
        'Std Dev': df[numeric_cols].std().values,
        'Mean': df[numeric_cols].mean().values,
        'Coef of Variation': cv.values
    })
    
    # Sort by variance (ascending) to see least varying columns first
    summary_by_var = summary.sort_values('Variance')
    print("\nColumns ranked by VARIANCE (least to most):")
    print(summary_by_var.to_string(index=False))
    
    print("\n" + "="*50)
    
    # Sort by coefficient of variation for normalized comparison
    summary_by_cv = summary.sort_values('Coef of Variation')
    print("\nColumns ranked by COEFFICIENT OF VARIATION (least to most):")
    print(summary_by_cv.to_string(index=False))
    
    print("\n" + "="*50)
    print("\nMost varying columns:")
    print(f"By variance: {summary_by_var.iloc[-1]['Column']}")
    print(f"By coefficient of variation: {summary_by_cv.iloc[-1]['Column']}")

# If you want to analyze categorical columns
categorical_cols = df.select_dtypes(include=['object', 'category']).columns

if len(categorical_cols) > 0:
    print("\n" + "="*50)
    print("\nCategorical columns analysis:")
    
    cat_summary = []
    for col in categorical_cols:
        unique_count = df[col].nunique()
        most_common = df[col].value_counts().iloc[0]
        most_common_pct = (most_common / len(df)) * 100
        
        cat_summary.append({
            'Column': col,
            'Unique Values': unique_count,
            'Most Common %': most_common_pct
        })
    
    cat_df = pd.DataFrame(cat_summary)
    # Higher percentage of most common value = less variation
    cat_df = cat_df.sort_values('Most Common %', ascending=False)
    
    print("\nCategorical columns (sorted by least variation):")
    print(cat_df.to_string(index=False))