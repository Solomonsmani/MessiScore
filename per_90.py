import pandas as pd
import numpy as np

# טען את הנתונים
df = pd.read_csv("fbref_new_players_updated_2024_25.csv")

# ודא שהעמודה מספרית
df["Playing Time_90s"] = pd.to_numeric(df["Playing Time_90s"], errors="coerce").fillna(0)

# רשימת העמודות שרוצים להמיר לפר 90 דקות
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

# הפוך את העמודות למספריות ואז צור פר90
for col in features_to_convert:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    new_col = col + "_per90"
    
    # אתחול לעמודת פר90 כסוג float
    df[new_col] = 0.0

    # מסכה לתנאי בטוח לחלוקה
    valid_mask = df["Playing Time_90s"] > 0

    # חישוב הבטוח
    df.loc[valid_mask, new_col] = df.loc[valid_mask, col] / df.loc[valid_mask, "Playing Time_90s"]

# שמור לקובץ חדש
df.to_csv("fbref_new_players_updated_2024_25_with_per90.csv", index=False)
print("✅ Done!")
