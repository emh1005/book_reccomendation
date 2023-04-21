import json
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from networkx.readwrite import json_graph

# Define the path to the cache file
CACHE_PATH = 'book_graph.json'

# Load the book data
with open('book_details.json', 'r') as f:
    books = json.load(f)

def build_graph(books):
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

# Load the graph from the cache file if it exists, otherwise build the graph and save it to the cache file
try:
    with open(CACHE_PATH, 'r') as f:
        G = json_graph.node_link_graph(json.load(f))
except:
    G = build_graph(books)
    with open(CACHE_PATH, 'w') as f:
        json.dump(json_graph.node_link_data(G), f)



def recommend_book(book_title, num_recommendations=5):
    '''
    Recommend books based on the input book title

    Parameters:
    book_title (str): title of the book to recommend similar books for
    num_recommendations (int): number of recommendations to return

    Returns:
    top_recommendations (list): list of recommended book titles
    '''
    
    # Get the neighbors of the book
    neighbors = list(G.neighbors(book_title))
    # Get the neighbors of the neighbors, excluding the book itself
    recommended_books = []
    for neighbor in neighbors:
        if G.nodes[neighbor]['type'] == 'book':
            recommended_books.extend(list(G.neighbors(neighbor)))
    recommended_books = [b for b in recommended_books if b != book_title]
    # Rank the recommended books by the edge weights between them and the input book
    rankings = {}
    for book in recommended_books:
        if G.has_edge(book_title, book):
            rankings[book] = G[book_title][book]['weight']
    sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
    top_recommendations = [book for book, _ in sorted_rankings][:num_recommendations]
    # return top_recommendations
       # Extract the book objects from the books list based on the recommended book titles
    recommended_books_json = []
    for book_title in top_recommendations:
        for book in books:
            if book['Title'] == book_title:
                recommended_books_json.append(book)
                break

    # Convert the list of book objects to a JSON object and return it
    return recommended_books_json

def main():
    title = input('Enter a book title, or "exit" to quit: ')
    
    while title != 'exit':
        try:
            # Get the recommended books
            results = recommend_book(title)

            # Print the results
            for book in results:
                print('---------------------')
                print(f"{book['Title']} by {book['Author']}")
                print(book['Description'])
                print(f"Rating: {book['Rating']} stars")
                print(f"Publish Date: {book['Publish Date']}")
                print('')

            title = input('Enter a book title, or "exit" to quit: ')
        except:
            print('Book not found')
            title = input('Enter a book title, or "exit" to quit: ')
        
if __name__ == '__main__':
    main()
