import os
from src.openai_client import OpenAIClient


def get_or_create_vector_store(client, vector_store_name):
    try:
        vector_store = client.beta.vector_stores.retrieve(vector_store_name)
        print(f"Retrieved existing vector store: {vector_store_name}")
    except Exception as e:
        print(f"Vector store {vector_store_name} not found. Creating new one.")
        vector_store = client.beta.vector_stores.create(name=vector_store_name)
        print(f"Created new vector store: {vector_store_name}")
    return vector_store


def upload_api_references(client):
    vector_store_name = "APIs"
    vector_store = get_or_create_vector_store(client, vector_store_name)

    file_dir = "../../resources/apis"
    file_paths = [os.path.join(file_dir, f) for f in os.listdir(file_dir)]
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
