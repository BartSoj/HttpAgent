from src.auth_manager import AuthManager


def main():
    token_manager = AuthManager(api_clients_path="resources/api_clients/api_clients.json",
                                api_tokens_path="resources/api_clients/api_tokens.json")
    name = input("Enter the name of the client: ")
    access_token = input("Enter the access token: ")
    refresh_token = input("Enter the refresh token or leave empty to skip: ")
    expires_at = input("Enter the expiration time or leave empty to skip: ")

    token_manager.add_client_token_manually(name,
                                            access_token,
                                            refresh_token if refresh_token else None,
                                            expires_at if expires_at else None)


if __name__ == "__main__":
    main()
