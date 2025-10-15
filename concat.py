import pandas as pd

# --- טען את הקובץ עם MultiIndex בעמודות (2 רמות)
df = pd.read_csv("fbref_new_players_updated_2024_25.csv", header=[0, 1])
print(df.columns.tolist())

# --- הגדרת העמודות של שחקן וקבוצה לפי שמות
player_col = ('Unnamed: 1_level_0', 'Player')
squad_col = ('Unnamed: 4_level_0', 'Squad')

# --- קיבוץ לפי שחקן וקבוצה
group_cols = [player_col, squad_col]
exclude_cols = group_cols + [('League', ''), ('Table', '')]
other_cols = [col for col in df.columns if col not in exclude_cols]

# --- קיבוץ ואיחוד שורות כפולות לפי שחקן וקבוצה
df_grouped = df.groupby(group_cols, as_index=False).agg(
    lambda x: x.dropna().iloc[0] if not x.dropna().empty else None
)

# --- סדר עמודות מחדש
ordered_cols = group_cols + [col for col in df_grouped.columns if col not in group_cols]
df_grouped = df_grouped[ordered_cols]

# --- שמירה לקובץ CSV (עם איחוד שמות עמודות לצורך שמירה)
df_grouped.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df_grouped.columns]
df_grouped.to_csv("fbref_new_players_updated_2024_25.csv", index=False, encoding="utf-8-sig")

print(f"✅ Done! Created file with {len(df_grouped)} unique players.")
