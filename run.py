import datetime
import socket
import ssl
from urlparse import urlparse
import urllib2, json



#This was modified from https://serverlesscode.com/post/ssl-expiration-alerts-with-lambda/
def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)

url = "amusementlogic.com"


now = datetime.datetime.now()
expirationDate = ssl_expiry_datetime(url)
delta = expirationDate - now
print delta.days
