import faker
import pytest

from videoshare.models import NodeType

fake = faker.Faker()


def test_get_folder(given, client, verify):
    # preconditions
    folder = given.folder.exists()

    # action
    response = client.get(f"folder/{folder.id}")

    # verification
    verify.http_response.status(response, 200)
    verify.folder.exists(folder_id=folder.id, parent_id=folder.parent_id)


def test_get_folder_nonexistent(given, client, verify):
    # preconditions
    folder_id = fake.uuid4()

    # action
    response = client.get(f"folder/{folder_id}")

    # verification
    verify.http_response.status(response, 404)


def test_create_folder(client, verify):
    # action
    response = client.post("folder/", json={"name": "name", "parent_id": None})

    # verification
    verify.http_response.status(response, 200)
    verify.folder.saved(folder_id=response.json.get("id"))


@pytest.mark.parametrize(
    "name, parent_id, code",
    [
        # Nonexistent folder
        (None, fake.uuid4(), 400),
        # Invalid folder name
        ("invalid/name", fake.uuid4(), 400),
        # Name already exists
        ("existing_name", fake.uuid4(), 400),
        # Parent does not exist
        ("valid_name", fake.uuid4(), 400),
        # Parent is not a folder
        ("valid_name", "ce037119-f987-4cfd-b68f-ab15f29d4b88", 400),
    ],
)
def test_create_folder_errors(given, client, verify, name, parent_id, code):
    # preconditions
    given.folder.exists(name="existing_name")
    given.video.exists(id_="ce037119-f987-4cfd-b68f-ab15f29d4b88", name="valid-name")

    # action
    response = client.post("folder/", json={"name": name, "parent_id": parent_id})

    # verification
    verify.http_response.status(response, code)


def test_move_folder(given, client, verify):
    # preconditions
    folder = given.folder.exists()
    parent = given.folder.exists()

    # action
    response = client.patch(f"folder/{folder.id}", json={"parent_id": parent.id})

    # verification
    verify.http_response.status(response, 200)
    verify.folder.exists(folder_id=folder.id, parent_id=parent.id)


@pytest.mark.parametrize(
    "node_type",
    [
        # Video exists with same name
        NodeType.VIDEO,
        # Folder exists with same name
        NodeType.FOLDER,
    ],
)
def test_move_folder_existing_name(given, client, verify, node_type):
    # preconditions
    name = fake.name()
    folder = given.folder.exists(name=name, parent_id=None)
    new_parent = given.folder.exists()
    given.node.exists(name=name, type_=node_type, parent_id=new_parent.id)

    # action
    response = client.patch(f"folder/{folder.id}", json={"parent_id": new_parent.id})

    # verification
    verify.http_response.status(response, 400)


@pytest.mark.parametrize(
    "folder_id, name, parent_id, code",
    [
        # Folder does not exist
        (None, "valid_name", fake.uuid4(), 404),
        # Parent does not exist
        (fake.uuid4(), "valid_name", fake.uuid4(), 400),
        # Parent is not a folder
        (fake.uuid4(), "valid_name", "ce037119-f987-4cfd-b68f-ab15f29d4b88", 400),
    ],
)
def test_move_folder_various_errors(
    given, client, verify, folder_id, name, parent_id, code
):
    # preconditions
    given.video.exists(
        id_="ce037119-f987-4cfd-b68f-ab15f29d4b88",
        name="valid_video_name",
    )
    if folder_id:
        given.folder.exists(id_=folder_id, name=name)

    # action
    response = client.patch(f"folder/{folder_id}", json={"parent_id": parent_id})

    # verification
    verify.http_response.status(response, code)
