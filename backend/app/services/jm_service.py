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
            # 官方移动端API获取评论
            resp = client.req_api(f'/forum?mode=manhua&aid={album_id}&page=1')
            if resp and hasattr(resp, 'res_data') and isinstance(resp.res_data, dict):
                c_list = resp.res_data.get('list', [])
                if c_list:
                    import re as regex
                    parsed_comments = []
                    for c in c_list:
                        raw_text = c.get('content', '')
                        # 去除HTML标签 (例如 <div...>)
                        clean_text = regex.sub(r'<[^>]+>', '', raw_text).strip()
                        if clean_text:
                            parsed_comments.append(clean_text)
                    comments_texts = parsed_comments[:15]
        except Exception as html_ce:
            print(f"Failed to fetch comments via API: {html_ce}")

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
