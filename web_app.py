import streamlit as st
from modules.load_data import load_books
from modules.process_preferences import process_user_preferences
from modules.recommendation import recommend_books
import json

# Загрузка базы данных книг.
books = load_books("data/books.json")

# Заголовок приложения.
st.title("Рекомендательная система книг 📚")
st.subheader("Введите свои предпочтения и получите рекомендации!")

# Проверка инициализации состояния для рекомендаций и выбранных книг.
if "recommendations" not in st.session_state:
    st.session_state["recommendations"] = None
if "selected_books" not in st.session_state:
    st.session_state["selected_books"] = []

# Форма для ввода предпочтений.
with st.form("preferences_form"):
    genres = st.text_input("Любимые жанры (через запятую):", value="")
    authors = st.text_input("Любимые авторы (через запятую):", value="")
    keywords = st.text_input("Ключевые слова (через запятую):", value="")
    min_year = st.number_input("Минимальный год выпуска:", min_value=0, value=1900)
    max_year = st.number_input("Максимальный год выпуска:", min_value=0, value=2024)
    strict_genres = st.checkbox("Фильтровать только по указанным жанрам")  # Новый чекбокс
    sort_by = st.selectbox("Сортировать рекомендации по:", ["Рейтингу", "Алфавиту", "Году выпуска"])
    submit_button = st.form_submit_button("Рекомендовать")

# Обработка данных и генерация рекомендаций.
if submit_button:
    preferences = process_user_preferences(
        genres.split(",") if genres else [],
        authors.split(",") if authors else [],
        keywords.split(",") if keywords else []
    )

    # Применение фильтров.
    filters = {"year": {"min_year": min_year, "max_year": max_year}}

    # Определение метода сортировки.
    sort_map = {"Рейтингу": "score", "Алфавиту": "title", "Году выпуска": "year"}
    sort_field = sort_map[sort_by]

    # Генерация рекомендаций.
    recommendations = recommend_books(books, preferences, filters=filters, sort_by=sort_field)

    if recommendations.empty:
        st.warning("К сожалению, по вашему запросу ничего не найдено.")
    else:
        st.session_state["recommendations"] = recommendations
        st.success("Рекомендации сгенерированы!")

# Если есть рекомендации, отображаем таблицу.
if st.session_state["recommendations"] is not None:
    recommendations = st.session_state["recommendations"].copy()

    # Исправляем формат года.
    recommendations["year"] = recommendations["year"].astype(int).astype(str)

    st.write("### Список рекомендаций:")
    st.dataframe(recommendations[['title', 'author', 'genre', 'year', 'score']])

    # Кнопки для сохранения списка рекомендаций.
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Сохранить рекомендации в CSV"):
            recommendations.to_csv("recommendations.csv", index=False, encoding="utf-8")
            st.success("Рекомендации сохранены в 'recommendations.csv'.")
    with col2:
        if st.button("Сохранить рекомендации в JSON"):
            recommendations_json = recommendations.to_dict(orient="records")
            with open("recommendations.json", "w", encoding="utf-8") as f:
                json.dump(recommendations_json, f, ensure_ascii=False, indent=4)
            st.success("Рекомендации сохранены в 'recommendations.json'.")

    # Добавление интерактивности для выбора книг.
    st.write("### Выберите книги для 'Списка прочитать':")
    selected_books = st.multiselect(
        "Выберите книги:",
        options=recommendations["title"].tolist(),
        default=st.session_state["selected_books"]
    )

    # Обновление выбранных книг в состоянии.
    st.session_state["selected_books"] = selected_books

    # Если выбраны книги, показываем их и добавляем возможность сохранить.
    if st.session_state["selected_books"]:
        reading_list = recommendations[recommendations["title"].isin(st.session_state["selected_books"])]

        st.write("### Ваш 'Список прочитать':")
        st.dataframe(reading_list[['title', 'author', 'genre', 'year']])

        # Кнопки для сохранения выбранных книг.
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Сохранить 'Список прочитать' в CSV"):
                reading_list.to_csv("reading_list.csv", index=False, encoding="utf-8")
                st.success("Список сохранен в 'reading_list.csv'.")
        with col2:
            if st.button("Сохранить 'Список прочитать' в JSON"):
                reading_list_json = reading_list.to_dict(orient="records")
                with open("reading_list.json", "w", encoding="utf-8") as f:
                    json.dump(reading_list_json, f, ensure_ascii=False, indent=4)
                st.success("Список сохранен в 'reading_list.json'.")
