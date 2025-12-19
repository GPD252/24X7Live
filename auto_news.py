import os
import google.generativeai as genai
from newspaper import Article
import requests

# AI and News Settings
GENAI_KEY = os.environ["GEMINI_API_KEY"]
NEWS_KEY = "AIzaSyAVFArQcaavFJC4X3r_3-DEnonXdAvBqgs" # Enter your NewsAPI key here
genai.configure(api_key=GENAI_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_trending_news():
    # Fetch today's trending technology news
    url = f"newsapi.org{NEWS_KEY}"
    response = requests.get(url).json()
    articles = response.get('articles', [])
    return [a['url'] for a in articles[:5]] # Only top 5 news links

def fetch_and_rewrite(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        # AI Rewrite Logic
        prompt = f"Rewrite this news in professional style for my news blog. Remove all original links. Make it unique for SEO. Content: {article.text}"
        response = model.generate_content(prompt)
        
        # Create Markdown File (for Hugo)
        safe_title = article.title[:30].replace(' ', '-').replace('/', '-')
        filename = f"content/posts/{safe_title}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"---\ntitle: \"{article.title}\"\ndate: 2025-12-19\ndraft: false\n---\n")
            f.write(response.text)
        print(f"Success: {article.title}")
    except Exception as e:
        print(f"Error processing {url}: {e}")

# Main execution
if __name__ == "__main__":
    links = get_trending_news()
    for link in links:
        fetch_and_rewrite(link)
