from flask import Flask
import json
from word_comparison import get_candidates


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Please check out the misspelled/ endpoint!'

@app.route('/misspelled/<word>')
def words_endpoint(word):
    candidates = get_candidates(word.lower())
    return json.dumps(candidates)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)

