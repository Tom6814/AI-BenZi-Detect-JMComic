import jmcomic

# Disable downloading behavior for identifying
option = jmcomic.JmOption.default()

# Basic fetch wrapper
def fetch_jm_album(album_id: str):
    try:
        client = option.build_jm_client()
        
        # 1. 获取本子详情 (标题, 标签, 简介, 作者, 封面)
        album = client.get_album_detail(album_id)

        tags = []
        if album.tags:
            tags = list(album.tags)
            
        authors = []
        if hasattr(album, 'author_list') and album.author_list:
            authors = list(album.author_list)
        elif album.author:
            authors = [album.author]
            
        author_str = ", ".join(authors) if authors else "Unknown"

        # 2. 获取评论 (获取前20-25条，选取点赞最高的前10条)
        comments_texts = []
        try:
            # 尝试调用 jmcomic 的评论获取接口（如果存在）。
            # 注意：jmcomic 最新版本的 client 可能包含 get_album_comment 或类似方法。
            # 这里以目前普遍支持的写法为例：
            comment_res = client.get_album_comment(album_id)
            # 假设返回的是一个评论对象列表，每个对象有 content/text 和 likes/zan 属性
            if comment_res:
                # 转为字典方便排序
                parsed_comments = []
                for c in comment_res:
                    text = getattr(c, 'content', getattr(c, 'text', str(c)))
                    likes = getattr(c, 'likes', getattr(c, 'zan', 0))
                    try:
                        likes = int(likes)
                    except:
                        likes = 0
                    parsed_comments.append({"text": text, "likes": likes})
                
                # 按点赞数降序排序，取前10条
                parsed_comments.sort(key=lambda x: x["likes"], reverse=True)
                top_10 = parsed_comments[:10]
                comments_texts = [c["text"] for c in top_10]
        except Exception as ce:
            print(f"Failed to fetch or parse comments for {album_id}: {ce}")
            comments_texts = []

        return {
            "id": album.album_id,
            "title": album.title,
            "author": author_str,
            "description": album.description if album.description else "无简介",
            "tags": tags,
            "cover_url": album.cover_url if hasattr(album, 'cover_url') else "",
            "comments": comments_texts
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
