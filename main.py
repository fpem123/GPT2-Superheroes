'''
    Name: main.py
    Writer: Hoseop Lee, Ainizer
    Rule: Flask app server
    update: 21.02.14
'''

from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)


##
# Get post request page.
@app.route('/superhero/<types>', methods=['POST'])
def generate(types):
    try:
        infer_path = None
        if types == 'story':
            infer_path = 'Story'
        elif types == 'power':
            infer_path = 'Power'
        text = request.form['text']
        length = int(request.form['length'])
        
        URL = f'https://feature-add-torch-serve-gpt-2-server-gkswjdzz.endpoint.ainize.ai/infer/GPT2-large_Superheroes{infer_path}'
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.post(URL, headers=headers, data=json.dumps({
            'text': text,
            'num_samples': 1,
            'length': length
        }))

        result = res.json()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': e}), 500


##
# Sever health checking page.
@app.route('/healthz', methods=["GET"])
def health_check():
    return "Health", 200


##
# Main page.
@app.route('/')
def main():
    return render_template('main.html'), 200


if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0')
