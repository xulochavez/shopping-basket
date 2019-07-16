"""Basket.

Simple application that prices a basket of products taking into account
any special offers.  The program accepts a list of items in the basket
and outputs the subtotal, the special offer discounts and the final price.

Information about products available for purchase (product names, units and
price) are loaded (by default) from the json file `products.json`.  Special
offers are are loaded (by default) from the json file `promotions.json`.
"""


import argparse
import sys

from basket import basket
from basket import util
from basket.util import logger, load_products, load_promotions


def parse_args(argv=None):
    """Parse command line arguments.

    :param list argv: Args to parse.
    """
    parser = argparse.ArgumentParser(prog='basket')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'{parser.prog} 0.1',
    )
    parser.add_argument(
        '--products',
        help='Path of the products json file',
        default='products.json',
        dest='products',
    )
    parser.add_argument(
        '--promotions',
        help='Path of the promotions json file',
        default='promotions.json',
        dest='promotions',
    )
    parser.add_argument(
        'items',
        metavar='item',
        type=str,
        nargs='+',
        help='One or more items for the basket.  Only items listed in '
             'goods.json are accepted.')
    parser.add_argument(
        '--verbose',
        help='Verbose output',
        default=False,
        action='store_true',
        dest='verbose',
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Program entry point.

    Parses any arguments, invokes `load_products` and `load_promotions` (to
    load the available goods and offers) and constructs a `basket` instance,
    giving it the available products in stock (`products`) and any prevailing
    offers (`promotions`).  For each product item specified on the command line,
    we add it to the basket. When all items have been added we query `basket`
    for a sub-total, discounts that could be applied and total price, which is
    output.

    :param list argv: Command line arguments.
    """
    # Parse arguments
    args = parse_args(argv)
    logger.enabled = args.verbose

    # Load available goods and offers
    products = load_products(args.products)
    promotions = load_promotions(args.promotions)

    # Make a basket and fill
    shopping_basket = basket.Basket(products, promotions)
    for item in args.items:
        if not shopping_basket.add(item):
            logger.log(f'Item \'{item}\' not in stock')

    # Print the results
    print(f'Subtotal: £{shopping_basket.subtotal/100:.2f}')
    shopping_basket.calculate_discounts()
    if shopping_basket.discounted_items:
        for item in shopping_basket.discounted_items:
            print(item.discount_message)
    else:
        print('(No offers available)')
    print(f'Total: £{shopping_basket.total/100:.2f}')


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
