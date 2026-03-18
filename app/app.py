
from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "salesken"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "secret"),
        connect_timeout=3
    )

def wait_for_db():
    retries = 10
    while retries > 0:
        try:
            conn = get_db()
            conn.close()
            print("Database is ready!")
            return
        except Exception as e:
            print(f"Database not ready, retrying... ({retries} left)")
            retries -= 1
            time.sleep(3)
    print("Could not connect to DB - starting anyway")

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "DevOps Project 1 - Running!",
        "service": "salesken-demo-app"
    })

@app.route("/health")
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": str(e)}), 500

@app.route("/visits")
def visits():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                visited_at TIMESTAMP DEFAULT NOW()
            );
        """)
        cur.execute("INSERT INTO visits DEFAULT VALUES;")
        cur.execute("SELECT COUNT(*) FROM visits;")
        count = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"total_visits": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    wait_for_db()
    app.run(host="0.0.0.0", port=5000, debug=True)

