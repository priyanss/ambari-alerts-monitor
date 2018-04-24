# Ambari Alerts Monitor
This is a small python-flask app to collect alerts from multiple Ambari servers and display it in one place for ease of monitoring. It queries Ambari server APIs and put all alerts together in a better way(my personal feeling).  

## Installation
This app is written on python 2.7 (Anaconda). Following modules are required -
```
flask
requests
datetime
json
```
If those are not installed alreay, you can install them using pip or conda or whatever.
Once the dependencies are resolved, simply clone the app -

```
$git clone https://github.com/priyanss/ambari-alerts-monitor.git
```

I recommend using Anaconda 2, since the app is developed and tested in Anaconda and has all the dependencies installed by default.
## Configuration
### hosts.json
This file contains the URL, username and password of all the Ambari servers you're going to collect alerts from. It's in json format and example values are populted already for your reference.
NOTE : Please give full URL, from http(s) up until the cluster name. Example : https://my_server.com:8443/api/v1/clusters/mycluster
### Configuring certificate if using https/ssl on Ambari
In order for python to securely connect to ssl enabled end points, it needs to be configured with a server certificate and key (or bundle). You can control this behaviour by modifying the parameters at **line 13** on **alert_mon.py**.

- If you're using SSL, first find where is your server/host CA certificate bundle is located. In the case of RHEL, CENTOS 7 , it's here : /etc/ssl/certs/ca-bundle.crt. This is what configured in this app as default. If you don't find it, create a server cert and key and use it here. More details can be found [here](http://docs.python-requests.org/en/master/user/advanced/). Now, point to that as shown below -
```
response = requests.get(host["href"]+'/alerts?fields=*&Alert/state.in(WARNING,CRITICAL)&Alert/maintenance_state=OFF&sortBy=Alert/state', verify="/path/to/ca-bundle.crt", auth=HTTPBasicAuth(host["username"], host["password"]))
```

- If you are connecting to non-ssl sites (http), simply remove the "verify" part to look like
```
response = requests.get(host["href"]+'/alerts?fields=*&Alert/state.in(WARNING,CRITICAL)&Alert/maintenance_state=OFF&sortBy=Alert/state', auth=HTTPBasicAuth(host["username"], host["password"]))
```
- If you want to turn off SSL completely, set "verify=False" instead of the cert part.
```
response = requests.get(host["href"]+'/alerts?fields=*&Alert/state.in(WARNING,CRITICAL)&Alert/maintenance_state=OFF&sortBy=Alert/state', verify=False, auth=HTTPBasicAuth(host["username"], host["password"]))
```
### Configure your IP
By default, the app listens on http://localhost:5000 . If you want to change the IP, go to **line 40** on **alert_mon.py**, and specify your IP like below -
```
app.run(host='1.2.3.4')
```
That's it !
## Run
You can run this in many ways.

### Easy way
After cloning the code as given in Installation step, 
```
$cd ambari-alerts-monitor
$python alert_mon.py &
```
### For production use cases
You can host it under Apache or Nginx as explained [here](http://flask.pocoo.org/docs/0.12/deploying/). You can also see a lot other options there.
