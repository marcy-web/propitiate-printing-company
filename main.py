import textwrap
import shutil
from time import sleep

word_tags = {
    "i": ["player"],
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
    "anne": ["anne"]
}

response_dict = {
    "player affection anne": ["aww, that's very sweet <3"],
    "who milly": ["what a silly question. that's you of course!"]
}

terminal_width = shutil.get_terminal_size().columns
user_input_parsed = ""
player_name = "milly"
response = ""
# initial_message = "It's been 20833 days since the incident. You don't know too much about what happened. It was before your time. Sheets of rain are pouring from the sky today. You go into an old building to get out of the storm. 'Propitiate Printing Company'. Room after room is ruined. But there's one that looks relatively untouched with a terminal on a desk. You sit down and see a blinking cursor."
# first_response = "Oh my gosh, Milly! It's been a long time! Any news?"

# wrapped_response = textwrap.fill(initial_message, width=terminal_width)

# for char in wrapped_response:
#         print(char, end="", flush=True)
#         sleep(0.05)

# contact = input("\n> ")
# wrapped_response = textwrap.fill(first_response, width=terminal_width)

# for char in wrapped_response:
#         print(char, end="", flush=True)
#         sleep(0.05)

# game loop
running = True
while running:
    user_input = input("\n> ")
    
    # response = f"'{user_input}', huh? Tell me more."
    user_input_split = user_input.split()
    for word in user_input_split:
        user_input_parsed
        if word in word_tags:
            user_input_parsed += " ".join(word_tags.get(word)) + " "

    user_input_parsed = user_input_parsed.strip()
    for key in response_dict:
        if user_input_parsed == key:
            response += " ".join(response_dict.get(key)) + " "
    print(response)
    # print(user_input_parsed)

    # print(response)
    # wrapped_response = textwrap.fill(response, width=terminal_width)

    # for char in wrapped_response:
    #     print(char, end="", flush=True)
    #     sleep(0.05)