from flask import Flask, render_template, request, jsonify
import asyncpg
import asyncio

app = Flask(__name__)

DATABASE_URL = "postgresql://travldev:jFXpjhll6SbCrhxKuJR7YFay6V9kV7tf@dpg-cupkr01opnds739655i0-a.oregon-postgres.render.com/travldb"

async def save_to_db(user_id, name, email):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("INSERT INTO users (user_id, name, email) VALUES ($1, $2, $3) ON CONFLICT (user_id) DO UPDATE SET name=$2, email=$3", user_id, name, email)
    await conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    user_id = data.get("userId")
    name = data.get("name")
    email = data.get("email")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(save_to_db(user_id, name, email))

    return jsonify({"message": "Form submitted successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
