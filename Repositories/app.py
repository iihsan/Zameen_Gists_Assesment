import os
import re
import requests
from github import Github
from flask import Flask, request
from flask import render_template

app = Flask(__name__)

def get_gists(username):
    try:
        url = "https://api.github.com/users/" + username + "/gists"

        resp = requests.get(url)
        gists = resp.json()
        gists_list = []
        gists_urls = []
        counter_ = []
        count = 0

        for gist in gists:
            for file in gist["files"]:
                fname = ''; furl=''

                try:
                    fname = gist["files"][file]["filename"]
                except:
                    pass

                try:
                    furl = gist["files"][file]["raw_url"]
                except:
                    pass

                try:
                    language = gist["files"][file]["language"]
                    gists_list.append(str(fname + " (" + language + ")"))
                except:
                    gists_list.append(str(fname))

                gists_urls.append(furl)
                counter_.append(count)
                count+=1
                # print("{}:{}".format(fname, furl))  # This lists out all gists
        return gists_list, gists_urls, counter_
    except:
        return False, False, False

def get_repos(username):
    try:
        g = Github()
        user = g.get_user(username)

        repos_list = []
        for repo in user.get_repos():
            repos_list.append(str(re.findall('.*/(.*)".*', str(repo)))[2:-2])
        return repos_list
    except:
        return [], [], []


@app.route("/")
@app.route("/index")
@app.route("/index",methods=['POST'])
def index():
    return render_template('index.html')

@app.route("/repos")
@app.route("/repos",methods=['POST'])
def repos():
    errors = []
    username = request.form['username']
    if username.strip() == '':
        errors.append(str('Please Enter a Username'))
        return render_template('index.html', errors=errors)

    gists_list, gists_urls, counter_  = get_gists(username)

    if len(gists_list) ==0:
        errors.append(str('No Public Gists Exists for ' + username))
        return render_template('index.html', errors=errors)
    return render_template('Gists.html', repos_list = gists_list, gists_urls=gists_urls, counter_=counter_)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
