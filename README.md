# reaktor-pre-assignment-2019
Reaktor pre-assignment for junior developer positions 2019

Program that reads information about packages from /var/lib/dpkg/status -file.  
Packages and their contents are brosable via HTML interface.


Live at: https://package-app.herokuapp.com/
  

## How to run:

Create new virtualenviroment:  
``` 
pip install virtualenv
virtualenv venv
venv\Scripts\activate
```
Activate venv on linux:
```
source venv/bin/activate
```
Clone this repository:
``` 
git clone https://github.com/Jerere/reaktor-pre-assignment-2019.git
cd reaktor-pre-assignment-2019
``` 

Install flask and run server.py:
``` 
pip install flask
python server.py
``` 

App now runs on localhost:5000
