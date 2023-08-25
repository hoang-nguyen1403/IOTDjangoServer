# IOTDjangoServer

```bash
Verify that Python is installed on your machine by typing the following command in the shell prompt:
python

This is a server for python IOT project using Django restfull api framework.

how to run this python server
install Django
pip install Django~=4.1.0
pip install Pillow==9.2.0
pip install adafruit-io
pip install djangorestframework==3.13.1
pip install libsass django-compressor django-sass-processor

# for graph
pip install django-extensions==3.1.3
pip install django-htmx==1.6.0
pip install bokeh==2.4.2

ref - https://github.com/jrief/django-sass-processor

python manage.py makemigrations
python manage.py migrate
# start server 
python manage.py runserver
```

```python
import requests
username = ''
password = ''
base_url = 'http://127.0.0.1:8000/api/'
# retrieve all courses
r = requests.get(f'{base_url}/{}')
courses = r.json()
available_courses = ', '.join([course['title'] for course in courses])
print(f'Available courses: {available_courses}')
for course in courses:
    course_id = course['id']
    course_title = course['title']
    r = requests.post(f'{base_url}courses/{course_id}/enroll/',
    auth=(username, password))
    if r.status_code == 200:
        # successful request
        print(f'Successfully enrolled in {course_title}')
import requests

base_url = 'http://127.0.0.1:8000/api/roomcondition/'
data = {
"temperature": "30",
        "soilmoisture": "20"
}
r = requests.post(base_url, data=data, auth=("admin", "1"))

```