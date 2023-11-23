# flask blog
a simple blog website using flask and python and sqlite3 as a database, also with authentication and authorization and some other features.
## how to run the project:
### command lines:
    python3 -m venv venv 
    . venv/bin/activate
    pip install -r requirements.txt 
    
    flask --app flaskr run --debug --port 5002
    pip install requests
    pip freeze > requirements.txt 
    deactivate
### python project
    python3 -m venv venv 
    . venv/bin/activate
    pip install -r requirements.txt 
    
    flask --app flaskr run --debug --port 5002
    pip install requests
    pip freeze > requirements.txt 
    deactivate

    ## docker commands
    docker build -t flask-blog-app .
    docker run -p 5004:5004 flask-blog-app
    docker run -it flask-blog-app bash


