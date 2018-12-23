import requests


def main():

    # Use requests to issue a standard HTTP GET request
    url = "http://httpbin.org/xml"
    result = requests.get(url)
    # printResults(result)

    # Send some parameters to the URL via a gET request
    url =  "http://httpbin.org/get"
    dataValues = {
        "key1": "value1",
        "key2": "value2"
    }
    result = requests.get(url, params=dataValues)

    # the darams arg allows me to send data with a post request
    url =  "http://httpbin.org/post"
    result = requests.post(url, data=dataValues)
    printResults(result)

    # pass a custom header to the server
    url = "http://httpbin.org/get"
    headerValues = {
        "User-Agent" : "Michael Ballard App / 1.0.0"
    }
    result = requests.get(url, headers=headerValues)
    printResults(result)


def printResults(resData):
    print("Result code: {}".format(resData.status_code))
    print("\n")

    print("Headers: -----------")
    print(resData.headers)
    print("\n")


    print("Returned data: ------------")
    # I can look at encoding properties to see response types
    print(resData.text)


if __name__ == "__main__":
    main()