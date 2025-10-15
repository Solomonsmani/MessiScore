from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# --- הגדרות דפדפן ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- מזהי טבלאות לפי קטגוריה ---
table_ids = {
    "stats_standard": "stats_standard",
    "stats_passing": "stats_passing",
    "stats_shooting": "stats_shooting",
    "stats_possession": "stats_possession",
    "stats_gca": "stats_gca",
    "stats_passing_types": "stats_passing_types"
}

# --- מילון כתובות לפי ליגות ---
tables = {
    "England": [
        "https://fbref.com/en/comps/9/stats/Premier-League-Stats",
        "https://fbref.com/en/comps/9/passing/Premier-League-Stats",
        "https://fbref.com/en/comps/9/shooting/Premier-League-Stats",
        "https://fbref.com/en/comps/9/possession/Premier-League-Stats",
        "https://fbref.com/en/comps/9/gca/Premier-League-Stats",
        "https://fbref.com/en/comps/9/passing_types/Premier-League-Stats"
    ],
    "Spain": [
        "https://fbref.com/en/comps/12/stats/La-Liga-Stats",
        "https://fbref.com/en/comps/12/passing/La-Liga-Stats",
        "https://fbref.com/en/comps/12/shooting/La-Liga-Stats",
        "https://fbref.com/en/comps/12/possession/La-Liga-Stats",
        "https://fbref.com/en/comps/12/gca/La-Liga-Stats",
        "https://fbref.com/en/comps/12/passing_types/La-Liga-Stats"
    ],
    "Italy": [
        "https://fbref.com/en/comps/11/stats/Serie-A-Stats",
        "https://fbref.com/en/comps/11/passing/Serie-A-Stats",
        "https://fbref.com/en/comps/11/shooting/Serie-A-Stats",
        "https://fbref.com/en/comps/11/possession/Serie-A-Stats",
        "https://fbref.com/en/comps/11/gca/Serie-A-Stats",
        "https://fbref.com/en/comps/11/passing_types/Serie-A-Stats"
    ],
    "France": [
        "https://fbref.com/en/comps/13/stats/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/passing/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/shooting/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/possession/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/gca/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/passing_types/Ligue-1-Stats"
    ],
    "Germany": [
        "https://fbref.com/en/comps/20/stats/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/passing/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/shooting/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/possession/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/gca/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/passing_types/Bundesliga-Stats"
    ],
    "Netherlands": [
        "https://fbref.com/en/comps/23/stats/Eredivisie-Stats",
        "https://fbref.com/en/comps/23/passing/Eredivisie-Stats",
        "https://fbref.com/en/comps/23/shooting/Eredivisie-Stats",
        "https://fbref.com/en/comps/23/possession/Eredivisie-Stats",
        "https://fbref.com/en/comps/23/gca/Eredivisie-Stats",
        "https://fbref.com/en/comps/23/passing_types/Eredivisie-Stats"
    ],
    "Portugal": [
        "https://fbref.com/en/comps/32/stats/Primeira-Liga-Stats",
        "https://fbref.com/en/comps/32/passing/Primeira-Liga-Stats",
        "https://fbref.com/en/comps/32/shooting/Primeira-Liga-Stats",
        "https://fbref.com/en/comps/32/possession/Primeira-Liga-Stats",
        "https://fbref.com/en/comps/32/gca/Primeira-Liga-Stats",
        "https://fbref.com/en/comps/32/passing_types/Primeira-Liga-Stats"
    ],
    "Argentina": [
        "https://fbref.com/en/comps/21/stats/Primera-Division-Stats",
        "https://fbref.com/en/comps/21/passing/Primera-Division-Stats",
        "https://fbref.com/en/comps/21/shooting/Primera-Division-Stats",
        "https://fbref.com/en/comps/21/possession/Primera-Division-Stats",
        "https://fbref.com/en/comps/21/gca/Primera-Division-Stats",
        "https://fbref.com/en/comps/21/passing_types/Primera-Division-Stats"
    ],
    "Brazil": [
        "https://fbref.com/en/comps/24/stats/Serie-A-Stats",
        "https://fbref.com/en/comps/24/passing/Serie-A-Stats",
        "https://fbref.com/en/comps/24/shooting/Serie-A-Stats",
        "https://fbref.com/en/comps/24/possession/Serie-A-Stats",
        "https://fbref.com/en/comps/24/gca/Serie-A-Stats",
        "https://fbref.com/en/comps/24/passing_types/Serie-A-Stats"
    ],
    "Scotland": [
        "https://fbref.com/en/comps/40/stats/Scottish-Premiership-Stats",
        "https://fbref.com/en/comps/40/passing/Scottish-Premiership-Stats",
        "https://fbref.com/en/comps/40/shooting/Scottish-Premiership-Stats",
        "https://fbref.com/en/comps/40/possession/Scottish-Premiership-Stats",
        "https://fbref.com/en/comps/40/gca/Scottish-Premiership-Stats",
        "https://fbref.com/en/comps/40/passing_types/Scottish-Premiership-Stats"
    ]
}

all_players = []

for league_name, urls in tables.items():
    for url in urls:
        # זיהוי הטבלה לפי URL
        if "/passing/" in url:
            table_id = "stats_passing"
        elif "/shooting/" in url:
            table_id = "stats_shooting"
        elif "/possession/" in url:
            table_id = "stats_possession"
        elif "/gca/" in url:
            table_id = "stats_gca"
        elif "/passing_types/" in url:
            table_id = "stats_passing_types"
        else:
            table_id = "stats_standard"  # URL בסיסי

        print(f"Scraping {league_name} - {table_id}...")
        driver.get(url)
        time.sleep(6)  # המתן לטעינת ה-JS

        try:
            table = driver.find_element(By.ID, table_id)
            html = table.get_attribute("outerHTML")
            df = pd.read_html(html, header=[0,1])[0]
            df["League"] = league_name
            df["Table"] = table_id
            all_players.append(df)
        except Exception as e:
            print(f"❌ Failed to scrape {league_name} [{table_id}]: {e}")

# --- שמירה לקובץ ---
full_df = pd.concat(all_players, ignore_index=True)
full_df.to_csv("fbref_new_players_updated_2024_25.csv", index=False)
driver.quit()

print("✅ Done! Extracted", len(full_df), "rows.")
