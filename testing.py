from time import sleep

def typingeffect(string):
    for i in string:
        print(i, end="", flush=True)
        sleep(0.1)

typingeffect("the qucik brown fox jumped over the lazy dog")