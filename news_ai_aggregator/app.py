from flask import Flask, render_template, request, url_for
import scraper
import summarizer
from newspaper import Article

app = Flask(__name__)

# A simple in-memory cache to store article content.
# This avoids re-scraping when a user clicks a headline.
# Key: article_url, Value: {'headline': str, 'text': str}
article_cache = {}

@app.route('/')
def index():
    """
    Displays a list of scraped headlines.
    This populates the cache, so it can be slow on first load.
    """
    print("Fetching headlines for the homepage...")
    try:
        # Scrape the source for a list of article objects
        raw_articles = scraper.scrape_articles()

        headlines = []
        # Process a limited number of articles to keep load times reasonable
        for article_obj in raw_articles[:12]:
            article_url = article_obj.url
            # Don't re-process articles we already have in the cache this session
            if article_url in article_cache:
                details = article_cache[article_url]
            else:
                details = scraper.get_article_details(article_obj)

            if details and details.get('headline') and details.get('text'):
                # Add to headlines for the template
                headlines.append({
                    'headline': details['headline'],
                    'link': url_for('article', url=article_url)
                })
                # Store the full details in the cache
                article_cache[article_url] = details

        print(f"Successfully processed {len(headlines)} headlines.")
        if not headlines:
            return render_template('error.html', message="Could not fetch any headlines. The source website might be blocking requests or has changed its structure.")

        return render_template('index.html', headlines=headlines)

    except Exception as e:
        print(f"An error occurred on the index route: {e}")
        return render_template('error.html', message="An unexpected error occurred while fetching the news.")

@app.route('/article')
def article():
    """
    Displays a summarized version of a single article.
    """
    article_url = request.args.get('url')
    if not article_url:
        return render_template('error.html', message="No article URL was provided."), 400

    # Try to get the article from the cache first
    cached_article = article_cache.get(article_url)
    text_to_summarize = None
    title = "Article"

    if cached_article:
        print(f"Article found in cache: {article_url}")
        title = cached_article['headline']
        text_to_summarize = cached_article['text']
    else:
        # Fallback: if not in cache, scrape it fresh
        print(f"Article not in cache. Scraping fresh: {article_url}")
        try:
            article_obj = Article(article_url)
            details = scraper.get_article_details(article_obj)
            if details and details.get('text'):
                title = details['headline']
                text_to_summarize = details['text']
            else:
                 return render_template('error.html', message="Could not retrieve the article content to summarize."), 404
        except Exception as e:
            print(f"Failed to scrape fresh article: {e}")
            return render_template('error.html', message="An error occurred while trying to retrieve the article."), 404

    print("Summarizing article...")
    summary = summarizer.summarize_text(text_to_summarize)

    return render_template('article.html', title=title, summary=summary)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
