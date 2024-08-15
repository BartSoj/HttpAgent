from src.auth_manager import AuthManager


def main():
    token_manager = AuthManager(api_clients_path="../../resources/api_clients/api_clients.json")
    token_manager.add_client_tokens()


if __name__ == "__main__":
    main()
