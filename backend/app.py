from flask import Flask, request
import pymysql
app = Flask(__name__)


def get_database_connection():
    return pymysql.connect(host="localhost", user="root", password="", database="subjects")

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/", methods=["GET"])
def get_all_scp_data():
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sub")
    rows = cur.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "item": row[1],
            "class": row[2],
            "description": row[3],
            "containment": row[4]
        })
    return {"scp data": data}

@app.route("/scp/<int:id>", methods=["GET"])
def get_scp_by_id(id):
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sub WHERE id=%s", (id,))
    row = cur.fetchone()
    conn.close()

    if row:
        return {"scp data": {
            "id": row[0],
            "item": row[1],
            "class": row[2],
            "description": row[3],
            "containment": row[4]
        }}
    else:
        return "SCP ID not found"

@app.route("/scp", methods=["POST"])
def add_scp():
    data = request.get_json()
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO sub (item, class, description, containment) VALUES (%s, %s, %s, %s)",
                (data["item"], data["class"], data["description"], data["containment"]))
    conn.commit()
    conn.close()
    return "SCP added successfully"

@app.route("/scp/<int:id>", methods=["PUT"])
def update_scp(id):
    data = request.get_json()
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("UPDATE sub SET item=%s, class=%s, description=%s, containment=%s WHERE id=%s",
                (data["item"], data["class"], data["description"], data["containment"], id))
    conn.commit()
    conn.close()
    return "SCP updated successfully"

@app.route("/scp/<int:id>", methods=["DELETE"])
def delete_scp(id):
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM sub WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return "SCP deleted successfully"

if __name__ == "__main__":
    app.run(debug=True)
