from flask import Flask, request
import requests
from threading  import Thread
import os
import json
import subprocess


app = Flask(__name__)
CHECK_GPU_CMD = 'hostname; while read line ; do if [ "$line" != "| No running processes found |" ] ; then gpui=$(echo $line | cut -d " " -f 2); pid=$(echo $line | cut -d " " -f 3); pinfo=$(ps -hp $pid -o comm,pid,ruser); printf "%s - %s \n" $gpui "$pinfo"; fi done < <(nvidia-smi  | grep -A 10 "|==========================================" | grep -B 10 "+-----------------------------------" | head -n -1 | tail -n +2 | tr -s " "); echo ""'


def load_config():
    with open('config.json') as config_f:
        config = json.load(config_f)
        app.config['servers'] = config['servers']
        if 'port' in config: 
            app.config['port'] = config['port']
        else: 
            app.config['port'] = int(os.environ.get('PORT', '5000'))
        if 'slack-token' in config:
            app.config['auth'] = config['slack-token']


def check_gpu(login, host, port="22"):
    return subprocess.check_output(["ssh", "-p", port, "-l", login, host, CHECK_GPU_CMD])


@app.route('/check_all')
def slack_integration():
    token = request.args.get('token', '')
    response_to = request.args.get('response_url', None)
    if app.config['auth'] == token:
        if response_to is None:
            return check_all(), 200
        else:
            thread = Thread(target=response_slack, kwargs={'res_url': response_to})
            thread.start()
            return "checking, might take several seconds...", 200
    else:
        return "Authentication failed", 403
        


def check_all():
    msg = "```\n"
    import getpass
    cur_login = getpass.getuser()
    for server in app.config['servers']:
        login = server.get('login', cur_login)
        port = str(server.get('port', 22))
        host = server['hostname']
        msg += check_gpu(login, host, port).decode('utf-8')
    msg += '\n```'
    return msg


def response_slack(res_url):
    msg = check_all()
    payload = {'text': msg}
    headers = {'Content-Type': 'application/json'}
    requests.post(res_url, data=json.dumps(payload), headers=headers)


if __name__ == "__main__":
    load_config()
    app.run(host='0.0.0.0', port=app.config['port'])

