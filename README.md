#flask blog

python project

    python3 -m venv venv 
    . venv/bin/activate
    pip install -r requirements.txt 
    
    flask --app flaskr run --debug --port 5002
    pip install requests
    pip freeze > requirements.txt 
    deactivate

    ## docker commands
    docker build -t my-flask-app .
    docker run -d -p 8080:5000 my-flask-app



