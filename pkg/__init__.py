from flask import Flask

app = Flask(__name__, instance_relative_config=True, static_folder='static', template_folder='templates')
from pkg import myroutes 