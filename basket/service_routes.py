from flask import Blueprint, jsonify, request, abort

from basket import product
from basket import promotion
from basket import basket
from basket import logger, load_products, load_promotions

bp = Blueprint('app_routes', __name__, url_prefix='/basket_api')


@bp.route("/")
def index():
    return "Welcome to the shopping basket app"


@bp.route('/price', methods=['GET'])
def price():
    items = request.args.getlist('item', '')

    # Load available goods and offers
    products = load_products('products.json')
    promotions = load_promotions('promotions.json')

    # Make a basket and fill
    shopping_basket = basket.Basket(products, promotions)
    for item in items:
        if not shopping_basket.add(item):
            logger.log(f'Item \'{item}\' not in stock')

    # collect the results
    result = f'Subtotal: £{shopping_basket.subtotal/100:.2f}'
    shopping_basket.calculate_discounts()
    if shopping_basket.discounted_items:
        for item in shopping_basket.discounted_items:
            result += '/n' + item.discount_message
    else:
        result += '/n' + '(No offers available)'
    result += '/n' + f'Total: £{shopping_basket.total/100:.2f}'

    return jsonify(result)
