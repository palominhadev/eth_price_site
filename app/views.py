from flask import Blueprint, render_template, jsonify
from .utils import get_ethereum_price

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('index.html', defi_pool_name='Sushi')


@views.route('/api/price')
def api_price():
    price_data = get_ethereum_price(min_price=3850, max_price=4450)
    return jsonify(price_data)
