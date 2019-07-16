import json, time

from basket import product
from basket import promotion


class SimpleLogger:
    enabled = False
    info = 'INFO'
    error = 'ERROR'

    def log(self, message, level=info):
        """Simple logger.

        :param str message: Log message
        :param str level: Log level name
        """
        if self.enabled:
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            print('{} {}: {}'.format(now, level, message))


logger = SimpleLogger()


def load_json(json_file_path):
    """Load json data.

    :param str json_file_path: Path to json file to load.
    """
    data = None
    try:
        with open(json_file_path) as f:
            data = json.load(f)
    except EnvironmentError:
        logger.log(f'No such file or directory: {json_file_path}',
                   SimpleLogger.error)
    except json.JSONDecodeError as e:
        logger.log(f'Failed to parse data file {json_file_path}: {e}',
                   SimpleLogger.error)
    return data


def load_products(products_file_path):
    """Load product definitions.

    Load product definition data describing the products this program will
    accept including product names, units and price.

    :param str products_file_path: Path to goods file.
    :return dict: Dictionary of product.Product instances.
    """
    products = {}
    data = load_json(products_file_path)
    if data is None:
        logger.log('No stock found in product data')
    else:
        # Build products list
        for prod in data:
            try:
                p = product.Product(prod['name'], prod['price'], prod['unit'], prod['active'])
                if p.active:
                    products[p.name] = p
            except ValueError as e:
                logger.log(f'Failed to load a product with data: {prod} ({e})',
                           SimpleLogger.error)
    return products


def load_promotions(promotions_file_path):
    """Load promotions.

    Load promotions data that specifies discounts that can be applied
    to goods purchased.

    :param str promotions_file_path: Path to promotions file.
    :return list: List of promotion.Promotion instances.
    """
    promotions = []
    data = load_json(promotions_file_path)
    if data:
        for prod_promo in data:
            try:
                promotions.append(promotion.Promotion(prod_promo))
            except (ValueError, KeyError) as e:
                logger.log('Failed to load offer with data: '
                           f'{prod_promo} ({e})', SimpleLogger.error)
    return promotions
