

def fum(a,b):
    """Set the response headers.
       :param resp: Response.
       :param ct: Content-type default "application/ld+json".
       :param headers: List of objects.
       :param status_code: status code default 200.
       :return: Response with headers.
    """
    return  a+b


print(fum(1,5))