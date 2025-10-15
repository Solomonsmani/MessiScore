# MessiScore: Find the Next Messi Using Machine Learning

This project aims to identify the most statistically similar players to Lionel Messi using a combination of unsupervised machine learning and deep learning models applied to detailed player performance metrics.

## Overview

Given a large dataset of professional football players (under age 30) from 10 leading leagues worldwide, the project builds a system that ranks players by how closely their playing style and statistical output resemble Lionel Messi in his recent seasons.

## Features Used

We utilize a comprehensive set of features reflecting attacking and creative play:

* Goals & Assists (per 90 minutes)
* Expected goals (xG), expected assists (xAG), npxG+xAG
* Shot quality and shots on target
* Carries, progressive carries, and touches in key areas
* Passing types: key passes, through balls, switches
* Dribble success, defensive pressure while dribbling
* Progressive actions via passing, carrying, and receiving

## Methodology

The final `FinalScore` is a weighted combination of five similarity measures:

1. **Cosine Similarity** on standardized features (20%)
   Highlights players with proportional stat profiles similar to Messi.

2. **Autoencoder Similarity** in latent space (25%)
   Learns abstract statistical patterns via deep learning and compares player vectors in the compressed space using cosine similarity.

3. **KMeans Score** (35%)
   Players are clustered using KMeans; similarity is based on the distance to the center of Messi’s cluster.

4. **Euclidean Similarity** (10%)
   Measures precise closeness in terms of raw numerical values.

5. **Manhattan Similarity** (10%)
   Emphasizes total absolute differences across features—often surfacing all-around contributors within their teams.

This ensemble approach helps uncover players similar to Messi not just by raw stats, but also by deeper playstyle, contribution, and functional role.

## Files

* `messi_similarity__all_scores_updated.csv`: Final rankings combining all metrics.
* `messi_similarity_cosine_scores_updated.csv`: Cosine similarity on original stats.
* `messi_similarity_autoencoder_scores_updated.csv`: Latent similarity from autoencoder.
* `messi_similarity_kmeans_scores_updated.csv`: Proximity to Messi’s cluster.
* `messi_similarity_full_with_Euclidean_distances_updated.csv`: Rankings by Euclidean similarity.
* `messi_similarity_full_with_Manhattan_distances_updated.csv`: Rankings by Manhattan similarity.

## Example Output: Top 5 Messi-like Players (Updated)

| Player        | Team          | Age | Final Score |
| ------------- | ------------- | --- | ----------- |
| Michael Olise | Bayern Munich | 22  | 0.993       |
| Florian Wirtz | Leverkusen    | 21  | 0.967       |
| Lamine Yamal  | Barcelona     | 17  | 0.910       |
| Rayan Cherki  | Lyon          | 20  | 0.906       |
| Cole Palmer   | Chelsea       | 22  | 0.895       |

## How to Run

1. Make sure your dataset (`fbref_new_players_updated_2024_25.csv`) is in the project directory.
2. Run the main script with Python 3.8+:

   ```bash
   python messi_score.py
   ```

## Requirements

* pandas
* numpy
* tensorflow
* scikit-learn


---

Messi is a one-of-a-kind player. But using the power of data, we just might be able to find echoes of his brilliance in the next generation.
