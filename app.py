# app.py

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# ============================================
#  Зберігання в пам'яті: список словників і лічильник ID
# ============================================
books = []
next_id = 1

def get_new_id():
    global next_id
    cur_id = next_id
    next_id += 1
    return cur_id

# ============================================
#  1) Отримання всіх книг:
#     GET /api/values/GetBooks
# ============================================
@app.route("/api/values/GetBooks", methods=["GET"])
def get_books():
    # Повертаємо поточний список книг у форматі JSON
    return jsonify(books), 200


# ============================================
#  2) Додавання однієї книги:
#     POST /api/values/PostAddOneBook
#     JSON-формат: { "title": "...", "author": "...", "year": 2020 }
# ============================================
@app.route("/api/values/PostAddOneBook", methods=["POST"])
def post_add_one_book():
    data = request.get_json()
    if not data:
        # Якщо тiло запиту не містить JSON, повертаємо помилку
        return jsonify({"error": "Відсутнє JSON-тiло"}), 400

    title = data.get("title")
    author = data.get("author")
    year = data.get("year")

    # Перевіряємо, чи вказані обов'язкові поля title та author
    if not title or not author:
        return jsonify({"error": "Поля 'title' та 'author' є обов'язковими"}), 400

    try:
        # Якщо year вказано, перетворюємо його на ціле число
        year_int = int(year) if year is not None else None
    except (ValueError, TypeError):
        return jsonify({"error": "Поле 'year' повинно бути цілим числом"}), 400

    # Створюємо нову книгу і додаємо до списку
    new_book = {
        "id": get_new_id(),
        "title": title,
        "author": author,
        "year": year_int
    }
    books.append(new_book)
    return jsonify(new_book), 201


# ============================================
#  3) Видалення однієї книги:
#     DELETE /api/values/<int:id>
#     Наприклад: DELETE /api/values/8
# ============================================
@app.route("/api/values/<int:id>", methods=["DELETE"])
def delete_one_book(id):
    global books
    # Шукаємо книгу за id у списку
    for idx, book in enumerate(books):
        if book["id"] == id:
            # Якщо знайдено, видаляємо її й повертаємо повідомлення
            books.pop(idx)
            return jsonify({"message": f"Книгу з id={id} видалено"}), 200
    # Якщо не знайдено, повертаємо помилку 404
    return jsonify({"error": f"Книга з id={id} не знайдена"}), 404


# ============================================
#  Запуск застосунку (точка входу)
#  Використовуємо порт із змінної середовища PORT (для Render)
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Прив’язка до 0.0.0.0, щоб доступно було ззовні
    app.run(host="0.0.0.0", port=port)
