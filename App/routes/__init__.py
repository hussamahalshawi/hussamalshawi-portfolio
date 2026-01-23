from flask import Blueprint

portfolio = Blueprint('portfolio', __name__)

@portfolio.route('/')
def index():
    return {"Hussam": "Alshawi"}