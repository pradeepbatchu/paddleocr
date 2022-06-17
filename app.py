import asyncio
import os
import time
from flask import Flask, abort, request,jsonify
from flask_cors import CORS, cross_origin
import logging
from flask_cors import CORS, cross_origin
from flask import jsonify
import json
from paddleocrsvc import imagetotext
from pdftotext import extract_text_from_pdf
app = Flask(__name__)


@app.route('/api/upload', methods=['POST'])
def file_upload():
    file = imagetotext()
    return file


@app.route('/api/upload/pdf', methods=['POST'])
def pdf_upload():
    file = extract_text_from_pdf()
    return file


@app.route('/api/help', methods=['GET'])
def help():
    endpoints = [rule.rule for rule in app.url_map.iter_rules()
                 if rule.endpoint !='static']
    return jsonify(dict(api_endpoints=endpoints))


@app.route("/api/routes", methods=["GET"])
def getRoutes():
    routes = {}
    for r in app.url_map._rules:
        routes[r.rule] = {}
        routes[r.rule]["functionName"] = r.endpoint
        routes[r.rule]["methods"] = list(r.methods)

    routes.pop("/static/<path:filename>")

    return jsonify(routes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)