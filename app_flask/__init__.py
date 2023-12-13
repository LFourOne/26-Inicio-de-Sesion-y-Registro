from flask import Flask
import re

app = Flask(__name__)
app.secret_key = "Shhhh, stay quiet!"

DATA_BASE = "db_magamagazines"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')