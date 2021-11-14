def keyvalue_to_delimited_string(objcoll, key, delim):
    """
    Function to convert a key value to a delimeted string,
    given object collection, key and delimiter
    """
    strvalue = ""
    # Loop through object collection
    for obj in objcoll:
        # Construct string value
        strvalue = strvalue + "delim" + obj.key
    strvalue = strvalue[(len(delim)):]
    # Return string value
    return strvalue
