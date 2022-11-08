def test_status(client, verify):
    response = client.get(path="status/")
    verify.http_response.status(response=response, status_code=200)
    verify.http_response.data(response=response, expected={"status": "OK"})
