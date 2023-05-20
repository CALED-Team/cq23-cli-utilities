import os
import subprocess
import sys

import docker

from utils import restore_cwd


def check_dockerfile_exists():
    current_dir = os.getcwd()
    dockerfile_path = os.path.join(current_dir, "Dockerfile")

    if os.path.isfile(dockerfile_path):
        print("Dockerfile found.")
    else:
        raise Exception(
            "Dockerfile not found! Make sure you run `cq23_run` from the directory that contains your bot's"
            "Dockerfile."
        )


def build_and_tag_image(image_tag):
    client = docker.from_env()
    current_dir = os.getcwd()
    dockerfile_path = os.path.join(current_dir, "Dockerfile")

    # Build the Docker image
    image, _ = client.images.build(
        path=current_dir, dockerfile=dockerfile_path, tag=image_tag
    )

    # Print the ID of the built image
    print("Docker image built with ID:", image.id)


def clone_or_pull_repository(repository_url, folder_path):
    if not os.path.exists(folder_path):
        # Clone the repository if the folder doesn't exist
        subprocess.run(["git", "clone", repository_url, folder_path])
    else:
        # Pull the latest changes if the folder already exists
        current_dir = os.getcwd()
        os.chdir(folder_path)
        subprocess.run(["git", "pull"])
        os.chdir(current_dir)


@restore_cwd
def run_game():
    print(sys.argv)
    return
    game_files_dir = ".game_files"
    gcs_folder_name = "gcs"
    gcs_repo = "https://github.com/CALED-Team/game-communication-system.git"
    client_image_tag = "local-dev-client:latest"

    check_dockerfile_exists()
    build_and_tag_image(client_image_tag)

    if not os.path.exists(game_files_dir):
        os.makedirs(game_files_dir)
    os.chdir(game_files_dir)

    clone_or_pull_repository(gcs_repo, gcs_folder_name)
