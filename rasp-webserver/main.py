from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/status')
def service_status():
    service_names = request.args.getlist('service_name')
    statuses = {}
    for service_name in service_names:
        status_result = subprocess.run(['systemctl', 'is-active', service_name], capture_output=True, text=True)
        # Store the service status in a dictionary using the service name as the key.
        statuses[service_name] = status_result.stdout.strip()
    return statuses

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
