from flask import redirect, render_template
from flask_restful import Resource, reqparse
import boto3, os, json

parser = reqparse.RequestParser()
parser.add_argument('package', help='Package Id', required=True)

class DownloadPackage(Resource):
    def get(self):
        data = parser.parse_args()
# NON CDN USERS COMMENT OUT FROM HERE TO LINE 32 #
        with open('config.json', 'r+') as f:
            objd = json.load(f)
            aws_access = objd['AWS_ACCESS_KEY']
            aws_secret = objd['AWS_SECRET_KEY']
            f.close()
        session = boto3.session.Session()
        client = session.client('s3', # Used by DigiOcean and AWS
                                region_name='sfo2', # Region Your Bucket Is Hosted In
                                endpoint_url='https://sfo2.digitaloceanspaces.com', # Endpoint URL (Don't include bucket subdomain)
                                aws_access_key_id=aws_access, # From config.json
                                aws_secret_access_key=aws_secret) # From config.json
        res = client.list_objects(Bucket='<YOURBUCKET>', Prefix='<SUBFOLDER>')
        try:
            for obj in res['Contents']:
                if str(data['package']) in str(obj['Key']):
                    suffix = obj['Key']
        except:
            return { 'err': 'Package Not Found' }, 404
# STOP COMMENTING OUT HERE #
        with open('count.json', 'r+') as json_file:
            dobj = json.load(json_file)
            if data['package'] not in dobj:
                dobj[data['package']] = 0
            count = dobj[data['package']]
            count += 1
            dobj[data['package']] = count
            json_file.seek(0)
            json.dump(dobj, json_file, indent=4)
            json_file.truncate()
            json_file.close()
# NON CDN USERS COMMENT OUT THIS RETURN STATEMENT #
        return redirect('https://<YOUR BUCKET>.sfo2.digitaloceanspaces.com/' + suffix, 302)

# UNCOMMENT LINE BELOW AND ENTER YOUR PACKAGES LINK ON YOUR REPOSITORY #
#        return redirect('https://repo.example.com/debs/' + data['package'], 302)

# For the above return, you should have your repo domain, the subfolder where your debs are #
# and then when you link it in your packages file, add the package= parameter as the file name. #
   

class GetPackageCount(Resource):
    def get(self):
        data = parser.parse_args()
        with open('count.json', 'r+') as f:
            dobj = json.load(f)
            f.close()
            if data['package'] not in dobj:
                return { 'Error': 'This File Has Either Not Been Downloaded Or Does Not Exist' }, 404
            return { 'package' : data['package'],
                    'count' : dobj[data['package']] }
        
