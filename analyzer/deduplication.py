from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.post import ScoredPost

def deduplicate_posts(posts: List[ScoredPost], similarity_threshold: float = 0.85) -> List[ScoredPost]:
    """
    Filter out duplicate or near-identical posts using TF-IDF cosine similarity.
    Keeps the highest trend-scored post when duplicates are found.
    """
    if len(posts) <= 1:
        return posts

    # Sort posts by trend score descending so we keep the highest quality version
    sorted_posts = sorted(posts, key=lambda x: x.trend_score, reverse=True)
    texts = [p.text for p in sorted_posts]

    try:
        vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
        tfidf_matrix = vectorizer.fit_transform(texts)
        sim_matrix = cosine_similarity(tfidf_matrix)

        unique_posts: List[ScoredPost] = []
        visited = set()

        for i in range(len(sorted_posts)):
            if i in visited:
                continue
            unique_posts.append(sorted_posts[i])
            for j in range(i + 1, len(sorted_posts)):
                if sim_matrix[i, j] >= similarity_threshold:
                    visited.add(j)

        return unique_posts
    except Exception:
        # Fallback if text processing fails
        return sorted_posts
