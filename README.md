# Web Scraping with Django


### Virtual Environment installation and activate:

```bash
python -m venv env
source env/bin/activate

```


### Installation of requirements:

```bash
pip install -r requirements.txt
```

### Makemigrations and migrate processes of Django project:

```bash
python manage.py makemigrations
python manage.py migrate
```

[Download](http://redis.io/download) Redis:

Open Redis:

```bash
redis-server
```

Open a terminal window, with in your `project root` where `manage.py` lives:
        
```bash
celery -A scraping worker -l info --pool=solo

celery -A scraping beat -l info
```

