import urllib.request
import urllib.parse
from http import HTTPStatus 

def main():

    # url  = "http://httpbin.org/get"

    # define parameters to send to my get
    args = {
        "name": "Michael Ballard",
        "is_author" : True
    }

    # # data needs to be url-encoded before passing as arguements
    data = urllib.parse.urlencode(args)

    # # issue the request the data params as part of the url
    # result = urllib.request.urlopen(url + "?" + data)

    # issue the request with a data parameter to use POST
    url = "http://httpbin.org/post"

    # to send a post request I must encode the data into bytes
    data = data.encode()
    result = urllib.request.urlopen(url, data= data)

    # print results

    print("Result code: {}".format(result.status))
    print("Returned data: ---------------")
    if (result.getcode() == HTTPStatus.OK):
        print(result.read().decode("utf-8"))


main()



