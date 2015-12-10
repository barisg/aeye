from flask import Flask, jsonify, request, render_template
import time, os, json, urllib
from process_image import recognize_image
import boto3

# Initialization
app = Flask(__name__)


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
    
# Web interface

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')



@app.route("/submit_form/", methods=["POST"])
def submit_form():
    image_url = request.form["image_url"]
    return jsonify(response=recognize_image(image_url))
    
        
# Amazon upload
@ap.route('/s3test/')
    s3 = boto3.resource('s3')
    buckets = []
    for bucket in s3.buckets.all():
        buckets.append(bucket.name)
    return str(buckets)
        
@app.route('/sign_s3/')
def sign_s3():
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET_NAME')

    object_name = urllib.quote_plus(request.args.get('file_name'))
    mime_type = request.args.get('file_type')

    expires = int(time.time()+60*60*24)
    amz_headers = "x-amz-acl:public-read"

    string_to_sign = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)
    
    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY.encode(), string_to_sign.encode('utf8'), sha1).digest())
    signature = urllib.quote_plus(signature.strip())

    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
        
    content = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
        'url': url,
    })
        
    return content



    

if __name__ == '__main__':
    app.run(debug=True)

