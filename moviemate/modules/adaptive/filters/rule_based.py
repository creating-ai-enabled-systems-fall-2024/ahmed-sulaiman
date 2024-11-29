import pandas as pd


class RuleBasedRecommender:
    def __init__(self, ratings_df, items_df):
        self.ratings_df = ratings_df
        self.items_df = items_df

    def recommend_top_movies(self, n=10):
        top_movies = (
            self.ratings_df.groupby('item_id')['rating'].mean()
            .sort_values(ascending=False)
            .head(n)
            .reset_index()
        )
        top_movies = top_movies.merge(self.items_df[['item_id', 'title']], on='item_id')
        return top_movies

    def recommend_by_genre(self, genre, n=10):
        if genre not in self.items_df.columns:
            raise ValueError(f"Genre '{genre}' not found in items metadata.")

        genre_movies = self.items_df[self.items_df[genre] == 1]
        genre_ratings = (
            self.ratings_df[self.ratings_df['item_id'].isin(genre_movies['item_id'])]
            .groupby('item_id')['rating']
            .mean()
            .sort_values(ascending=False)
            .head(n)
            .reset_index()
        )
        genre_ratings = genre_ratings.merge(
            self.items_df[['item_id', 'title']], on='item_id'
        )
        return genre_ratings

    def evaluate_top_n(self, test_df, n=10):
        top_movies = self.recommend_top_movies(n=n)['item_id'].tolist()
        
        relevant_items = test_df[test_df['rating'] >= 4]['item_id'].unique()
        recommended_relevant = [item for item in top_movies if item in relevant_items]
        
        precision_at_n = len(recommended_relevant) / len(top_movies)
        recall_at_n = len(recommended_relevant) / len(relevant_items)
        return {"Precision@N": precision_at_n, "Recall@N": recall_at_n}
