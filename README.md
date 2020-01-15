# backend of xyt
## How to initial
```
pip3 install -r requirements.txt
cp .env.example .env
flask db init
flask db upgrade
flask db migrate
```
## How to run
```
(dev)
python3 xyt.py
(prod)
use gunicorn
```