# pylint: disable=unused-variable,expression-not-assigned

from expecter import expect


def describe_stream():

    def it_exists(client):
        response = client.get("/stream")

        expect(response.status_code) == 200
        expect(response.mimetype) == 'text/html'
