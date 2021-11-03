def keyvalue_to_delimited_string(objcoll, key, delim):
    """
    Function to convert a key value to a delimeted string,
    given object collection, key and delimeter
    """
    strvalue = ""
    for obj in objcoll:
        strvalue = strvalue + "delim" + obj.key
    strvalue = strvalue[(len(delim)):]
    return strvalue
