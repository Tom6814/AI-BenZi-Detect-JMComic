import jmcomic

option = jmcomic.JmOption.default()

def fetch_jm_album(album_id: str):
    try:
        client = option.build_jm_client()
        album = client.get_album_detail(album_id)

        tags = list(album.tags) if album.tags else []
        authors = list(album.author_list) if hasattr(album, 'author_list') and album.author_list else ([album.author] if album.author else [])
        author_str = ", ".join(authors) if authors else "Unknown"

        comments_texts = []
        try:
            from jmcomic.jm_client_impl import JmHtmlClient
            html_client = JmHtmlClient(client.postman, client.get_domain_list())
            html_resp = html_client.get(f'/ajax/comment?aid={album_id}')
            data = html_resp.json()
            if 'data' in data and data['data']:
                parsed_comments = []
                for c in data['data']:
                    text = c.get('comment', '')
                    addtime = int(c.get('addtime', 0)) if str(c.get('addtime', 0)).isdigit() else 0
                    parsed_comments.append({"text": text, "time": addtime})

                parsed_comments.sort(key=lambda x: x["time"], reverse=True)
                top_15 = parsed_comments[:15]
                comments_texts = [c["text"] for c in top_15]
        except Exception as html_ce:
            print(f"Failed to fetch comments via HTML: {html_ce}")

        return {
            "id": album.album_id,
            "title": album.title,
            "author": author_str,
            "description": album.description if album.description else "无简介",
            "tags": tags,
            "cover_url": f"https://{client.domain_list[0]}/media/albums/{album_id}.jpg",
            "comments": comments_texts
        }
    except Exception as e:
        print(f"Error fetching JM album {album_id}: {e}")
        return None

def search_jm_albums(query: str):
    try:
        client = option.build_jm_client()
        search_page = client.search_site(query)
        results = []
        for album_tuple in search_page:
            if isinstance(album_tuple, tuple) and len(album_tuple) == 2:
                album_id, album_info = album_tuple
                title = album_info if isinstance(album_info, str) else getattr(album_info, 'name', '') or getattr(album_info, 'title', '')
                if isinstance(album_info, dict):
                    title = album_info.get('name', album_info.get('title', str(album_info)))
                results.append({
                    "id": album_id,
                    "title": title,
                    "cover": f"https://{client.domain_list[0]}/media/albums/{album_id}.jpg"
                })
        return results
    except Exception as e:
        print(f"Error searching JM for {query}: {e}")
        return []
