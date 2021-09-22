def get_product_offer_str(product_offers, delim):
    """
    Helper function to return a string of product offer
    full descriptions concatenated with the given delimeter.
    """
    product_offer_str = ""
    for product_offer in product_offers:
        product_offer_str = (
            product_offer_str + delim + product_offer.description_full)
    product_offer_str = product_offer_str + delim
    return product_offer_str
