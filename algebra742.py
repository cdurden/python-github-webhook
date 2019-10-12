from github_webhook import Webhook
from flask import Flask
import subprocess

app = Flask(__name__)  # Standard Flask app
webhook = Webhook(app) # Defines '/postreceive' endpoint

@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Hello, World!"

@webhook.hook()        # Defines a handler for the 'push' event
def on_push(data):
    process = subprocess.Popen(['git','pull'], cwd=os.path.join(os.environ['WSGI_APPS_PATH'], data['repository']['name']))
    stdoutput, stderroutput = process.communicate()
        app_path, stdout=PIPE, stderr=PIPE)
    process = subprocess.Popen(["sudo", "systemctl", "restart", "apache2"], stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()
    print("Got push with: {0}".format(data))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
