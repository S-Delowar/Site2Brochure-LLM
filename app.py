import logging
from flask import Flask, render_template, request, Response, send_file, stream_with_context
from brochure.brochure_generator import generate_brochure_streaming
from utils.markdown_to_html import markdown_to_html

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/stream", methods=["POST"])
def stream():
    company_name = request.form["company_name"]
    website_url = request.form["website_url"]

    def generate():
        for mark_text in generate_brochure_streaming(company_name, website_url):
            html_content = markdown_to_html(mark_text)
            logging.info(html_content)
            yield f"<div class='mb-3'>{html_content}</div>\n"

    return Response(generate(), content_type='text/html')




if __name__ == "__main__":
    app.run(port=5000, debug=True)