import jmcomic

# Disable downloading behavior for identifying
option = jmcomic.JmOption.default()

# Basic fetch wrapper
def fetch_jm_album(album_id: str):
    try:
        client = option.build_jm_client()
        album = client.get_album_detail(album_id)
        
        tags = []
        if album.tags:
            tags = list(album.tags)
            
        return {
            "id": album.album_id,
            "title": album.title,
            "author": album.author if album.author else "Unknown",
            "description": album.description if album.description else "无简介",
            "tags": tags,
            "cover_url": album.cover_url if hasattr(album, 'cover_url') else ""
        }
    except Exception as e:
        print(f"Error fetching JM album {album_id}: {e}")
        return None
        
def search_jm_albums(query: str):
    try:
        client = option.build_jm_client()
        # client.search_site typically returns a JmSearchPage
        search_page = client.search_site(query)
        results = []
        for album in search_page:
            results.append({
                "id": album.album_id,
                "title": album.title,
                "cover": album.cover_url if hasattr(album, 'cover_url') else ""
            })
        return results
    except Exception as e:
        print(f"Error searching JM for {query}: {e}")
        return []
