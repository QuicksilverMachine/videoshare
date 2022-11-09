def test_create_video(given, client, verify):
    # action
    response = client.post("video/", json={"name": "name", "parent_id": None})

    # verification
    verify.http_response.status(response, 200)
    verify.video.saved(video_id=response.json.get("id"))


def test_move_video(given, client, verify):
    # preconditions
    video = given.video.exists()
    parent = given.folder.exists()

    # action
    response = client.patch(f"video/{video.id}", json={"parent_id": parent.id})

    # verification
    verify.http_response.status(response, 200)
    verify.video.exists(video_id=video.id, parent_id=parent.id)
