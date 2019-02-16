## django-ss-autorebuild
Simple Shadowsocks Web Manager

version: 0.1.0

require: python3.6+

## Usage
```bash
pip install -r requirements.txt
pip install -U git+https://github.com/shadowsocks/shadowsocks.git@master
cd ssadmin && python manage.py migrate 
python manage.py setup
python manage.py runserver 0:8000
```
