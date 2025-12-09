import os
import shutil
import pytest
import subprocess
import time
import requests
from pytest import fixture


def describe_SquirrelServer():
    @fixture(scope="function")
    def server():
        shutil.copy("empty_squirrel_db.db", "squirrel_db.db")

        process = subprocess.Popen(
            ["python3", "squirrel_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        max_retries = 30
        server_ready = False
        for i in range(max_retries):
            try:
                response = requests.get("http://127.0.0.1:8080/squirrels", timeout=0.5)
                server_ready = True
                break
            except (requests.exceptions.RequestException, requests.exceptions.Timeout):
                time.sleep(0.2)

        if not server_ready:
            process.terminate()
            raise RuntimeError("Server failed to start")

        yield process

        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

    @fixture
    def base_url():
        return "http://127.0.0.1:8080"

    def describe_GET_squirrels():
        def returns_200(server, base_url):
            response = requests.get(f"{base_url}/squirrels")
            assert response.status_code == 200

        def returns_json(server, base_url):
            response = requests.get(f"{base_url}/squirrels")
            assert "application/json" in response.headers.get("Content-Type", "")

        def returns_empty_list(server, base_url):
            response = requests.get(f"{base_url}/squirrels")
            assert response.json() == []

        def returns_squirrels_list(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "Fluffy", "size": "large"})
            response = requests.get(f"{base_url}/squirrels")
            assert isinstance(response.json(), list)
            assert len(response.json()) == 1

        def returns_multiple_squirrels(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "DJ", "size": "medium"})
            requests.post(f"{base_url}/squirrels", data={"name": "Jeff", "size": "large"})
            requests.post(f"{base_url}/squirrels", data={"name": "Curtis", "size": "extra large"})
            response = requests.get(f"{base_url}/squirrels")
            assert len(response.json()) == 3

        def returns_ordered_by_id(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "First", "size": "large"})
            requests.post(f"{base_url}/squirrels", data={"name": "Second", "size": "small"})
            response = requests.get(f"{base_url}/squirrels")
            squirrels = response.json()
            assert squirrels[0]["name"] == "First"
            assert squirrels[1]["name"] == "Second"
            assert squirrels[0]["id"] < squirrels[1]["id"]

    def describe_GET_squirrel():
        def returns_200(server, base_url):
            create_response = requests.post(f"{base_url}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{base_url}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{base_url}/squirrels/{squirrel_id}")
            assert response.status_code == 200

        def returns_json(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{base_url}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{base_url}/squirrels/{squirrel_id}")
            assert "application/json" in response.headers.get("Content-Type", "")

        def returns_404(server, base_url):
            response = requests.get(f"{base_url}/squirrels/9999")
            assert response.status_code == 404

    def describe_POST_squirrels():
        def returns_201(server, base_url):
            response = requests.post(f"{base_url}/squirrels", data={"name": "Fluffy", "size": "large"})
            assert response.status_code == 201

        def creates_squirrel(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{base_url}/squirrels")
            assert len(list_response.json()) == 1

        def creates_multiple_squirrels(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "First", "size": "large"})
            requests.post(f"{base_url}/squirrels", data={"name": "Second", "size": "small"})
            list_response = requests.get(f"{base_url}/squirrels")
            assert len(list_response.json()) == 2

        def assigns_unique_ids(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "First", "size": "large"})
            requests.post(f"{base_url}/squirrels", data={"name": "Second", "size": "small"})
            list_response = requests.get(f"{base_url}/squirrels")
            squirrels = list_response.json()
            assert squirrels[0]["id"] != squirrels[1]["id"]

        def returns_400_when_name_missing(server, base_url):
            response = requests.post(f"{base_url}/squirrels", data={"size": "large"})
            assert response.status_code == 400
    
        def returns_400_when_size_missing(server, base_url):
            response = requests.post(f"{base_url}/squirrels", data={"name": "Fluffy"})
            assert response.status_code == 400


    def describe_PUT_squirrel():
        def returns_204(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "Original", "size": "large"})
            list_response = requests.get(f"{base_url}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.put(f"{base_url}/squirrels/{squirrel_id}", data={"name": "Updated", "size": "small"})
            assert response.status_code == 204

        def returns_404(server, base_url):
            response = requests.put(f"{base_url}/squirrels/9999", data={"name": "Test", "size": "large"})
            assert response.status_code == 404

        def updates_name(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "Original", "size": "large"})
            list_response = requests.get(f"{base_url}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.put(f"{base_url}/squirrels/{squirrel_id}", data={"name": "Updated", "size": "large"})
            get_response = requests.get(f"{base_url}/squirrels/{squirrel_id}")
            assert get_response.json()["name"] == "Updated"

        def updates_size(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{base_url}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.put(f"{base_url}/squirrels/{squirrel_id}", data={"name": "Fluffy", "size": "tiny"})
            get_response = requests.get(f"{base_url}/squirrels/{squirrel_id}")
            assert get_response.json()["size"] == "tiny"

        def preserves_id(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "Original", "size": "large"})
            list_response = requests.get(f"{base_url}/squirrels")
            original_id = list_response.json()[0]["id"]
            requests.put(f"{base_url}/squirrels/{original_id}", data={"name": "Updated", "size": "small"})
            get_response = requests.get(f"{base_url}/squirrels/{original_id}")
            assert get_response.json()["id"] == original_id


    def describe_DELETE_squirrels_id():
        def returns_204(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "ToDelete", "size": "large"})
            list_response = requests.get(f"{base_url}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.delete(f"{base_url}/squirrels/{squirrel_id}")
            assert response.status_code == 204

        def returns_404(server, base_url):
            response = requests.delete(f"{base_url}/squirrels/9999")
            assert response.status_code == 404

        def removes_squirrel_from_database(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "ToDelete", "size": "large"})
            list_response = requests.get(f"{base_url}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.delete(f"{base_url}/squirrels/{squirrel_id}")
            list_response = requests.get(f"{base_url}/squirrels")
            assert len(list_response.json()) == 0

        def delete_specified_squirrel(server, base_url):
            requests.post(f"{base_url}/squirrels", data={"name": "Keep", "size": "large"})
            requests.post(f"{base_url}/squirrels", data={"name": "Delete", "size": "small"})
            list_response = requests.get(f"{base_url}/squirrels")
            delete_id = list_response.json()[1]["id"]
            requests.delete(f"{base_url}/squirrels/{delete_id}")
            list_response = requests.get(f"{base_url}/squirrels")
            assert len(list_response.json()) == 1
            assert list_response.json()[0]["name"] == "Keep"
