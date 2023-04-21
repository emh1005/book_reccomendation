import requests
from bs4 import BeautifulSoup
import json
import datetime

def get_goodreads_data(urls, books_data_file):
    '''
    Scrape books from Goodreads lists

    Parameters:
        urls (list): list of urls to scrape
        books_data_file (str): path to save books data

    Returns:
        None
    '''
    books_data = []

    for url in urls:
        page = 1
        while True:
            page_url = f"{url}?page={page}"
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            books = soup.find_all('tr', {'itemtype': 'http://schema.org/Book'})
            if not books:
                break

            for book in books:
                book_url = 'https://www.goodreads.com' + book.find('a', class_='bookTitle')['href']
                books_data.append(book_url)

            page += 1

    with open(books_data_file, 'w') as file:
        json.dump(books_data, file, indent=4)


def get_book_details(books_data_file, books_details_file):
    '''
    Scrape book details from Goodreads

    Parameters:
        books_data_file (str): path to books data
        books_details_file (str): path to save books details

    Returns:
        None
    '''
    
    with open(books_data_file, 'r') as file:
        books_data = json.load(file)

    books_details = []

    for book_data in books_data:
        response = requests.get(book_data)
        soup = BeautifulSoup(response.text, 'html.parser')

        title_elem = soup.find('h1', attrs={'data-testid': 'bookTitle'})
        title = title_elem.text.strip() if title_elem else 'n/a'

        author_elem = soup.find('a', class_='ContributorLink')
        author = author_elem.text.strip() if author_elem else 'n/a'

        cover_div = soup.find('div', class_='BookCover__image')
        cover = cover_div.find('img', class_='ResponsiveImage')['src'] if cover_div else 'n/a'

        rating_elem = soup.find('div', class_='RatingStatistics__rating')
        rating = float(rating_elem.text.strip()) if rating_elem else 'n/a'

        rating_counts_elem = soup.find('span', attrs={'data-testid': 'ratingsCount'})
        rating_counts = int(rating_counts_elem.text.strip().split()[0].replace(',', '')) if rating_counts_elem else 'n/a'

        review_counts_elem = soup.find('span', attrs={'data-testid': 'reviewsCount'})
        review_counts = int(review_counts_elem.text.strip().split()[0].replace(',', '')) if review_counts_elem else 'n/a'

        description_elem = soup.find('div', attrs={'data-testid': 'description'})
        description = description_elem.text.strip() if description_elem else 'n/a'

        genres_elem = soup.find_all('span', class_='BookPageMetadataSection__genreButton')
        genres = [genre.text.strip() for genre in genres_elem] if genres_elem else 'n/a'

        publish_date_elem = soup.find('p', attrs={'data-testid': 'publicationInfo'})
        publish_date_str = publish_date_elem.text.strip() if publish_date_elem else 'n/a'

        try:
            publish_date_str = publish_date_str.split("First published ")[1]
            publish_date = datetime.strptime(publish_date_str, "First published %B %d, %Y").strftime("%B %d, %Y")
        except:
            publish_date = publish_date_str

        book_detail = {
            'Book URL': book_data,
            'Title': title,
            'Author': author,
            'Cover': cover,
            'Rating': rating,
            'Rating Counts': rating_counts,
            'Review Counts': review_counts,
            'Description': description,
            'Genres': genres,
            'Publish Date': publish_date
        }

        books_details.append(book_detail)

    with open(books_details_file, 'w') as file:
        json.dump(books_details, file, indent=4)


def filter_data(books_details_file):
    with open(books_details_file, 'r') as file:
        books_details = json.load(file)

    filtered_books_details = []
    for book_data in books_details:
        rating_counts = book_data['Rating Counts']
        if isinstance(rating_counts, str):
            if 'k' in rating_counts or 'm' in rating_counts or 'N/A' in rating_counts:
                filtered_books_details.append(book_data)
            else:
                rating_counts = int(rating_counts.split()[0].replace(',', ''))

        if isinstance(rating_counts, int) and rating_counts >= 5000:
            filtered_books_details.append(book_data)

        rating = book_data['Rating']
        if isinstance(rating, str):
                rating = float(rating)
        if isinstance(rating, float) and rating >= 3.30:
            filtered_books_details.append(book_data)

    with open(books_details_file, 'w') as file:
        json.dump(filtered_books_details, file, indent=4)



def main():
    books_data_file = 'books_data.json'
    books_details_file = 'books_details.json'

    # Scrape books from Goodreads lists
    urls = ['https://www.goodreads.com/list/show/35080',
        'https://www.goodreads.com/list/show/35177',
        'https://www.goodreads.com/list/show/36647',
        'https://www.goodreads.com/list/show/117146',
        'https://www.goodreads.com/list/show/35708',
        'https://www.goodreads.com/list/show/117368',
        'https://www.goodreads.com/list/show/39332',
        'https://www.goodreads.com/list/show/141035',
        'https://www.goodreads.com/list/show/141034',
        'https://www.goodreads.com/list/show/43804',
        'https://www.goodreads.com/list/show/143500',
        'https://www.goodreads.com/list/show/5']
    get_goodreads_data(urls, books_data_file)

    # Scrape details of books from Goodreads
    get_book_details(books_data_file, books_details_file)

    # Filter data
    filter_data(books_details_file)

if __name__ == '__main__':
    main()