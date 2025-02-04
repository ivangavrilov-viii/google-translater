## ***Instructions for launching and developing a word translation service with Google Translator***

## [[GOOGLE_TRANSLATER]]
 

## Created by [Ivan Gavrilov](https://github.com/ivangavrilov-viii)
---
### Clone service repository from GitHub
```bash
git@github.com:ivangavrilov-viii/google-translater.git
```
---
### Create a virtual environment for the service
```bash
cd google-translater
python -m venv venv
```
---
### Activate a virtual environment
```bash
source venv/bin/activate
```
---
### Install all packages & libraries from `requirements.txt`
```bash
pip install -r requirements.txt
```
---
### Add service in `crontab`
```bash
crontab -e
```

```bash
--- Press "I" to change  
--- Write string  
--- press "Esc"  
--- Press ":"  
--- Write "wq" for save changes or "q!" For exit without saving  
```

```bash
0 2 * * * /home/user/google-translater/venv/bin/python3.11 /home/user/google-translater/main.py  
```
---
