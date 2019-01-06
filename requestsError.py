import requests 
from requests import HTTPError, Timeout

def main():

    try: 
        # url = 'http://httpbin.org/status/404'
        url = 'http://httpbin.org/delay/5'
        result= requests.get(url, timeout=2)
        result.raise_for_status()
        printResults(result)

    # throw any http errors
    except HTTPError as err:
        print("Error: {}".format(err))

    # set an error for server timeouts
    except Timeout as err:
        print("Request code: {}".format(err))


def printResults(resData):
    print("Result code: {} ".format(resData.status_code))
    print("\n")

    print("Returned data: --------------")
    print(resData.text)


if __name__ == "__main__":
    main()