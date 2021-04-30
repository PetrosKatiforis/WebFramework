import json

def utf8_bytes(data):
    """
    Ensures that the response will be utf-8 bytes
    
    :param text: String or bytes or dictionary object
    :returns: A bytes object
    """

    if isinstance(data, dict):
        data = json.dumps(data)

    if isinstance(data, str):
        return data.encode("utf-8")

    return data
