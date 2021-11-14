def get_product_offer_str(product_offers, delim):
    """
    Helper function to return a string of product offer
    full descriptions concatenated with the given delimiter.
    """
    product_offer_str = ""
    # Loop through product offers
    for product_offer in product_offers:
        # Set product offer string
        product_offer_str = (
            product_offer_str + delim + product_offer.description_full)
    product_offer_str = product_offer_str + delim
    # return product offer string
    return product_offer_str
