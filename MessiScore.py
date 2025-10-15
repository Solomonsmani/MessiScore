import pandas as pd
import numpy as np
import random
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances, pairwise_distances
from sklearn.cluster import KMeans
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam

# --- Load dataset ---
df = pd.read_csv("fbref_new_players_updated_2024_25.csv", low_memory=False)

# Keep only relevant positions
# positions = ['MF', 'FW', 'CM', 'LM', 'RM', 'WM', 'LW', 'RW', 'AM', 'LB', 'RB', 'FB']
allowed_positions = ['LW', 'RW', 'AM', 'FW']
df = df[df["Unnamed: 3_level_0_Pos"].apply(lambda x: any(pos in x for pos in allowed_positions))]

# --- Features ---
features = [
    "Per 90 Minutes_Gls", "Per 90 Minutes_Ast", "Per 90 Minutes_G+A", "Per 90 Minutes_G-PK",
    "Standard_G/Sh", "Per 90 Minutes_xG", "Per 90 Minutes_xAG", "Per 90 Minutes_npxG+xAG",
    "SCA_SCA90", "GCA_GCA90",
    "Standard_SoT/90", "Take-Ons_Succ","Take-Ons_Succ%", "Take-Ons_Tkld%", "Touches_Att Pen", "Touches_Att 3rd",
    "Unnamed: 28_level_0_PPA", "Unnamed: 27_level_0_1/3","Pass Types_TB", "Pass Types_Sw", "Unnamed: 26_level_0_KP", 
    "Carries_Carries", "Carries_TotDist", "Carries_PrgDist", "Carries_1/3", "Carries_CPA",
    "Progression_PrgC", "Progression_PrgP", "Progression_PrgR",
]


# --- Filter and preprocess ---
df["Playing Time_Min"] = pd.to_numeric(df["Playing Time_Min"], errors='coerce')
df["Playing Time_Starts"] = pd.to_numeric(df["Playing Time_Starts"], errors='coerce')
df["Unnamed: 5_level_0_Age"] = pd.to_numeric(df["Unnamed: 5_level_0_Age"], errors='coerce')

df = df[
    (df["Playing Time_Min"] > 1800) &
    (df["Playing Time_Starts"] >= 20) 
     & (df["Unnamed: 5_level_0_Age"] < 30)
]

# --- Messi's stats ---
messi_row = pd.DataFrame({
    "Per 90 Minutes_Gls": [0.95], "Per 90 Minutes_Ast": [0.43], "Per 90 Minutes_G+A": [1.38], "Per 90 Minutes_G-PK": [0.84],
    "Standard_G/Sh":[0.15], "Per 90 Minutes_xG": [0.64], "Per 90 Minutes_xAG": [0.39], "Per 90 Minutes_npxG+xAG": [0.96],
    "SCA_SCA90": [7.11], "GCA_GCA90": [1.17],
    "Standard_SoT/90": [2.42], "Take-Ons_Succ": [104.77],"Take-Ons_Succ%":[62.9],"Take-Ons_Tkld%":[35.5], "Touches_Att Pen": [142.44],"Touches_Att 3rd": [991.77],
    "Unnamed: 28_level_0_PPA": [93.88], "Unnamed: 27_level_0_1/3":[169.55],"Pass Types_TB":[31.66], "Pass Types_Sw":[12.11], "Unnamed: 26_level_0_KP":[62.44], 
    "Carries_Carries":[1395.11], "Carries_TotDist":[8496.66], "Carries_PrgDist":[4411.33], "Carries_1/3":[124.66], "Carries_CPA":[43.55],
    "Progression_PrgC": [131.22], "Progression_PrgP": [249.11], "Progression_PrgR": [176.11],
    "Unnamed: 1_level_0_Player": ["Lionel Messi"], "Unnamed: 4_level_0_Squad": ["Inter Miami"], "Unnamed: 5_level_0_Age": [38]
})

# --- Prepare data ---
df_features = df[features].apply(pd.to_numeric, errors='coerce').fillna(0)
df_with_messi = pd.concat([df_features, messi_row[features]], ignore_index=True)

# --- Reproducibility ---
seed_value = 42
random.seed(seed_value)
np.random.seed(seed_value)
tf.random.set_seed(seed_value)

# --- Standardize ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_with_messi)

# --- AutoEncoder ---
input_dim = X_scaled.shape[1]
encoding_dim = 10

input_layer = Input(shape=(input_dim,))
encoded = Dense(16, activation='relu')(input_layer)
encoded = Dense(encoding_dim, activation='relu')(encoded)
decoded = Dense(16, activation='relu')(encoded)
decoded = Dense(input_dim, activation='linear')(decoded)

autoencoder = Model(input_layer, decoded)
encoder = Model(input_layer, encoded)
autoencoder.compile(optimizer=Adam(learning_rate=0.01), loss='mse')
autoencoder.fit(X_scaled, X_scaled, epochs=100, batch_size=32, shuffle=True, verbose=0)

# --- Latent space ---
X_latent = encoder.predict(X_scaled)

# --- Remove Messi before similarity computations ---
X_scaled_wo_messi = X_scaled[:-1]
X_latent_wo_messi = X_latent[:-1]
messi_vector = X_scaled[-1].reshape(1, -1)
messi_latent = X_latent[-1].reshape(1, -1)

# --- Similarities ---
cos_sim = cosine_similarity(X_scaled_wo_messi, messi_vector).flatten()
autoencoder_similarities = cosine_similarity(X_latent_wo_messi, messi_latent).flatten()

euclidean_dist = euclidean_distances(X_latent_wo_messi, messi_latent).flatten()
euclidean_sim = 1 - (euclidean_dist / euclidean_dist.max())

manhattan_dist = manhattan_distances(X_latent_wo_messi, messi_latent).flatten()
manhattan_sim = 1 - (manhattan_dist / manhattan_dist.max())

# --- KMeans ---
kmeans = KMeans(n_clusters=14, random_state=42, n_init='auto') 
kmeans_labels = kmeans.fit_predict(X_scaled)
messi_cluster = kmeans_labels[-1]
messi_cluster_center = kmeans.cluster_centers_[messi_cluster]
distances = pairwise_distances(X_scaled[:-1], [messi_cluster_center]).flatten()
kmeans_scores_continuous = 1 - (distances / distances.max())

# --- Normalize to [0, 1] ---
scaler_score = MinMaxScaler()
cos_sim_norm = scaler_score.fit_transform(cos_sim.reshape(-1, 1)).flatten()
autoencoder_similarities_norm = scaler_score.fit_transform(autoencoder_similarities.reshape(-1, 1)).flatten()
kmeans_scores_continuous_norm = scaler_score.fit_transform(kmeans_scores_continuous.reshape(-1, 1)).flatten()
euclidean_sim_norm = scaler_score.fit_transform(euclidean_sim.reshape(-1, 1)).flatten()
manhattan_sim_norm = scaler_score.fit_transform(manhattan_sim.reshape(-1, 1)).flatten()

# --- Final score ---
final_score = (
    0.2 * cos_sim_norm +
    0.25 * autoencoder_similarities_norm +
    0.35 * kmeans_scores_continuous_norm +
    0.1 * manhattan_sim_norm +
    0.1 * euclidean_sim_norm
)

# --- Player Info (excluding Messi) ---
player_info_df = pd.concat([
    df[['Unnamed: 1_level_0_Player', 'Unnamed: 4_level_0_Squad','Unnamed: 5_level_0_Age']],
    messi_row[['Unnamed: 1_level_0_Player', 'Unnamed: 4_level_0_Squad','Unnamed: 5_level_0_Age']]
], ignore_index=True)
player_info_df_wo_messi = player_info_df[:-1]

# --- Result DataFrames ---
df_result = pd.DataFrame({
    'Player': player_info_df_wo_messi['Unnamed: 1_level_0_Player'],
    'Team': player_info_df_wo_messi['Unnamed: 4_level_0_Squad'],
    'Age': player_info_df_wo_messi['Unnamed: 5_level_0_Age'],
    'CosineSimilarity': cos_sim_norm,
    'AutoencoderSimilarity': autoencoder_similarities_norm,
    'KMeansScore': kmeans_scores_continuous_norm,
    'EuclideanSimilarity': euclidean_sim_norm,
    'ManhattanSimilarity': manhattan_sim_norm,
    'FinalScore': final_score
}).sort_values(by='FinalScore', ascending=False).reset_index(drop=True)

# Individual results
cosine_result = df_result[['Player', 'Team', 'Age', 'CosineSimilarity']].sort_values(by='CosineSimilarity', ascending=False)
autoencoder_result = df_result[['Player', 'Team', 'Age', 'AutoencoderSimilarity']].sort_values(by='AutoencoderSimilarity', ascending=False)
kmeans_result = df_result[['Player', 'Team', 'Age', 'KMeansScore']].sort_values(by='KMeansScore', ascending=False)
Euclidean_result = df_result[['Player', 'Team', 'Age', 'EuclideanSimilarity']].sort_values(by='EuclideanSimilarity', ascending=False)
Manhattan_result = df_result[['Player', 'Team', 'Age', 'ManhattanSimilarity']].sort_values(by='ManhattanSimilarity', ascending=False)

# --- Output ---
print("--- Top 10 Players Similar to Messi ---")
print(df_result.head(10))

# --- Save ---
df_result.to_csv("results/messi_similarity__all_scores_updated.csv", index=False, encoding='utf-8-sig')
cosine_result.to_csv("results/messi_similarity_cosine_scores_updated.csv", index=False, encoding='utf-8-sig')
autoencoder_result.to_csv("results/messi_similarity_autoencoder_scores_updated.csv", index=False, encoding='utf-8-sig')
kmeans_result.to_csv("results/messi_similarity_kmeans_scores_updated.csv", index=False, encoding='utf-8-sig')
Euclidean_result.to_csv("results/messi_similarity_full_with_Euclidean_distances_updated.csv", index=False, encoding='utf-8-sig')
Manhattan_result.to_csv("results/messi_similarity_full_with_Manhattan_distances_updated.csv", index=False, encoding='utf-8-sig')
