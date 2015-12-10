from hashlib import sha1
import time, os, json, base64, hmac, urllib
import urllib2
import boto3

AWS_ACCESS_KEY = 'AKIAI4KLQAMVFP6IVRYQ'
AWS_SECRET_KEY = '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'
S3_BUCKET = 'eye-images'

def s3_auth():

    object_name = urllib.quote_plus('shutter.png')
    mime_type = 'image/png'

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
    
signed_content = json.loads(s3_auth())
signed_request = signed_content['signed_request']

print signed_request

try:
    response = urllib2.urlopen(signed_request)
    html = response.read()
    print html
except urllib2.HTTPError as e:
    print e


# ----------------------


def s3boto():
    from boto3.session import Session
    
    session = Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name='us-west-2')
    s3 = session.resource('s3')
    client = session.client('s3')
    
    expires = int(time.time()+60*60*24)    
    object_name = urllib.quote_plus('shutter.png')
    
    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
    
    fields = client.generate_presigned_post(S3_BUCKET, object_name)['fields']
    content = json.dumps({
        'signed_request' : '%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s' % (url, fields['AWSAccessKeyId'], expires, fields['signature']),
        'url': url,
    })

    return content
    
signed_content = json.loads(s3boto())
signed_request = signed_content['signed_request']

print signed_request

try:
    response = urllib2.urlopen(signed_request)
    html = response.read()
    print html
except urllib2.HTTPError as e:
    print e

