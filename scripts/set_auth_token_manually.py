from httpagent.auth_manager import AuthManager


def main():
    token_manager = AuthManager(api_clients_path="resources/api_clients/api_clients.json",
                                api_tokens_path="resources/api_clients/api_tokens.json")
    name = input("Enter the name of the client: ")
    access_token = input("Enter the access token: ")
    refresh_token = input("Enter the refresh token or leave empty to skip: ")
    expires_at = input("Enter the expiration time or leave empty to skip: ")
    scope = input("Enter the scope or leave empty to skip: ")
    prefix = input("Enter the authorization header prefix or leave empty to skip: ")

    params = {"access_token": access_token}
    if refresh_token:
        params["refresh_token"] = refresh_token
    if expires_at:
        params["expires_at"] = expires_at
    if scope:
        params["scope"] = scope
    if prefix:
        params["prefix"] = prefix

    token_manager.add_client_token_manually(name, **params)


if __name__ == "__main__":
    main()
