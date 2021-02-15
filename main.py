'''
    Name: main.py
    Writer: Hoseop Lee, Ainizer
    Rule: Flask app server
    update: 21.02.14
'''

from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask, request, jsonify, render_template
import torch
import os
from queue import Queue, Empty
from threading import Thread
import time

app = Flask(__name__)

print("model loading...")

print(os.system("ls"))

# Model & Tokenizer loading
story_tokenizer = AutoTokenizer.from_pretrained('./GPT2-large_SuperheroesStory')
story_model = AutoModelForCausalLM.from_pretrained('./GPT2-large_SuperheroesStory')

power_tokenizer = AutoTokenizer.from_pretrained('./GPT2-large_SuperheroesPower')
power_model = AutoModelForCausalLM.from_pretrained('./GPT2-large_SuperheroesPower')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
story_model.to(device)
power_model.to(device)

requests_queue = Queue()    # request queue.
BATCH_SIZE = 1              # max request size.
CHECK_INTERVAL = 0.1

print("complete model loading")


##
# Request handler.
# GPU app can process only one request in one time.
def handle_requests_by_batch():
    while True:
        request_batch = []

        while not (len(request_batch) >= BATCH_SIZE):
            try:
                request_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue

            for requests in request_batch:
                try:
                    types = requests["input"].pop(0)

                    if types == 'story':
                        requests["output"] = mk_superhero_story(requests['input'][0], requests['input'][1])
                    elif types == 'power':
                        requests["output"] = mk_superhero_power(requests['input'][0], requests['input'][1])

                except Exception as e:
                    requests["output"] = e


handler = Thread(target=handle_requests_by_batch).start()


##
# GPT-2 generator.
# Make superhero story.
def mk_superhero_story(name, length):
    try:
        text = name + " is"
        story_ids = story_tokenizer.encode(text, return_tensors='pt')

        # input_ids also need to apply gpu device!
        story_ids = story_ids.to(device)

        min_length = len(story_ids.tolist()[0])
        length += min_length

        length = length if length > 50 else 50

        # story model generating
        story_outputs = story_model.generate(story_ids, pad_token_id=50256,
                                             do_sample=True,
                                             max_length=length,
                                             min_length=min_length,
                                             top_k=40,
                                             num_return_sequences=1)

        result = dict()

        for idx, sample_output in enumerate(story_outputs):
            result[0] = story_tokenizer.decode(sample_output.tolist(), skip_special_tokens=True)

        return result

    except Exception as e:
        print('Error occur in script generating!', e)
        return jsonify({'error': e}), 500


##
# GPT-2 generator.
# Make superhero power.
def mk_superhero_power(name, length):
    try:
        text = name + " is"
        power_ids = power_tokenizer.encode(text, return_tensors='pt')

        # input_ids also need to apply gpu device!
        power_ids = power_ids.to(device)

        min_length = len(power_ids.tolist()[0])
        length += min_length

        length = length if length > 50 else 50

        # power model generating
        power_outputs = power_model.generate(power_ids, pad_token_id=50256,
                                             do_sample=True,
                                             max_length=length,
                                             min_length=min_length,
                                             top_k=40,
                                             num_return_sequences=1)

        result = dict()

        for idx, sample_output in enumerate(power_outputs):
            result[0] = power_tokenizer.decode(sample_output.tolist(), skip_special_tokens=True)

        return result

    except Exception as e:
        print('Error occur in script generating!', e)
        return jsonify({'error': e}), 500


##
# Get post request page.
@app.route('/superhero/<types>', methods=['POST'])
def generate(types):
    args = []

    if types == 'story':
        args.append('story')
    elif types == 'power':
        args.append('power')
    else:
        return jsonify({'Error': 'Unknown type'}), 404

    # GPU app can process only one request in one time.
    if requests_queue.qsize() > BATCH_SIZE:
        return jsonify({'Error': 'Too Many Requests'}), 429

    try:

        name = request.form['name']
        length = int(request.form['length'])

        args.append(name)
        args.append(length)

    except Exception as e:
        return jsonify({'message': 'Invalid request'}), 500

    # input a request on queue
    req = {'input': args}
    requests_queue.put(req)

    # wait
    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    return jsonify(req['output'])


##
# Queue deadlock error debug page.
@app.route('/queue_clear')
def queue_clear():
    while not requests_queue.empty():
        requests_queue.get()

    return "Clear", 200


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
    from waitress import serve
    serve(app, port=80, host='0.0.0.0')
