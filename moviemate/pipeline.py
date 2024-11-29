import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


class Pipeline:
    def __init__(self, ratings_path, items_path=None, users_path=None):
        self.ratings_path = ratings_path
        self.items_path = items_path
        self.users_path = users_path
        self.ratings_df = None
        self.items_df = None
        self.users_df = None

    def load_dataset(self):
        self.ratings_df = pd.read_csv(
            self.ratings_path, sep='\t',
            names=['user_id', 'item_id', 'rating', 'timestamp']
        )

        self.ratings_df['timestamp'] = pd.to_datetime(self.ratings_df['timestamp'], unit='s')

        if self.items_path:
            self.items_df = pd.read_csv(
                self.items_path, sep='|', encoding='latin-1', header=None,
                names=[
                    'item_id', 'title', 'release_date', 'video_release_date', 'IMDb_URL',
                    'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy',
                    'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                    'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
                ]
            )
            self.items_df['genres'] = self.items_df.iloc[:, 5:].apply(
                lambda x: ','.join(x.index[x == 1]), axis=1
            )

        if self.users_path:
            self.users_df = pd.read_csv(
                self.users_path, sep='|', header=None,
                names=['user_id', 'age', 'gender', 'occupation', 'zip_code']
            )

    def partition_data(self, partition_type='user_stratified', test_size=0.2):
        if self.ratings_df is None:
            raise ValueError("Dataset not loaded. Call `load_dataset()` first.")

        if partition_type == 'user_stratified':
            # User-stratified sampling
            gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=42)
            train_idx, test_idx = next(gss.split(self.ratings_df, groups=self.ratings_df['user_id']))
            train_df = self.ratings_df.iloc[train_idx]
            test_df = self.ratings_df.iloc[test_idx]

        elif partition_type == 'temporal':
            # Temporal sampling
            sorted_ratings = self.ratings_df.sort_values(by='timestamp')
            split_idx = int(len(sorted_ratings) * (1 - test_size))
            train_df = sorted_ratings.iloc[:split_idx]
            test_df = sorted_ratings.iloc[split_idx:]

        else:
            raise ValueError("Invalid partition_type. Choose 'user_stratified' or 'temporal'.")

        return train_df, test_df
