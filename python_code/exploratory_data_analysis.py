import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# ==========================================
# 0. Dynamic File Path Resolution
# ==========================================
script_dir = os.path.dirname(os.path.abspath(__file__))

def find_file(filename, search_dir):
    """Search for a file in the script directory or subdirectories."""
    path1 = os.path.join(search_dir, filename)
    if os.path.exists(path1):
        return path1
    
    for root, dirs, files in os.walk(search_dir):
        for f in files:
            if filename.lower() in f.lower():
                return os.path.join(root, f)
    return None

client_file_path = find_file("client_data.csv", script_dir) or "client_data.csv"
price_file_path = find_file("price_data.csv", script_dir) or "price_data.csv"

print(f"Loading client data from: {client_file_path}")
print(f"Loading price data from:  {price_file_path}")

client_df = pd.read_csv(client_file_path)
price_df = pd.read_csv(price_file_path)

# Ensure churn is integer type to avoid type mismatch
if 'churn' in client_df.columns:
    client_df['churn'] = client_df['churn'].astype(int)

# Color palette mapping
palette_colors = {0: '#2b5c8f', 1: '#d95f02'}

# ==========================================
# 1. Helper Plotting Functions
# ==========================================

def plot_distribution(df, column, ax, bins_=50):
    """Plot distribution of a numerical column split by churn status."""
    sns.histplot(
        data=df,
        x=column,
        hue='churn',
        bins=bins_,
        kde=True,
        element='step',
        stat='density',
        common_norm=False,
        ax=ax,
        palette=palette_colors
    )
    ax.set_title(f'Distribution of {column} by Churn Status', fontsize=12, fontweight='bold')
    ax.set_xlabel(column)
    ax.set_ylabel('Density')

def plot_stacked_bars(df_pct, title, size_=(12, 6)):
    """Plot stacked bar chart showing percentage breakdown."""
    ax = df_pct.plot(kind='bar', stacked=True, figsize=size_, color=['#2b5c8f', '#d95f02'])
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Category')
    plt.ylabel('Percentage (%)')
    plt.xticks(rotation=45, ha='right')
    plt.legend(['Retained (0)', 'Churned (1)'], title='Status', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        if height > 5:
            x, y = p.get_xy() 
            ax.text(x + width / 2, y + height / 2, f'{height:.1f}%', ha='center', va='center', color='white', fontweight='bold')
            
    plt.tight_layout()
    plt.show()

# ==========================================
# 2. Data Cleaning & Type Conversion
# ==========================================

print("\n--- Step 1: Converting Data Types ---")

date_cols = ['date_activ', 'date_end', 'date_modif_prod', 'date_renewal']
for col in date_cols:
    if col in client_df.columns:
        client_df[col] = pd.to_datetime(client_df[col])

if 'price_date' in price_df.columns:
    price_df['price_date'] = pd.to_datetime(price_df['price_date'])

if 'has_gas' in client_df.columns and client_df['has_gas'].dtype == 'O':
    client_df['has_gas'] = client_df['has_gas'].map({'t': True, 'f': False})

print("\nClient DF Info Summary:")
print(client_df.info())

# ==========================================
# 3. Target Variable Analysis (Churn Rate)
# ==========================================

print("\n--- Step 2: Analyzing Churn Distribution ---")

churn_counts = client_df['churn'].value_counts(normalize=True) * 100
print(f"Retained (0): {churn_counts.get(0, 0):.2f}%")
print(f"Churned  (1): {churn_counts.get(1, 0):.2f}%")

fig, ax = plt.subplots(figsize=(6, 4))
sns.countplot(x='churn', hue='churn', data=client_df, palette=palette_colors, ax=ax, legend=False)
plt.title("Customer Churn Count & Balance", fontsize=12, fontweight='bold')
plt.xlabel("Churn (0 = Retained, 1 = Churned)")
plt.ylabel("Customer Count")

for p in ax.patches:
    height = p.get_height()
    if height > 0:
        pct = (height / len(client_df)) * 100
        ax.annotate(f'{height:,}\n({pct:.1f}%)', (p.get_x() + p.get_width() / 2., height / 2),
                    ha='center', va='center', color='white', fontweight='bold')

plt.tight_layout()
plt.show()

# ==========================================
# 4. Numerical Feature Distributions
# ==========================================

print("\n--- Step 3: Visualizing Feature Distributions ---")

fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12, 12))

# Log transformation applied for visualization due to severe right-skewness
plot_distribution(client_df.assign(cons_12m_log=np.log1p(client_df['cons_12m'])), 'cons_12m_log', axs[0])
plot_distribution(client_df.assign(forecast_cons_12m_log=np.log1p(client_df['forecast_cons_12m'])), 'forecast_cons_12m_log', axs[1])
plot_distribution(client_df, 'net_margin', axs[2])

plt.tight_layout()
plt.show()

# ==========================================
# 5. Categorical Breakdown vs. Churn
# ==========================================

print("\n--- Step 4: Categorical Feature Analysis ---")

if 'channel_sales' in client_df.columns:
    channel = client_df.groupby(['channel_sales', 'churn'])['id'].count().unstack().fillna(0)
    channel_pct = channel.div(channel.sum(axis=1), axis=0) * 100
    plot_stacked_bars(channel_pct, "Churn Rate by Sales Channel")

# ==========================================
# 6. Pricing Data Aggregation
# ==========================================

print("\n--- Step 5: Pricing Aggregation & Sensitivity Analysis ---")

price_summary = price_df.groupby('id').agg({
    'price_off_peak_var': ['mean', 'min', 'max'],
    'price_peak_var': ['mean', 'min', 'max'],
    'price_off_peak_fix': ['mean', 'min', 'max']
})
price_summary.columns = ['_'.join(col) for col in price_summary.columns]

client_eda_df = client_df.merge(price_summary, on='id', how='left')

print(f"Final Merged Dataset Shape: {client_eda_df.shape}")
print("EDA Step 2 complete! Prepared for Feature Engineering.")