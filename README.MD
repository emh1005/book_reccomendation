# Book Recommendation System

## Introduction
This code is a book recommendation system that suggests books similar to the input book title. It uses book descriptions and genres to compute the similarity between books and creates a graph of books and their similarities. Based on the input book title, the program finds the most similar books and returns them as recommendations.

## Required Python Packages
The following packages are required to run this program:
networkx
sklearn

## Data Processing
The clean_data.py script scrapes book data from Goodreads lists using beautifulsoup4 library and filters the data based on certain criteria.
The script accesses the data by scraping book data from Goodreads lists. The script uses the requests library to send HTTP requests to the URLs and the beautifulsoup4 library to parse the HTML content of the responses. The script then extracts the URLs of individual book pages and stores them in a list called books_data. The list is saved to a JSON file called books_data.json.

The script then uses the books_data list to scrape book details from individual book pages. The script sends HTTP requests to each book URL in the list and extracts the following attributes for each book:
* Book URL: The URL of the book page on Goodreads.
* Title: The title of the book.
* Author: The name of the author of the book.
* Cover: The URL of the cover image of the book.
* Rating: The average rating of the book on Goodreads.
* Rating Counts: The number of ratings for the book on Goodreads.
* Review Counts: The number of reviews for the book on Goodreads.
* Description: The description of the book on Goodreads.
* Genres: A list of the genres of the book on Goodreads.
* Publish Date: The publish date of the book.

The script then filters the book data based on the following criteria:
* Rating Counts is greater than or equal to 5000.
* Rating is greater than or equal to 3.30.
The filtered book data is saved to the same JSON file, books_details.json.

## Data Sturcture
This code builds a graph data structure to represent books and their relationships based on their genres and descriptions.

The graph is built using the NetworkX library in Python, and the data is stored as nodes and edges. Each book is represented as a node, with the book's title as its label, and its description and type as additional attributes. The type attribute is used to differentiate book nodes from other types of nodes that might be added to the graph.

Edges are added between books based on their similarity in genres and descriptions. The weight of each edge is computed as the product of the genre similarity and description similarity between the two books. This weight indicates the strength of the relationship between the two books.

The TF-IDF algorithm is used to compute the similarity between the book descriptions. The algorithm processes the descriptions and creates a vector representation for each one. The vectors are then compared to compute the similarity matrix.

Finally, the graph is returned as a NetworkX object, which can be further processed or analyzed as needed. Additionally, the graph can be saved in JSON format using the json_graph library to enable sharing or further analysis.

## Instruction to Run the Program
1. Clone the repository or download the code files
2. Make sure that the required Python packages are installed
3. Download the book_details.json file and place it in the same directory as the code files
4. Run the book_recommendation.py file using the command python book_recommendation.py
5. Enter a book title when prompted, or enter "exit" to quit the program

Note: The book_graph.json file is used to cache the computed graph. If it exists, the program loads the graph from the file instead of computing it again. If you want to rebuild the graph, delete the book_graph.json file.

## Interacting with the Program
1. When you run the program, you will be prompted to enter a book title. Enter the title of the book for which you want to get recommendations.
2. The program will return a list of 5 recommended books similar to the input book. Each book includes the title, author, description, rating, and publish date.
3. You can enter another book title to get more recommendations, or enter "exit" to quit the program.