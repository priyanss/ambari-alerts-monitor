import requests
import datetime
import json as JSON
from requests.auth import HTTPBasicAuth
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    results = []
    host_details = JSON.load(open('hosts.json'))
    for host in host_details["hosts"]:
        response = requests.get(host["href"]+'/alerts?fields=*&Alert/state.in(WARNING,CRITICAL)&Alert/maintenance_state=OFF&sortBy=Alert/state', verify="/etc/ssl/certs/ca-bundle.crt", auth=HTTPBasicAuth(host["username"], host["password"]))
	if response.status_code != 200:
		return render_template('error.html', host=host["href"])
        alert = JSON.loads(response.content)
	results.append(alert)
    temp = JSON.dumps(results)
    result = JSON.loads(temp)
    return render_template('index.html', result=result)

def urlsplit (href):
    split_url = href.split("/api/")[-2:]
    return split_url[0]

def todatetime (epoch):
    return datetime.datetime.fromtimestamp(epoch/1000).strftime('%d-%m-%Y %H:%M:%S')

def duration (original,latest):
    orig=datetime.datetime.strptime(datetime.datetime.fromtimestamp(original/1000).strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
    late=datetime.datetime.strptime(datetime.datetime.fromtimestamp(latest/1000).strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
    duration=late-orig
    return duration

app.jinja_env.globals.update(urlsplit=urlsplit)    
app.jinja_env.globals.update(todatetime=todatetime)
app.jinja_env.globals.update(duration=duration)

if __name__ == "__main__":
    app.run()
