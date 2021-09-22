# Function to convert a key value to a delimeted strin, given object collection, key and delimeter

def keyvalue_to_delimited_string(objcoll, key, delim):
    strvalue = ""
    for obj in objcoll:
        strvalue = strvalue + "delim" + obj.key
    strvalue = strvalue[(len(delim)):]
    return strvalue