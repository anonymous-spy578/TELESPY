import json
import os
import time
import sys
import uuid
from datetime import datetime
from colorama import Fore, Style, Back, init
init(autoreset=True)
USERS_FILE = 'users.json'
MESSAGES_FILE = 'messages.json'
FUSERS_FILE = 'fusers.json'

def clear():
    os.system('cls' if os.name == 'nt'
        else 'clear')
        
def load_json(file):
    """Load JSON data from a file. Initialize with empty JSON if the file is missing or empty."""
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f, indent=4)
        return {}
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                data = {}
                with open(file, 'w') as f:
                    json.dump(data, f, indent=4)
            return data
    except json.JSONDecodeError:
        with open(file, 'w') as f:
            json.dump({}, f, indent=4)
        return {}  
        
def save_json(file, data):
    """Save data to a JSON file."""
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)        
    
def loading_animation():
    """Display loading animation."""
    animation= ['⌛ loading .....','⏳ loading .....']*10
    for frame in animation:
        time.sleep(0.9)
        sys.stdout.write("\r" + frame)
        sys.stdout.flush()
    clear()    
    print("\nLoading complete 😸")
    time.sleep(1)

def register(name, email, country, password):
    users= load_json(USERS_FILE)
    if email in users:
        print("You already have a telespy account")
        time.sleep(2)
        return main_menu()

    p2= "TS"
    username= name.replace(" ", "TS")+str(uuid.uuid4()) [:5]
    pin= p2.replace(" ", "2y")+str(uuid.uuid4()) [:5]
    users[email] ={
        'name': name,
        'username': username,
        'country': country,
        'pin': pin,
        'password': password
    }
    save_json(USERS_FILE, users)
    return pin
    
def login(email, password, pin):
    users= load_json(USERS_FILE)
    user= users.get(email)
    if user and user ['password'] == password:
        if user and user ['pin'] == pin:
            loading_animation()
            clear()
            print(f"🤗 Welcome {user['name']}")
            time.sleep(1.6)
            user_dashboard(user)
            return user
    print("\nInvalid credentials 🙊")
    time.sleep(3)
    return
            
def user_dashboard(user):
    clear()
    print("="*40)
    print("TELESPY".center(40))
    print("="*40)
    print(f"😺 {user['name']} pin: {user['pin']}".center(40))
    print("_"*40)
    print("\n1. 👥 Friends   |   2. 🔍 Discover")
    print("_"*40)
    print("\n0. 👤 Logout")
    print("_"*40)
    xx=input("\nWhat do you wish to explore: ")
    if xx == '1':
        friends(user)
    elif xx == '2':
        search(user)
    elif xx == '0':
        loading_animation()
        print("logging out.... ")
        time.sleep(2)
        return main_menu()
    else:
        print("invalid input")
        time.sleep(2)
        return user_dashboard(user)
    
def friends(user):
    clear()
    friends_list = load_json(FUSERS_FILE).get(user['username'], [])  # Load the friends list for the user
    
    print("="*40)
    print("FRIENDS".center(40))
    print("="*40)
    
    if not friends_list:  # If the user has no friends
        print("\nYou have no friends.")
        print("="*40)
        time.sleep(1.5)
        return user_dashboard(user)
    
    # Display the list of friends
    print("\n0. ↩️ Back")
    for idx, friend in enumerate(friends_list, 1):
        print(f"{idx}. {friend}")
    
    print("_"*40)
    
    # Prompt user to select a friend
    cf = input("\nOpen a chat with a specific friend (number): ")
    
    if cf == '0':  # Option to go back
        return user_dashboard(user)
    
    # Validate the user input and open the chat
    if cf.isdigit() and 1 <= int(cf) <= len(friends_list):
        selected_index = int(cf)
        selected_friend = friends_list[selected_index - 1]
        print(f"\nOpening chat with {selected_friend}...")
        time.sleep(1.5)
        return chat(user, selected_friend)  # Call the chat function with the selected friend
    else:
        print("\nInvalid input. Returning to the friends list...")
        time.sleep(1.5)
        return friends(user)
        
def chat(user, selected_friend):
    clear()
    print("=" * 40)
    print(f"Chatting with {selected_friend}".center(40))
    print("=" * 40)
    
    # Try to load the messages from the file, handle if file is empty or missing
    try:
        with open("messages.json", "r") as file:
            messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):  # Catch missing or invalid file
        messages = {}  # Initialize an empty dictionary if file is empty or invalid

    # Generate a unique chat key using both usernames (sorted alphabetically)
    chat_key = f"{min(user['username'], selected_friend)}-{max(user['username'], selected_friend)}"
    
    # Display chat history (if any)
    if chat_key in messages:
        print("\nChat History:")
        for message in messages[chat_key]:
            print(f"{message['sender']}: {message['message']} ({message['timestamp']})")
    else:
        print("\nNo messages yet.")
    
    print("_" * 40)

    # Input loop to keep the chat active
    while True:
        msg = input("\nType a message (or type 'exit' to leave the chat): ")
        
        if msg.lower() == 'exit':
            break

        # Create a new message entry
        new_message = {
            "sender": user['username'],
            "message": msg,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }

        # Add the message to the conversation history
        if chat_key not in messages:
            messages[chat_key] = []
        
        messages[chat_key].append(new_message)
        
        # Save the updated messages to messages.json
        with open("messages.json", "w") as file:
            json.dump(messages, file, indent=4)
        
        print(f"\n{user['username']}: {msg}")
        time.sleep(0.5)  # Simulate message being sent

    return friends(user)  # Return to the friends list after exiting the chat
    
def search(user):
    users = load_json(USERS_FILE)
    clear()
    print("="*40)
    print("Discover new friends".center(40))
    print("\n0. ↩️ Back")
    print("_"*40)
    sf=input("\nsearch a friend username: ")
    if sf == '0':
        return user_dashboard(user)
    elif sf == user['username']:
        print("Your are trying to search yourself 🫤")
        time.sleep(1.3)
        return search(user)
    user_found = False
    for user_data in users.values():
        if sf == user_data['username']:
            user_found = True
            print(f"{user_data['name']}")
            cm = input("Add Friend (Yes/No) ")
            if cm == 'Yes':
                save_friend(user, sf)
            elif cm == 'No':
                print("Cancelling.... ")
                time.sleep(1.4)
                return search(user)
            else:
                print("invalid input")
                return search(user)
    if not user_found:
        print("No user found 🚫")
        time.sleep(1.4)
        return search(user)
    
def save_friend(user, friend_username):
    friends = load_json(FUSERS_FILE)
    
    # Check if they are already friends
    if user['username'] in friends and friend_username in friends[user['username']]:
        print("You are both already friends")
        time.sleep(1.4)
        return search(user)
    
    # Add user to the friends list if they are not already in the file
    if user['username'] not in friends:
        friends[user['username']] = []
    
    # Add the friend's username to the user's friends list
    friends[user['username']].append(friend_username)
    
    # Add the user's username to the friend's list to ensure mutual friendship
    if friend_username not in friends:
        friends[friend_username] = []
    
    if user['username'] not in friends[friend_username]:
        friends[friend_username].append(user['username'])
        
    # Save the updated friends list to the file
    save_json(FUSERS_FILE, friends)
    print("Friend request sent")
    time.sleep(1.6)
    
    return search(user)
    
def main_menu():
    # Added an indented block of code here
    while True:
        clear()
        loading_animation()
        clear()
        print("="*40)
        print("TELESPY".center(40))
        print("="*40)
        print("\n1. Register")
        print("2. Login")
        print("0. Exit")
        main = input("Pick a choice: ")
        
        if main == '1':
            clear()
            print("="*40)
            print("Register".center(40))
            print("="*40)
            name = input("\nWhat is your name: ")
            email = input("What is your email: ")
            country = input("What is your country: ")
            password = input("Create a password: ")
            pin = register(name, email, country, password)
            if pin:
                print("Registration successful!")
                print(f"Your access pin is: {pin}")
                print("Keep it safe")
                lol=input("Type 0 to return: ")
                if lol == '0':
                    return main_menu()
        
        elif main == '2':
            clear()
            print("="*40)
            print("Login".center(40))
            print("="*40)
            email = input("\nWhat is your email: ")
            password = input("What is your password: ")
            access_pin = input("What is your access pin: ")
            login(email, password, access_pin)
        
        elif main == '0':
            print("Exiting.....")
            time.sleep(2)
            clear()
            break
if __name__ == '__main__':
    main_menu()