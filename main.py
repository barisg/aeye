from flask import Flask, jsonify, request, render_template
from hashlib import sha1
import time, os, json, base64, hmac, urllib
from process_image import recognize_image


# Initialization
app = Flask(__name__)
# app.config["SECRET_KEY"] = '\t\xfc\xb6\xfe-\xd5\x05\xc5\x1c\x8a6\x0bT\xd7\xb1\xea\xcdFb+C\xaf\x8b\xba'


# ----- Controllers -----

# API call

@app.route('/api/<image_url>', methods=['GET'])
def api_response(image_url):
    image_url = urllib.unquote_plus(image_url)
    return jsonify(response=recognize_image(image_url))


@app.route('/api/', methods=['GET'])
def api_response_param():
    all_args = request.args.lists()

    return api_response(str(all_args[0][0]))

    
@app.route('/hello')
def hello():
    return 'Hello World!'
    

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')
    
        
@app.route('/sign_s3/')
def sign_s3():
    print 'in sign s3'
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET')

    object_name = urllib.quote_plus(request.args.get('file_name'))
    print object_name
    mime_type = request.args.get('file_type')

    expires = int(time.time()+60*60*24)
    amz_headers = "x-amz-acl:public-read"

    string_to_sign = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY.encode(), string_to_sign.encode('utf8'), sha1).digest())
    signature = urllib.quote_plus(signature.strip())

    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
    
    print url
    
    content = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
        'url': url,
    })
    
    print content
    
    return content


@app.route("/submit_form/", methods=["POST"])
def submit_form():
    print 'in submit form'
    image_url = request.form["image_url"]
    return jsonify(response=recognize_image(image_url))
    

if __name__ == '__main__':
    app.run(debug=True)

