import requests


def print_answer(content, role):
    print(f"\n## {role}")
    print("-" * (len(role) + 3))
    print(content)
    print()


def get_user_input(role):
    print(f"\n## {role}")
    print("-" * (len(role) + 3))
    user_input = input()
    print()
    return user_input


def run(user_name, agent_name, agent_url):
    while True:
        user_input = get_user_input(user_name)
        if user_input == "exit":
            break
        response = requests.post(agent_url, json={"content": user_input})
        print_answer(response.text, agent_name)


def main():
    run("User", "Assistant", "http://localhost:8000/")


if __name__ == "__main__":
    main()
