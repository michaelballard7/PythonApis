import urllib.request

def main():
    """ Retrieving XML with urllib """
    # url to retrieve simple data
    url = "http://httpbin.org/xml"

    # open the url and retrieve some data 
    result = urllib.request.urlopen(url)

    # retrieve the status code for a specific request
    print("Result code: {} ".format(result.status))

    # retrieve the headers from a specific request
    print("Headers: -------------------")
    print(result.getheaders())

    # decode the returned XML and display it
    print("Returned data: -----------")
    print(result.read().decode('utf-8'))

if __name__ == "__main__":
    main()