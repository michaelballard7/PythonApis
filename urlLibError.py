import urllib.request
from http import HTTPStatus
from urllib.error import HTTPError, URLError


def main():
    
    # define url's
    url = "http://no-such-server.org"
    url2 = "http://httpbin.org/status/404"
    url3 =  "http://httpbin/org/html"

    # Define try and exception handling to contain errors
    try: 
        result = urllib.request.urlopen(url)
        print("Result code: {}".format(result.status))
        if (result.getcode() == HTTPStatus.OK):
            print(result.read().decode('utf-8'))
    except HTTPError as err:
        print("Error: {}".format(err.code))

    except URLError as err:
        print("This servers is a dud {}".format(err.reason))

main()



