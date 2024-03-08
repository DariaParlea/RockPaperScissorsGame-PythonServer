import socket
import random

# List of words for the game
words = ["hangman", "computer", "python", "programming", "challenge"]

# Choose a random word
chosen_word = random.choice(words)
word_length = len(chosen_word)

# Initialize the game state
guessed_word = ["_" for _ in range(word_length)]
attempts = 6

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind(("0.0.0.0", 12345))

# Listen for incoming connections
server_socket.listen(1)
print("Hangman Server is listening...")

# Accept a connection from a client
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

# Send initial game information to the client
initial_data = f"Word: {' '.join(guessed_word)}   Attempts left: {attempts}"
client_socket.send(initial_data.encode())

while attempts > 0:
    # Receive the guessed letter from the client
    guessed_letter = client_socket.recv(1).decode()

    if guessed_letter in chosen_word:
        for i in range(word_length):
            if chosen_word[i] == guessed_letter:
                guessed_word[i] = guessed_letter
    else:
        attempts -= 1

    # Send updated game information to the client
    game_data = f"Word: {' '.join(guessed_word)}   Attempts left: {attempts}"
    client_socket.send(game_data.encode())

    # Check if the game is won or lost
    if "_" not in guessed_word:
        client_socket.send("You win!\n".encode())
        break
    if attempts == 0:
        client_socket.send(f"You lose! The word was: {chosen_word}\n".encode())
        break

# Close the client socket
client_socket.close()
server_socket.close()
