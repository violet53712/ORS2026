import pandas as pd
import numpy as np

# Configuration
BATCH_SIZE = 41
INPUT_FILE = 'optim.csv'

# Load data
df = pd.read_csv(INPUT_FILE)

# Define dimension columns
dimension_cols = [
    "d []", "dw [mm]", "h [mm]", "h_s [mm]", "l [mm]", 
    "l_inset [mm]", "l_s [mm]", "ls [mm]", "w [mm]", 
    "w_inset [mm]", "w_s [mm]"
]

# Calculate number of batches
num_batches = len(df) // BATCH_SIZE

# INITIALIZE lists to store results for each batch
results = {
    'operating_freq_GHz': [],
    's11_left_dB': [],
    's11_min_dB': [],
    's11_right_dB': [],
    'min_index_in_batch': []
}

# Add dimension columns to results
for dim in dimension_cols:
    results[dim] = []



# Process each batch
for batch_num in range(num_batches):
    # Calculate start and end indices for this batch
    start_idx = batch_num * BATCH_SIZE
    end_idx = start_idx + BATCH_SIZE
    
    # Extract batch data
    batch_s11 = df["dB(St(port1_T1,port1_T1)) []"].iloc[start_idx:end_idx].values
    batch_freq = df["Freq [GHz]"].iloc[start_idx:end_idx].values
    
    # Find minimum S11 in this batch
    min_idx = np.argmin(batch_s11)
    
    # Get S11 values (with boundary protection)
    left_idx = max(0, min_idx - 2)
    right_idx = min(len(batch_s11) - 1, min_idx + 2)
    
    # Store S11 results
    results['operating_freq_GHz'].append(batch_freq[min_idx])
    results['s11_left_dB'].append(batch_s11[left_idx])
    results['s11_min_dB'].append(batch_s11[min_idx])
    results['s11_right_dB'].append(batch_s11[right_idx])
    results['min_index_in_batch'].append(min_idx)
    
    # Store dimension values (take first row of batch as representative)
    for dim in dimension_cols:
        results[dim].append(df[dim].iloc[start_idx])

# Create output dataframe
output_df = pd.DataFrame(results)

# Reorder columns: dimensions first, then results
column_order = dimension_cols + [
    'operating_freq_GHz', 
    's11_min_dB', 
    's11_left_dB', 
    's11_right_dB', 
    'min_index_in_batch'
]
output_df = output_df[column_order]

# Save to files
output_df.to_csv('goodata2.csv', index=False)
output_df.to_excel("output2.xlsx", sheet_name='Sheet1', index=False)

# Display summary
print(f"Processed {num_batches} batches of {BATCH_SIZE} samples each")
print(f"\nOutput shape: {output_df.shape[0]} rows × {output_df.shape[1]} columns")
print(f"\nColumns: {output_df.columns.tolist()}")

print("\n" + "="*60)
print("SUMMARY STATISTICS")
print("="*60)
print(f"Best S11 (most negative):  {output_df['s11_min_dB'].min():.4f} dB")
print(f"Worst S11 (least negative): {output_df['s11_min_dB'].max():.4f} dB")
print(f"Mean S11:                   {output_df['s11_min_dB'].mean():.4f} dB")
print(f"\nOperating Frequency Range:  {output_df['operating_freq_GHz'].min():.4f} - {output_df['operating_freq_GHz'].max():.4f} GHz")

print("\n" + "="*60)
print("FIRST 5 ROWS OF OUTPUT")
print("="*60)
print(output_df.head())