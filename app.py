import binwalk
from flask import Flask, request, redirect
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import HTTPException
import os
import redis
import base64

app = Flask(__name__)

r = redis.Redis.from_url('redis://localhost:6667', db=3, decode_responses=True)

def save_to_db(h, blob):
    r.hset(h, 'blob', base64.b64encode(blob))
    return True

def load_from_db(h):
    return base64.b64decode(r.hget(h, 'blob'))


def analyze(data, sha256=''):
	ret = ''
	with open(sha256, 'wb') as f:
		f.write(data)
	for module in binwalk.scan(id, signature=True):
	    ret += "%s Results for %s:\n" % (module.name, id)
	    for result in module.results:
	        ret += "\t0x%.8X    %s\n" % (result.offset, result.description)
	os.remove(sha256)
	return ret

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return BadRequest('No file part')
        file = request.files['file']
        if file:
            save_to_db(request.args.get('id'), file.read())
            return ('File saved', 200)
    return BadRequest('Error') 

@app.route('/analyze')
def analyze_route():
	sha256 = request.args.get('id')
	try:
		return (r.hget(sha256, 'results'), 200)
	except:
		try:
			results = analyze_data(load_from_db(sha256), sha256)
			r.hset(sha256, 'results', results)
			return (results, 200)
		except Exception as e:
			print(f'{sha256} blob not found or {e}')
			return (f'{sha256} blob not found or {e}', 404)			

if __name__ == '__main__':
    
    app.run(debug=True)
