import pandas as pd
import numpy as np

from os import path

# Load data

def load_data(file_path):
    assert isinstance(file_path, str), 'Argument {} is not a string'
    assert path.exists(file_path), '{} does not exist'.format(path)

    df = pd.read_csv(file_path)

    return df

def drop_correlated_features(df, threshold=0.99):
    # calculate correlation matrix between columns
    corr_matrix = df.corr()

    # Select upper triangle of correlation matrix
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

    # Find index of feature columns with correlation greater than threshold
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]

    # drop correlated columns
    filtered_df = df.drop(df[to_drop], axis=1)

    return filtered_df

def calculate_correlation_matrix():
    books_df = load_data('data/books.csv')
    tags_df = load_data('data/tags.csv')
    book_tags = load_data('data/book_tags.csv')

    # 99% corr 
    selected_tags = [  236,   240,   248,   251,   254,   261,   272,   509,   617,
              671,   698,   711,   747,   751,   753,   780,   783,   785,
              805,   831,   833,   895,   923,   941,  1010,  1078,  1128,
             1416,  1499,  1540,  1542,  1642,  1659,  1691,  2056,  2271,
             2305,  2538,  2852,  3371,  3379,  3389,  3392,  4615,  5090,
             5207,  5481,  7725,  8055,  8517,  8717,  9221, 10093, 10197,
            10210, 11557, 11590, 11743, 15048, 25149, 25152, 30574, 32586]

    # select only tags used more than 5k times
    tag_counts = pd.merge(book_tags, tags_df, on='tag_id').groupby('tag_id')['count'].sum().sort_values(ascending=False)
    top_tags = tag_counts[tag_counts>5000]

    # apply filter
    filtered_book_tags = book_tags[book_tags['tag_id'].isin(top_tags.index)]

    # aggregate to remove duplicate tags
    grouped_book_tags = filtered_book_tags.groupby(['goodreads_book_id','tag_id'])['count'].sum().reset_index()

    # pivot tables (books x tags)
    pivoted_book_table = grouped_book_tags.pivot('goodreads_book_id','tag_id','count')


    filtered_pivoted_book_table = pivoted_book_table[selected_tags]
    # filtered_pivoted_book_table = drop_correlated_features(pivoted_book_table)

    # change table from count to binary (1 or 0)
    book_tag_table = (filtered_pivoted_book_table>0).astype(int)

    # calculate correlation matrix between books
    correlation_matrix = pd.DataFrame(np.corrcoef(book_tag_table), index=book_tag_table.index\
                                      , columns=book_tag_table.index)

    return correlation_matrix

def save_correlation_matrix(correlation_matrix):
    correlation_matrix.to_csv('data/correlation_matrix.csv')
    return True

# Function to be called outside
def find_k_similar_books(goodreads_book_id, n=20):
    similar_books = list(top_books[str(goodreads_book_id)].iloc[:n])
    filtered_books_df = books_df[books_df['goodreads_book_id'].isin(similar_books)].copy()

    return filtered_books_df.to_dict(orient='records')

# seach title or author name
def book_lookup(search_string, n=20):
    cond1 = books_df['title'].str.lower().str.contains(search_string.lower().replace('+',' '))
    cond2 = books_df['authors'].str.lower().str.contains(search_string.lower())
    return books_df[cond1|cond2].iloc[:n].to_dict(orient='records')

# get top books
def get_top_books(n=20):
    return books_df.sort_values('average_rating',ascending=False).iloc[:n].to_dict(orient='records')

books_df = load_data('data/books.csv')
top_books = pd.read_csv('data/top_books.csv')

# n = 20
# goodreads_book_id = 12609433
# book_recommendations = find_k_similar_books(correlation_matrix, books_df, goodreads_book_id, n)