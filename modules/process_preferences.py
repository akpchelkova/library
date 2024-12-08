def process_user_preferences(genres, authors, keywords):
    """
    Обрабатывает пользовательские предпочтения.
    :param genres: Список любимых жанров.
    :param authors: Список любимых авторов.
    :param keywords: Список ключевых слов.
    :return: Словарь предпочтений.
    """
    return {
        "genres": set(genre.strip().lower() for genre in genres),
        "authors": set(author.strip().lower() for author in authors),
        "keywords": set(keyword.strip().lower() for keyword in keywords)
    }
