# importing the requests library
import json
import requests


def endPoint(plate):
    # the api-endpoint
    apiEndpoint = "http://pastebin.com/api/api_post.php"

    # data to be sent to api
    body = {"LicensePlate": plate}

    # sending post request and saving response as response object
    request = requests.post(url=apiEndpoint, data=json.dumps(body))

    if request.status_code == 200:
        print("The request was a success!")
    elif request.status_code == 404:
        print("Result not found!")
    else:
        print("Other!")


endPoint("123")
# Main class which responsible for integration of whole image processing piplines
# if __name__ == "__main__":
#     endPoint("123ABC")
