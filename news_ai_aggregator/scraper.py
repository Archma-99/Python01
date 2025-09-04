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

def _get_best_image_url(article):
    """
    Selects the best possible image URL from an article object by checking
    the top_image and then iterating through all found images.
    """
    # Heuristics for what makes a good image URL
    GOOD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
    BAD_KEYWORDS = ['logo', 'icon', 'avatar', 'profile', 'svg', 'gif', 'badge', 'sponsor', 'placeholder']

    def is_url_good(url):
        if not url or not isinstance(url, str):
            return False

        lower_url = url.lower()
        # Check if it has a good extension
        if not any(ext in lower_url for ext in GOOD_EXTENSIONS):
            return False
        # Check if it contains bad keywords
        if any(keyword in lower_url for keyword in BAD_KEYWORDS):
            return False
        return True

    # 1. Start with top_image, it's often the right one if it's valid.
    if is_url_good(article.top_image):
        return article.top_image

    # 2. If top_image is not good, search all images for a better one.
    if article.imgs:
        for img_url in article.imgs:
            if is_url_good(img_url):
                # Return the first good one found
                return img_url

    # 3. If no good image is found anywhere, return None.
    return None

def get_article_details(article):
    """
    Parses a newspaper Article object to get its title, text, url, and best image.
    """
    try:
        article.download()
        article.parse()

        best_image = _get_best_image_url(article)

        return {
            'headline': article.title,
            'text': article.text,
            'link': article.url,
            'image_url': best_image
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
