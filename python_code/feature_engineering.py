import os
import pandas as pd
import numpy as np

# ==========================================
# 0. Dynamic File Path Resolution & Loading
# ==========================================
script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

def find_file(filename, search_dir):
    """Search for a file in the directory or subdirectories."""
    path = os.path.join(search_dir, filename)
    if os.path.exists(path):
        return path
    for root, _, files in os.walk(search_dir):
        for f in files:
            if filename.lower() in f.lower():
                return os.path.join(root, f)
    return None

client_file = find_file("clean_data_after_eda.csv", script_dir) or "clean_data_after_eda.csv"
price_file = find_file("price_data.csv", script_dir) or find_file("price_data (1).csv", script_dir) or "price_data.csv"

print(f"Loading client dataset from: {client_file}")
print(f"Loading price dataset from:  {price_file}")

client_df = pd.read_csv(client_file)
price_df = pd.read_csv(price_file)

# ==========================================
# 1. Price Feature Engineering (Estelle's Hypothesis)
# ==========================================
print("\n--- Engineering Price Difference Features (Dec vs Jan) ---")

price_df['price_date'] = pd.to_datetime(price_df['price_date'])

# Compute total prices (variable energy rate + fixed power rate)
price_df['price_off_peak'] = price_df['price_off_peak_var'] + price_df['price_off_peak_fix']
price_df['price_peak'] = price_df['price_peak_var'] + price_df['price_peak_fix']
price_df['price_mid_peak'] = price_df['price_mid_peak_var'] + price_df['price_mid_peak_fix']

# Isolate January and December price snapshots
jan_prices = price_df[price_df['price_date'].dt.month == 1].set_index('id')
dec_prices = price_df[price_df['price_date'].dt.month == 12].set_index('id')

# Calculate price differences between December and January
price_diff = pd.DataFrame(index=price_df['id'].unique())

# Off-Peak Differences (Estelle's primary feature)
price_diff['offpeak_diff_dec_jan_energy'] = dec_prices['price_off_peak_var'] - jan_prices['price_off_peak_var']
price_diff['offpeak_diff_dec_jan_power'] = dec_prices['price_off_peak_fix'] - jan_prices['price_off_peak_fix']
price_diff['offpeak_diff_dec_jan'] = dec_prices['price_off_peak'] - jan_prices['price_off_peak']

# Peak Differences
price_diff['peak_diff_dec_jan_energy'] = dec_prices['price_peak_var'] - jan_prices['price_peak_var']
price_diff['peak_diff_dec_jan_power'] = dec_prices['price_peak_fix'] - jan_prices['price_peak_fix']
price_diff['peak_diff_dec_jan'] = dec_prices['price_peak'] - jan_prices['price_peak']

# Mid-Peak Differences
price_diff['midpeak_diff_dec_jan_energy'] = dec_prices['price_mid_peak_var'] - jan_prices['price_mid_peak_var']
price_diff['midpeak_diff_dec_jan_power'] = dec_prices['price_mid_peak_fix'] - jan_prices['price_mid_peak_fix']
price_diff['midpeak_diff_dec_jan'] = dec_prices['price_mid_peak'] - jan_prices['price_mid_peak']

price_diff = price_diff.fillna(0).reset_index().rename(columns={'index': 'id'})

# Aggregated annual pricing statistics per customer
price_agg = price_df.groupby('id').agg({
    'price_off_peak_var': ['mean', 'min', 'max', 'std'],
    'price_peak_var': ['mean', 'min', 'max', 'std'],
    'price_mid_peak_var': ['mean', 'min', 'max', 'std'],
    'price_off_peak_fix': ['mean', 'min', 'max', 'std'],
    'price_peak_fix': ['mean', 'min', 'max', 'std'],
    'price_mid_peak_fix': ['mean', 'min', 'max', 'std']
})
price_agg.columns = ['_'.join(col) for col in price_agg.columns]
price_agg = price_agg.fillna(0).reset_index()

# Merge price features with client dataset
df = client_df.merge(price_diff, on='id', how='left')
df = df.merge(price_agg, on='id', how='left')

# ==========================================
# 2. Date Transformations & Tenure Extraction
# ==========================================
print("\n--- Transforming Date Features ---")

date_cols = ['date_activ', 'date_end', 'date_modif_prod', 'date_renewal']
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col])

# Benchmark reference point
ref_date = pd.to_datetime('2016-01-01')

# Fixed timedelta calculation compatible with Pandas 2.0+ and NumPy 2.0+
df['months_activ'] = ((ref_date - df['date_activ']).dt.days // 30.4375).astype(int)
df['months_to_end'] = ((df['date_end'] - ref_date).dt.days // 30.4375).astype(int)
df['months_modif'] = ((ref_date - df['date_modif_prod']).dt.days // 30.4375).astype(int)
df['months_renewal'] = ((ref_date - df['date_renewal']).dt.days // 30.4375).astype(int)

# Drop raw date columns
df = df.drop(columns=date_cols, errors='ignore')

# ==========================================
# 3. Consumption Ratios & Financial Metrics
# ==========================================
print("\n--- Creating Consumption & Profitability Ratios ---")

df['total_cons_12m'] = df['cons_12m'] + df['cons_gas_12m']
df['cons_last_month_ratio'] = df['cons_last_month'] / ((df['cons_12m'] / 12) + 1)
df['forecast_vs_actual_cons'] = df['forecast_cons_12m'] / (df['cons_12m'] + 1)
df['net_margin_per_cons'] = df['net_margin'] / (df['cons_12m'] + 1)

# ==========================================
# 4. Categorical Encoding & Output
# ==========================================
print("\n--- Encoding Categorical Variables ---")

if 'has_gas' in df.columns:
    df['has_gas'] = df['has_gas'].map({'t': 1, 'f': 0, True: 1, False: 0}).fillna(0).astype(int)

cat_cols = [c for c in ['channel_sales', 'origin_up'] if c in df.columns]
df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

# Save output
output_file = os.path.join(script_dir, "clean_data_engineered.csv")
df.to_csv(output_file, index=False)

print(f"\nFeature Engineering Complete!")
print(f"Engineered Dataset Shape: {df.shape}")
print(f"Saved output file to: {output_file}")