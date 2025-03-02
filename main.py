import textwrap
import shutil
from time import sleep
import readline
from datetime import datetime
import string

word_tags = {
    "i": ["player"],
    "i'm": ["player"],
    "me": ["player"],
    "my": ["player", "possessive"],
    "who": ["question", "identity"],
    "what": ["question", "information"],
    "when": ["question", "time"],
    "where": ["question", "location"],
    "why": ["question", "reason"],
    "how": ["question", "method"],
    "love": ["affection"],
    "you": ["anne"],
    "milly": ["milly"],
    "anne": ["anne"],
    "hi": ["greeting", "casual"],
    "time": ["time"],
    "not": ["not"],
    "we": ["player", "anne"]
}

response_dict = {
    "player affection anne": ["aww, that's very sweet <3"],
    "player affection anne anne": ["aww, that's very sweet <3"],
    "question identity milly": ["what a silly question. that's you of course!"],
    "greeting casual": ["hey!"],
    "greeting casual anne": ["hey!"],
    "question identity anne": ["It's Anne! Don't you remember?"]
}

player_input = ""
terminal_width = shutil.get_terminal_size().columns
player_input_parsed = ""
response = ""
running = False

#story
introduced_to_player = False
player_name = "milly"



def parse_player_input():
    player_input_split = player_input.split()
    global player_input_parsed
    player_input_parsed = ""

    for word in player_input_split:
        if word in word_tags:
            player_input_parsed += " ".join(word_tags.get(word)) + " "

    player_input_parsed = player_input_parsed.strip()
    generate_response()

def generate_response():
    global response
    response = ""

    if player_input_parsed == "question information time":
        current_time = datetime.now().strftime("%H:%M:%S")
        response = f"It's {current_time}"
    elif player_input_parsed == "player not milly":
        introductions()
        return
    else:
        for key in response_dict:
            if player_input_parsed == key:
                response += " ".join(response_dict.get(key)) + " "
    
    response = textwrap.fill(response, width=terminal_width)
    display_response()

def display_response():
    for char in response:
        print(char, end="", flush=True)
        sleep(0.05)

#story chapters

def start_game():
    initial_message = "It's been 20833 days since the incident. You don't know too much about what happened. It was before your time. Sheets of rain are pouring from the sky today. You go into an old building to get out of the storm. 'Propitiate Printing Company'. Room after room is ruined. But there's one that looks relatively untouched with a terminal on a desk. You sit down and see a blinking cursor."
    first_response = "Oh my gosh, Milly! It's been a long time! Any news?"
    wrapped_response = textwrap.fill(initial_message, width=terminal_width)
    global running

    for char in wrapped_response:
        print(char, end="", flush=True)
        sleep(0.05)

    contact = input("\n> ")
    wrapped_response = textwrap.fill(first_response, width=terminal_width)

    for char in wrapped_response:
        print(char, end="", flush=True)
        sleep(0.05)
    running = True

def introductions():
    global introduced_to_player
    if not introduced_to_player:
        global response
        global player_name
        response = "oh... who are you then?"
        display_response()
        player_name = input("\n> ")
        player_name = player_name.translate(str.maketrans('', '', string.punctuation))
        player_name = player_name.split()[-1]
        response = f"hello, {player_name}. it's nice to meet you"
        display_response()
        introduced_to_player = True
        return
    response = f"i know. you're {player_name}."
    display_response()

start_game()

# game loop
while running:
    player_input = input("\n> ")
    parse_player_input()