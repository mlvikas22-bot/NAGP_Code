from flask import Flask, jsonify
import mysql.connector
import os
import socket

app = Flask(__name__)

VERSION = "v1"
APPLICATION_NAME = "employee-api"


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


@app.route("/")
def get_employees():
    try:
        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM employees")

        records = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "application": APPLICATION_NAME,
            "version": VERSION,
            "pod": socket.gethostname(),
            "records": records
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    }), 200


@app.route("/version")
def version():
    return jsonify({
        "application": APPLICATION_NAME,
        "version": VERSION,
        "pod": socket.gethostname()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
