def test_get_folder(given, client, verify):
    # precondition
    folder = given.folder.exists()

    # action
    response = client.get(f"folder/{folder.id}")

    # verification
    verify.http_response.status(response, 200)
    verify.folder.exists(folder_id=folder.id, parent_id=folder.parent_id)


def test_create_folder(client, verify):
    # action
    response = client.post("folder/", json={"name": "name", "parent_id": None})

    # verification
    verify.http_response.status(response, 200)
    verify.folder.saved(folder_id=response.json.get("id"))


# @pytest.mark.parametrize([])
def test_move_folder(given, client, verify):
    # precondition
    folder = given.folder.exists()
    parent = given.folder.exists()

    # action
    response = client.patch(f"folder/{folder.id}", json={"parent_id": parent.id})

    # verification
    verify.http_response.status(response, 200)
    verify.folder.exists(folder_id=folder.id, parent_id=parent.id)
