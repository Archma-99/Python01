import newspaper

# URL provided by the user.
NEWS_URL = "https://www.bbc.com/innovation/technology"

def scrape_articles():
    """
    Scrapes articles from the news source using newspaper3k.
    Returns a list of Article objects.
    """
    print(f"Building news source from: {NEWS_URL}")
    try:
        news_source = newspaper.build(NEWS_URL, memoize_articles=False, request_timeout=15)
        print(f"Found {len(news_source.articles)} articles.")
        return news_source.articles
    except Exception as e:
        print(f"Could not build news source: {e}")
        return []

def get_article_details(article):
    """
    Parses a newspaper Article object to get its title, text, and url.
    """
    try:
        article.download()
        article.parse()
        return {
            'headline': article.title,
            'text': article.text,
            'link': article.url
        }
    except Exception as e:
        # Don't print errors for every article, can be noisy.
        # print(f"Error processing article: {e}")
        return None

if __name__ == '__main__':
    print("Testing the scraper...")
    articles = scrape_articles()
    if articles:
        processed_count = 0
        for article in articles:
            if processed_count >= 5:
                break
            details = get_article_details(article)
            if details and details['text']:
                print(f"\nHeadline: {details['headline']}")
                print(f"Link: {details['link']}")
                print(f"Content Preview: {details['text'][:150]}...")
                processed_count += 1
        if processed_count == 0:
            print("Could not process any articles. The website structure may be incompatible.")
    else:
        print("No articles found. The URL may be incorrect or the site may be blocking requests.")
