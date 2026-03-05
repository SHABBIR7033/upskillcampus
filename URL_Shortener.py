from flask import Flask, redirect, request, render_template_string
import sqlite3
import string
import random

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect("urls.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS url_map (
            short_url TEXT PRIMARY KEY,
            long_url TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None
    if request.method == "POST":
        long_url = request.form["long_url"]

        if not long_url.startswith("http"):
            return "Invalid URL format"

        conn = sqlite3.connect("urls.db")
        cur = conn.cursor()

        short_url = generate_short_url()
        cur.execute("INSERT INTO url_map VALUES (?, ?)", (short_url, long_url))

        conn.commit()
        conn.close()

        short_url = request.host_url + short_url

    return render_template_string("""
        <h2>URL Shortener</h2>
        <form method="post">
            <input type="text" name="long_url" placeholder="Enter Long URL" required>
            <button type="submit">Shorten</button>
        </form>
        {% if short_url %}
            <p>Short URL: <a href="{{ short_url }}">{{ short_url }}</a></p>
        {% endif %}
    """, short_url=short_url)

@app.route("/<short_url>")
def redirect_url(short_url):
    conn = sqlite3.connect("urls.db")
    cur = conn.cursor()

    cur.execute("SELECT long_url FROM url_map WHERE short_url = ?", (short_url,))
    result = cur.fetchone()

    conn.close()

    if result:
        return redirect(result[0])
    else:
        return "URL not found"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
