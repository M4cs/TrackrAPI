# Trackr Cydia Repository API

# Endpoints:

`/packages` - Package Serving Endpoint

`/packages/count` - Package Count Endpoint

# What is Trackr?

Trackr is a simple, lightweight download count and CDN service for DigitalOcean and AWS Buckets. You don't need DigitalOcean or AWS but it is optimized to work with them.

The Trackr API consists of 2 simple endpoints. One for serving files and tracking the times served (`/packages`) and one for grabbing the count of packages (`/packages/count`). The API is setup to run with Gunicorn and Nginx but you can configure it to suit your needs. I run it on my DigitalOcean box with Supervisor and Gunicorn. Follow [this medium post](https://medium.com/ymedialabs-innovation/deploy-flask-app-with-nginx-using-gunicorn-and-supervisor-d7a93aa07c18) for an easy guide on getting a flask app running with those two tools.

# Requirements

- A Virtual Private Server or Dedicated Server on Linux (Ubuntu 16.04 is generally easiest to get setup)
- Nginx (You can use Apache but I don't offer support for it)
- Flask
- Python 3.5.2+
- Optional: DigitalOcean Spaces or Amazon S3 Bucket and/or CDN Service

# Using

**For DigitalOcean or AWS S3 Buckets**

To get setup with Trackr and  you will need to edit the `config.json` file in the `app/` folder. There you will put your Access Key and Secret Key. You can also make them environment variables and replace the `aws_access_key` and `aws_secret_key` parameters in the Session call inside `app/resources.py`. **You will also need to configure `app/resources.py` inside the Session call with your CDN endpoints. Example below.**

**For The Rest and DigitalOcean or AWS S3 Bucket Hosts**

First, clone the repository to your server in your user's home folder (I don't reccommend using root). If you are not using a CDN or Bucket to host files comment out the block in `app/resources.py` that says **`NON CDN USERS COMMENT OUT`**. Also comment out the return statement at the bottom and uncomment/replace the link with your repository. **READ THE `app/resources.py` COMMENTS IN ORDER TO UNDERSTAND HOW THE REDIRECTS WORK**

Follow [this link](https://medium.com/ymedialabs-innovation/deploy-flask-app-with-nginx-using-gunicorn-and-supervisor-d7a93aa07c18) once you have all the files setup on your server to get it running as a service on your box.

# How The Packages Redirect Works

I'm sure for some people who are new to python or programming in general they don't understand how the redirects work to get the packages file setup to serve files.

### For CDNs:

How To Set Parameters Correctly:

```
client = session.client('s3', # Digital Ocean and AWS use this
                        region_name='', # Ex.: 'sfo2'
                        endpoint_url='', # Ex.: 'https://sfo2.digitaloceanspaces.com/'
                        aws_access_key_id=aws_access, # Enter in app/config.json
                        aws_secret_access_key=aws_secret) # Enter in app/config.json
res = client.list_objects(Bucket='', Prefix='') # Bucket = Space or Bucket your files are on. Prefix = subfolder(s) in bucket that files are contained in.
```

### For Non-CDNs:

How To Set Redirects and Your Repo Up:

If your repo is setup like this:
```
/repo
/repo/index.html
/repo/Packages.bz2
/repo/Release
/repo/CydiaIcon.png
/repo/debs/
     /debs/com.example.tweak.deb
     /debs/com.example2.tweak.deb
```

Then your redirect should be:

```
return redirect('https://repo.example.com/repo/debs/' + data['packages'], 302)
```

Your Filename Value for the entry for `com.example.tweak.deb` in `Packages` would be:
```
Filename: https://api.example.com/packages?package=com.example.tweak.deb
```