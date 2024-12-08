def calculate_match_score(book, preferences):
    """
    Рассчитывает рейтинг соответствия книги предпочтениям пользователя.
    """
    score = 0
    # Совпадение по жанрам.
    if book['genre'].lower() in preferences['genres']:
        score += 2
    # Совпадение по автору.
    if book['author'].lower() in preferences['authors']:
        score += 3
    # Совпадение по ключевым словам.
    for keyword in preferences['keywords']:
        if keyword in book['description'].lower():
            score += 1
    return score


def recommend_books(books_df, preferences, filters=None, sort_by="score"):
    """
    Генерирует список рекомендаций на основе предпочтений пользователя.
    :param books_df: DataFrame с информацией о книгах.
    :param preferences: Словарь предпочтений пользователя.
    :param filters: Фильтры для рекомендаций (например, минимальный год, строгие жанры).
    :param sort_by: Поле для сортировки результатов.
    :return: Отсортированный DataFrame с рекомендациями.
    """
    # Рассчитываем рейтинг для каждой книги.
    books_df['score'] = books_df.apply(lambda book: calculate_match_score(book, preferences), axis=1)

    # Исключаем книги с рейтингом 0.
    books_df = books_df[books_df['score'] > 0]

    # Применение фильтров.
    if filters:
        # Фильтр по жанрам.
        if 'genres' in filters and preferences['genres']:
            if filters.get('strict_genres', False):
                # Если включен строгий режим, исключаем книги с неподходящими жанрами.
                books_df = books_df[books_df['genre'].str.lower().isin(preferences['genres'])]

        # Фильтр по годам.
        if 'year' in filters:
            if 'min_year' in filters['year']:
                books_df = books_df[books_df['year'] >= filters['year']['min_year']]
            if 'max_year' in filters['year']:
                books_df = books_df[books_df['year'] <= filters['year']['max_year']]

    # Сортировка.
    if sort_by == "score":
        books_df = books_df.sort_values(by='score', ascending=False)
    elif sort_by == "title":
        books_df = books_df.sort_values(by='title')
    elif sort_by == "year":
        books_df = books_df.sort_values(by='year', ascending=False)

    return books_df
