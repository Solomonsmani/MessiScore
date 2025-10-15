import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv("fbref_new_players_updated_2024_25.csv")

# Ensure the column is numeric
df["Playing Time_90s"] = pd.to_numeric(df["Playing Time_90s"], errors="coerce").fillna(0)

# List of features to convert to per 90 minutes
features_to_convert = [
    "Take-Ons_Succ",
    "Touches_Att Pen",
    "Touches_Att 3rd",
    "Unnamed: 28_level_0_PPA",
    "Unnamed: 27_level_0_1/3",
    "Pass Types_TB",
    "Pass Types_Sw",
    "Unnamed: 26_level_0_KP",
    "Carries_Carries",
    "Carries_TotDist",
    "Carries_PrgDist",
    "Carries_1/3",
    "Carries_CPA",
    "Progression_PrgC",
    "Progression_PrgP",
    "Progression_PrgR"
]

# Convert columns to numeric and then create per90 versions
for col in features_to_convert:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    new_col = col + "_per90"
    
    # Initialize the per90 column as float
    df[new_col] = 0.0

    # Mask to avoid division by zero
    valid_mask = df["Playing Time_90s"] > 0

    # Safe calculation of per90 values
    df.loc[valid_mask, new_col] = df.loc[valid_mask, col] / df.loc[valid_mask, "Playing Time_90s"]

# Save to a new CSV file
df.to_csv("fbref_new_players_updated_2024_25_with_per90.csv", index=False)
print("✅ Done!")
