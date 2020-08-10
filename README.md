# setup
## 0. install xvfb for excute virtual frameebuffer: a virtual windows like chrome windows
sudo apt install xvfb
## 1. install pipenv
pip3 install pipenv

## 2. if has error "keyring.itul.escape"
pip3 install --upgrade keyring.alt

## 3. clone this repo, change dir to dowloaded folder

## 4. install dependencies of project
pipenv install

## 5.initialize pipenv /activate venv
pipenv shell

## 6. addtional for vscode:
add setting for visual code

add .vscode/setting.json:

{

    "python.pythonPath": "<Path to venv>",
    "files.exclude": {
        "**/.git": true,
        "**/.svn": true,
        "**/.hg": true,
        "**/CVS": true,
        "**/.DS_Store": true,
        "**/.pyc": true,
        "**/__pycache": true
    }
    
}

## 7. run crawler
python crawler.py

