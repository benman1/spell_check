# Spell-correction Web Service

This service provides a list of likely matches for a word, ordered by their probability. 


## Running

First, start the service. This is done by changing into the project directory and typing the following: 

```
virtualenv venv
pip install -r requirements.txt
python api.py
```

## Endpoints

You can access the endpoint via curl (or your web browser) at: 

curl localhost://misspelled/$word


