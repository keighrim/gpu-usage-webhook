# Who's using GPU now? 

This is a simple webapp designed for Slack integration (as a slash command) to check Nvidia GPU usage of multiple servers. 

## Installation 
### Requirement 
* The server that runs this app MUST have password-less ssh access to GPU servers. 
* GPU servers MUST have Nvidia GPU(s) and have reasonably recent Nvidia driver and CUDA installed (tested on cuda 10.0)

### Configuration 
* Open `config.json` file 
1. Add server objects to check. 
(example)
```json
"servers": [
{ "hostname": "some.hostname.url", "port": 22, "login": "some_login"  }
]
```
  * `port` is ssh port (not the port this webapp is listening) (if not given, defaults to 22)
  * `login` is unix username on the GPU server (if not give, the username used for running this webapp will be used)
    * this login MUST have access to `nvidia-smi` command 
2. Set port number this app to listen 
(example)
```json
"port": 8880
```
  * If not given, system envvar `$PORT` will be used. If `$PORT` is not set, `5000` will be used. 

### Slack integration 

Add Slack app called `slash commands` (developed by slack team), and set command, icon, name as you want. For URL, use the url where this webapp will be listening (including port). For HTTP method, pick `GET`. And finally, copy the slack token string and pasted it in the `config.json` file. 
(example)
```json 
"slack-token": "SLACKTOKENHASHSTRING"
```

### Start-up
Install dependencies. 
```bash 
pip install -r requirments.txt
```
And start the server. 
```bash 
python app.py
```


