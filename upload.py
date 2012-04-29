import mimetypes, os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

config = {}
config['S3_API_KEY'] = 'AKIAJX3DKI72JEK4AL6Q'
config['S3_API_SECRET'] = os.environ.get('S3_API_SECRET')
print os.environ.get('S3_API_SECRET')
config['S3_BUCKET'] = 'www.redrobingardens.co.uk'

def config_value(key):
    return config[key]

ext_allowed = tuple('jpg jpeg png html js css pdf gif'.split())

def allowed(filename):
    return (extension(filename) in ext_allowed)

def extension(filename):
    return filename.rsplit('.', 1)[-1]

def store_in_s3(filename, content):
    conn = S3Connection(    config_value("S3_API_KEY"),
        config_value("S3_API_SECRET"),)
    bucket = conn.create_bucket( config_value('S3_BUCKET') )
    k = Key(bucket) # create key on this bucket
    k.key = filename
    mime = mimetypes.guess_type(filename)[0]
    k.set_metadata('Content-Type', mime)
    print filename
    k.set_contents_from_filename(content)
    k.set_acl('public-read')

def upload_file(filename, u_filename):
    #with open(filename) as f:
    store_in_s3(u_filename, filename)

if __name__ == '__main__':
    path = "./static"
    for dirpath, dirnames, filenames in os.walk(path):
        # print os.path.join(path, filenames)
        for file in filenames:
            filename = os.path.join(dirpath, file)
            u_filename = filename[len(path) + 1:].replace('\\', '/')
            if allowed(filename):
                print u_filename
                upload_file(filename, u_filename)

