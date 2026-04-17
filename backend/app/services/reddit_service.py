import httpx
import urllib.parse

async def search_reddit_posts(query: str, limit: int = 5):
    """Search Reddit for posts related to the query via pullpush."""
    if not query:
        return []
    
    url = f"https://api.pullpush.io/reddit/search/submission/?q={urllib.parse.quote(query)}&size={limit}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            
            results = []
            posts = data.get("data", [])
            for post in posts:
                title = post.get("title", "")
                selftext = post.get("selftext", "")
                score = post.get("score", 0)
                permalink = post.get("permalink", "")
                
                content = selftext[:500] + "..." if len(selftext) > 500 else selftext
                results.append({
                    "title": title,
                    "content": content,
                    "score": score,
                    "url": f"https://www.reddit.com{permalink}" if permalink else ""
                })
            
            return results
    except Exception as e:
        print(f"Error searching Reddit (via pullpush) for {query}: {e}")
        return []
