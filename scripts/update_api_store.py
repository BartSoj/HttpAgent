import os
from utils.openai_client import OpenAIClient


def get_or_create_vector_store(client, vector_store_name):
    vector_stores = client.beta.vector_stores.list()
    matching_store = next((store for store in vector_stores.data if store.name == vector_store_name), None)

    if matching_store:
        print(f"Retrieved existing vector store: {vector_store_name}")
        return matching_store
    else:
        print(f"Vector store {vector_store_name} not found. Creating new one.")
        vector_store = client.beta.vector_stores.create(name=vector_store_name)
        print(f"Created new vector store: {vector_store_name}")
        return vector_store


def get_existing_files(client, vector_store_id):
    files_in_vector_store = client.beta.vector_stores.files.list(vector_store_id)
    return set(client.files.retrieve(file.id).filename for file in files_in_vector_store)


def upload_api_references(client):
    vector_store_name = "APIs"
    vector_store = get_or_create_vector_store(client, vector_store_name)

    existing_files = get_existing_files(client, vector_store.id)
    file_dir = "../resources/apis"
    local_files = set(os.listdir(file_dir))

    new_files = local_files - existing_files
    if not new_files:
        print("No new files to upload.")
        return

    file_paths = [os.path.join(file_dir, f) for f in new_files]
    file_streams = [open(path, "rb") for path in file_paths]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    print(f"File batch status: {file_batch.status}")
    print(f"File counts: {file_batch.file_counts}")

    for stream in file_streams:
        stream.close()


def main():
    client = OpenAIClient().get_client()
    upload_api_references(client)


if __name__ == "__main__":
    main()
