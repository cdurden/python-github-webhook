from github_webhook import Webhook
from flask import Flask
import subprocess
import os
PIPE = subprocess.PIPE

app = Flask(__name__)  # Standard Flask app
webhook = Webhook(app) # Defines '/postreceive' endpoint

@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Hello, World!"

@webhook.hook()        # Defines a handler for the 'push' event
def on_push(data):
    print("Got push on repository '{:s}'".format(data['repository']['name']))
    if os.path.exists(os.path.join(os.environ['WSGI_APPS_PATH'], data['repository']['name'])):
        process = subprocess.Popen(['git','pull'], cwd=os.path.join(os.environ['WSGI_APPS_PATH'], data['repository']['name']), stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
    if os.path.exists(os.path.join(os.environ['WSGI_APPS_PATH'], 'dev', data['repository']['name'])):
        process = subprocess.Popen(['git','pull'], cwd=os.path.join(os.environ['WSGI_APPS_PATH'], 'dev', data['repository']['name']), stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
#    if data['repository']['name'] in ['md','slides','tasks']:
#        print("updating teaching_assets")
#        process = subprocess.Popen(['git','submodule','foreach','git','pull','origin','master'], cwd=os.path.join(os.environ['WSGI_APPS_PATH'], 'teaching_assets'), stdout=PIPE, stderr=PIPE)
#        stdoutput, stderroutput = process.communicate()
    if data['repository']['name'] in ['algebra742']:
        process = subprocess.Popen(["sudo", "systemctl", "restart", "apache2"], stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
        process = subprocess.Popen(["sudo", "systemctl", "restart", "emperor.uwsgi"], stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
    #process = subprocess.Popen(["sudo", "pm2", "restart", "server"], stdout=PIPE, stderr=PIPE)
    #stdoutput, stderroutput = process.communicate()
    #print("Got push with: {0}".format(data))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
