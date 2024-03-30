import ipaddress
import socket


def get_choice():
    choice = input("Choose rock (r), paper (p), or scissors (s): ").lower()
    while choice not in ['r', 'p', 's']:
        print("Invalid choice. Please choose again.")
        choice = input("Choose rock (r), paper (p), or scissors (s): ").lower()
    return choice


def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return "tie"
    elif (choice1 == 'r' and choice2 == 's') or \
            (choice1 == 'p' and choice2 == 'r') or \
            (choice1 == 's' and choice2 == 'p'):
        return "win"
    else:
        return "lose"


def play_game(connection):
    scores = {"win": 0, "lose": 0, "tie": 0}
    for _ in range(3):
        player_choice = get_choice()
        connection.sendall(player_choice.encode('utf-8'))
        opponent_choice = connection.recv(1024).decode('utf-8')
        result = determine_winner(player_choice, opponent_choice)
        scores[result] += 1
        print(f"Round result: You {result}.")
    return scores


def run_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            scores = play_game(conn)
            print(f"Game over. Scores: {scores}")


def run_client(server_host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_host, port))
        print(f"Connected to {server_host}:{port}")
        scores = play_game(s)
        print(f"Game over. Scores: {scores}")


if __name__ == "__main__":
    choice = input("Do you want to host a game (h) or connect to a game (c)? ").lower()
    if choice == 'h':
        run_server()
    elif choice == 'c':
        ip_address = input("Enter the host IP address: ")
        try:
            host = ipaddress.ip_address(ip_address)
            print(f"{ip_address} is a valid {host.version} IP address.")
            run_client(str(host))
        except ValueError:
            print(f"{ip_address} is not a valid IP address.")

    else:
        print("Invalid choice.")
