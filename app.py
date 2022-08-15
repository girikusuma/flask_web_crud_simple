from flask import Flask

app = Flask(__name__)
app.secret_key = "shayudgwrHSiug&^rdq&HDOIAHa8X7SWG8F"

from routes import *

if __name__ == "__main__":
    app.run(debug=True, port=8000)
