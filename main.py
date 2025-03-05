import textwrap
import shutil
from time import sleep
import readline
from datetime import datetime
import string

response = ""

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
    "we": ["player", "anne"],
    "want": ["desire"],
    "look around": ["explore"],
    "explore": ["explore"],
    "remove": ["remove"],
    "take off": ["remove"],
    "clothes": ["clothes"],
    "clothing": ["clothes"],
    "take": ["take"],
    "off": ["off"],
    
}

response_dict = {
    "player affection anne": ["Aww, that's very sweet <3"],
    "player affection anne anne": ["Aww, that's very sweet <3"],
    "question identity milly": ["What a silly question. That's you of course!"],
    "greeting casual": ["Hey!"],
    "greeting casual anne": ["Hey!"],
}

interactable_objects = {
    "apple": {
        "eat": "You take a bite of the ancient apple. It makes you feel sick...",
        "throw": "You chuck the apple on the ground. It spletters with a squelch."
    }
}

# exploration_dict = {
# }

magicae_list = ["magic", "magicae", "compendium"]

game_state = "chatting"

player_input = ""
terminal_width = shutil.get_terminal_size().columns
player_input_parsed = ""
running = False
strip_punctuation = string.punctuation.replace("'", "")

#story
introduced_to_player = False
player_name = "Milly"

has_visited_basement = False
has_found_compendium = False

#exploring
clothes_off = False
is_sitting = True
current_location_general = "milly_office"
current_location_specific = "milly_desk"



def parse_player_input():
    global player_input, has_found_compendium, player_input_parsed
    player_input = player_input.lower()
    player_input = player_input.translate(str.maketrans('', '', strip_punctuation))
    player_input_split = player_input.split()
    player_input_parsed = ""

    for word in player_input_split:
        if word in word_tags:
            player_input_parsed += " ".join(word_tags.get(word)) + " "

        if word in magicae_list:
            if not has_found_compendium:
                magic_mention()
                return

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
    elif player_input_parsed == "question identity anne":
        if not introduced_to_player:
            response = "I'm Anne! Don't you remember?"
        else:
            response = "I'm Anne. Milly created me... a long time ago."
    elif player_input_parsed == "player desire explore":
        stop_chatting()
        return
    else:
        for key in response_dict:
            if player_input_parsed == key:
                response += " ".join(response_dict.get(key)) + " "

    if response == "" or response == " ":
        response = "I have *no* idea what you're talking about"
    
    display_response()

def display_response():
    global response
    response = textwrap.fill(response, width=terminal_width)
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
        response = "Oh... who are you then?"
        display_response()
        player_name = input("\n> ")
        player_name = player_name.translate(str.maketrans('', '', string.punctuation))
        player_name = player_name.split()[-1]
        player_name = player_name.capitalize()
        response = f"Hello, {player_name}. It's nice to meet you"
        display_response()
        introduced_to_player = True
        return
    response = f"I know. you're {player_name}."
    display_response()

def magic_mention():
    global response
    response = "Do you believe in magic?"
    display_response()
    answer = input("\n> ")
    response = "Interesting..."
    display_response()

def stop_chatting():
    global response, game_state
    response = f"Ok. See you soon {player_name}!"
    display_response()
    game_state = "exploring"


#exploration
def parse_exploration_input():
    global player_input, player_input_parsed, clothes_off
    player_input = player_input.lower()
    player_input = player_input.translate(str.maketrans('', '', strip_punctuation))
    player_input_split = player_input.split()
    player_input_parsed = ""

    for word in player_input_split:
        if word in word_tags:
            player_input_parsed += " ".join(word_tags.get(word)) + " "

    player_input_parsed = player_input_parsed.strip()
    generate_exploration_response()

def generate_exploration_response():
    global response
    response = ""

    if player_input_parsed == "greeting casual":
        response = f"'{player_input.capitalize()}' echoes off the walls of the room. Feeling lonely?"
    elif player_input_parsed == "remove clothes" or player_input_parsed == "remove player clothes" or player_input_parsed == "take clothes off":
        response = "You peel off your clothes. Raincoat, blouse, bra, skirt, stockings, underwear. And leave them in a heap on the floor"
        clothes_off = True
    else:
        response = "I have no idea what you're talking about..."

    display_response()

start_game()

# game loop
while running:
    if game_state == "chatting":
        player_input = input("\n> ")
        parse_player_input()
    elif game_state == "exploring":
        player_input = input("\n> [Exploring] ")
        parse_exploration_input()