import pandas as pd
import networkx as nx
import random

# Load datasets
books_df = pd.read_csv("large_books.csv")
ratings_df = pd.read_csv("large_ratings.csv")

# Create a bipartite graph
G = nx.Graph()

# Add users and books as nodes
users = ratings_df["user_id"].unique()
books = books_df["book_id"].unique()

G.add_nodes_from(users, bipartite=0)  # User nodes
G.add_nodes_from(books, bipartite=1)  # Book nodes

# Add weighted edges (ratings as weights)
edges = list(zip(ratings_df["user_id"], ratings_df["book_id"], ratings_df["rating"]))
G.add_weighted_edges_from(edges)

# Function to perform random walk with restart
def random_walk(graph, start_user, steps=50, restart_prob=0.3):
    current_node = start_user
    visited_books = []

    for _ in range(steps):
        neighbors = list(graph.neighbors(current_node))
        if not neighbors:
            break  # Stop if no connections

        if random.random() < restart_prob:
            current_node = start_user  # Restart walk
        else:
            current_node = random.choices(neighbors, weights=[graph[current_node][n]['weight'] for n in neighbors])[0]

        if current_node in books:  # Record only book visits
            visited_books.append(current_node)

    return visited_books

# Function to get top recommended books for a user
def get_recommendations(user_id, top_n=10):
    walked_books = random_walk(G, user_id, steps=100)
    book_counts = {book: walked_books.count(book) for book in set(walked_books)}
    
    # Sort books by visit frequency
    recommended_books = sorted(book_counts, key=book_counts.get, reverse=True)[:top_n]

    # Retrieve book details
    recommended_books_df = books_df[books_df["book_id"].isin(recommended_books)][["book_id", "title", "authors", "average_rating"]]
    
    return recommended_books_df

# Example: Get recommendations for a user
user_id = ratings_df["user_id"].sample(1).iloc[0]  # Pick a random user
recommendations = get_recommendations(user_id)
print(f"Recommended books for User {user_id}:\n", recommendations)

