from app import app
from flask import Flask, request, jsonify
from app.views import * 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)