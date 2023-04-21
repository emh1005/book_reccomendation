import json
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt

# Define the path to the cache file
CACHE_PATH = 'book_graph.json'

# Load the book data
with open('book_details.json', 'r') as f:
    books = json.load(f)

def build_graph():
    '''
    Build a graph from the book data
    
    Parameters:
    books (list): list of book objects
        
    Returns:
    G (networkx.Graph): graph of books and their similarities
    '''
    # Create a new graph
    G = nx.Graph()

    # Add nodes for each book
    for book in books:
        G.add_node(book['Title'], type='book', description=book['Description'])

    # Use TF-IDF to compute the similarities between book descriptions
    descriptions = [book['Description'] for book in books]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(descriptions)
    similarity_matrix = (X * X.T).A

    # Add edges between books based on their genre and description similarities
    for i, book1 in enumerate(books):
        for j, book2 in enumerate(books):
            if i != j:
                genre_similarity = len(set(book1['Genres']).intersection(set(book2['Genres'])))
                description_similarity = similarity_matrix[i][j]
                if genre_similarity > 0 and description_similarity > 0:
                    G.add_edge(book1['Title'], book2['Title'], weight=genre_similarity * description_similarity)
    return G


try:
    with open(CACHE_PATH, 'r') as f:
        G = json_graph.node_link_graph(json.load(f))
except:
    G = build_graph()
    with open(CACHE_PATH, 'w') as f:
        json.dump(json_graph.node_link_data(G), f)
