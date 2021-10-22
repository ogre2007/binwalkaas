import binwalk
from flask import Flask, request, redirect
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import HTTPException
import os

app = Flask(__name__)


def analyze_data(data, sha256):
	r = ''
	with open(sha256, 'wb') as f:
		f.write(data)
	for module in binwalk.scan(sha256, signature=True):
	    r += "%s Results:\n" % module.name
	    for result in module.results:
	        r += "\t%s    0x%.8X    %s\n" % (result.file.path, result.offset, result.description)
	#os.remove(sha256)
	return r

@app.route('/analyze', methods=['POST'])
def upload_and_analyze():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return BadRequest('No file part')
        file = request.files['file']
        if file:
            result = analyze_data(file.read(), request.args['sha256'])

            return (result, 200)

    return BadRequest('Error') 


if __name__ == '__main__':
    
    app.run(debug=True)
