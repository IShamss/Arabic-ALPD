# importing the requests library
import requests
from nose.tools import assert_true


def endPoint(plate):
    # the api-endpoint
    apiEndpoint = "https://iic-delivery.mybluemix.net/image-processing/plates"
    # apiEndpoint="'http://localhost:8080'"
    # data to be sent to api
    body = {"plate": plate}

    # sending post request and saving response as response object
    request = requests.post(url=apiEndpoint, data=body)
    # assert_true(request.ok)
    if request.status_code == 200:
        return request.text
    elif request.status_code == 404:
        return "Result not found!"
    else:
        return "Other!"

# endPoint("123")
# Main class which responsible for integration of whole image processing piplines
# if __name__ == "__main__":
#     endPoint("123ABC")
