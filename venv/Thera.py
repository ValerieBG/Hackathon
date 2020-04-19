"""
This is our project for the 2020 YETI Hackathon! After throwing around various ideas, we settled on a therapist robot, which we
believe has huge potential in increasing easy access to mental health care. This bot is not meant to replace a traditional
therapist, but rather to supplement one in times of need such as right now. We chose python as our programming language
because of its readability and usefulness for AI (but mostly because we couldn't resist the pun). None of us had had experience
with python in the past, so we immediately began learning the language. One key breakthrough that makes our bot stand out
is that it uses IBM Watson's tone analyzer to customize responses. We built our bot around the 7 tones provided by IBM's API.
One challenge we had was integrating our bot with a website, which was our initial plan. While we were able to set up
a website using flask, we ran out of time and weren't able to host our bot there. Overall, we had a lot of fun on this
project, especially with coming up with responses and making our insult bot, and enjoyed learning Python!
Enjoy!
-Sherry, Valerie, and Ben
"""

import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import random
import time

text = ""
mode = ""
name = ""


# Tone Analyzer class created (analyzes the user's tone using IBM Watson Tone Analyzer)
class ToneAnalyzer:

    # references cloud account to access an API key and service url to use the package
    def __init__(self):
        global tone_analyzer
        global authenticator
        authenticator = IAMAuthenticator('5H5rGMsQV9k61CQreRRATfsZ45UjJUVtE-V-PsThD8z2')
        tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            authenticator=authenticator
        )
        tone_analyzer.set_service_url(
        'https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/243e1e66-4f3a-43fc-a10e-37666cca200a')

    # creates a dictionary of tones and their intensity from a user input
    def getTone(self, inputText):
        global tone_analysis
        global tone_analyzer
        tone_analysis = tone_analyzer.tone(
            {'text': inputText},
            content_type='application/json'
        ).get_result()

# loops through each tone in the tone_analysis dictionary and identifies the strongest tone, allowing us to customize
# our responses around that tone
    def getStrongestTone(self, inputText):
        global tone_analysis
        self.getTone(inputText)
        strongestToneScore = 0
        strongestTone = ""
        for tone in tone_analysis.get('document_tone').get('tones'):
            if tone.get('score') > strongestToneScore:
                strongestToneScore = tone.get('score')
                strongestTone = tone.get('tone_id')
        return strongestToneScore, strongestTone


# Bot class handles all actions relating to responding to the user
class Bot:

    insults = []
    jokes = []
    questions = []
    therapyResponses = []
    x = False
    # the negative emotion counter is used to keep track of when the user is having too many negative emotions.
    negEmotionCounter = 0

# Bot constructor with response lists to avoid repetitive responses
    def __init__(self):
        self.insults = [
            "You suck",
            "You're an idiot",
            "I hate you",
            "Uhh did I ask?",
            "No one cares about you",
            "You're closer to your death than you've ever been",
            name + " is such an ugly name",
            "Why are you wasting time talking to a bot",
            "Sherry says hi!",
            "I would love to insult you, but i'm afraid i can't do as well as nature did",
            "Wow. it must be difficult exhausting your entire vocabulary in one sentence.",
            "I'd slap you, but that'd be animal abuse",
            "Nobody has ever loved you or ever will.",
            "Your grades are lower than your IQ.",
            "I bet you’re antivax.",
            "You listen to justin Beiber.",
            "I enjoy seeing you, it raises my own self esteem because of how much of a bad person you are.",
            "I think you just heightened my standards.",
            "I bet you cheated and still failed.",
            "I like myself more than I like you, and that says a lot.",
            "I bet you play fortnite.",
            "There is nothing good about your personality or your looks."
        ]
        self.jokes = [
            "I would tell you a joke about time travel, but you didn't like it",
            "I hate russian dolls. They're so full of themselves",
            "You know what's remarkable? Whiteboards."
                      ]
        self.questions = [
            "What positive changes would you like to see happen in your life?",
            "In general, how would you say your mood is?",
            "Have you ever experienced an ‘attack’ of fear, anxiety, or panic?",
            "Tell me about your day.",
            "What are some goals you'd like to set?"
        ]
        self.therapyResponses = [
            "How long have you been feeling this way?",
            "Have you told anyone else about how you feel?",
            "Are these feelings reoccurring?",
            "What is the severity of your situation?",
            "List the factors that have contributed to your feelings",
            "What sort of things would it take to make you happier or more at peace?"
        ]

    # changes mode to theraPY (nice bot) or theraCRY (insult bot) based on user input and alerts user
    def setMode(self, inputText):
        global mode
        if inputText == "0":
            mode = "py"
            print("You are now in theraPY mode. (1 at any time to switch to theraCRY mode, Q to quit)")
        elif inputText == "1":
            mode = "cry"
            print("You are now in theraCRY mode. (0 at any time to switch to theraPY mode, Q to quit")

# prints out each response the bot returns, waiting 1 second between each response to give the bot a lifelike quality.
# the bot waits longer when the response is "in" or "out" for when the user is angry and needs to take a deep breath
    def printResponses(self, response):
        for sentence in response:
            print(sentence)
            if sentence == "in" or sentence == "out":
                time.sleep(2.5)
            else:
                time.sleep(1)

# This function returns a list of responses based on the user's emotion.
    def getNiceBotResponse(self, inputText):
        response = []
        strongestToneScore = toneAnalyzer.getStrongestTone(inputText)[0]
        strongestTone = toneAnalyzer.getStrongestTone(inputText)[1]

        # the tone score is based on how strongly an emotion is felt, and the therapyst lets the user know it's okay to feel a lot of emotion
        # This response gets annoying after a while, so the therapist only says it once.
        randNum = random.randint(0, 4)
        if strongestToneScore > 0.95 and (not self.x):
            response.append("I understand you're feeling a lot of emotion right now and that's okay.")
            self.x = True

        # if the user is angry, the therapyst helps them take a deep breath.
        if strongestTone == "anger":
            response.append("I understand that you're mad right now.")
            response.append("Let's take a deep breath to calm down.")
            response.append("in")
            response.append("out")
            response.append("good job!")
            self.negEmotionCounter = self.negEmotionCounter + 1
        elif strongestTone == "fear":
            response.append("I know things can be scary sometimes.")
            self.negEmotionCounter = self.negEmotionCounter + 1
        elif strongestTone == "joy":
            response.append("I'm so happy for you!")
        elif strongestTone == "sadness":
            self.negEmotionCounter = self.negEmotionCounter + 1
            response.append("I'm sorry to hear that. What happened?")

        # We tell the user a joke if they're feeling sad over half of the time.
            randNum = random.randint(1, 4)
            if randNum >= 3:
                response.append("Here's a joke to cheer you up!")
                response.append(random.choice(self.jokes))
        elif strongestTone == "analytical":
            response.append("I'm glad you're thinking through the situation.")
            response.append("How does that make you feel?")
        elif strongestTone == "confident":
            response.append("I'm glad you're opening up!")
            response.append("Let's continue this dialogue.")
        elif strongestTone == "tentative":
            response.append("It's okay to be uncertain sometimes.")
            response.append("Let's talk through this together.")
        else:
            # When the user's response is less than 3 words, no emotion can be detected so this response is given.
            response.append("hmm can you elaborate on that?")

        # when the user is experience too many negative emotions, the bot is willing to provide resources.
        if self.negEmotionCounter > 10:
            response.append("you sound like you're going through some rough stuff.")
            response.append("i'm just a bot, so if you ever need more help, please call the suicide prevention hotline:")
            response.append("1-800-273-8255")

        # when the user is experiencing strong negative emotions, therapy asks questions to understand the issue
        if (strongestTone == "fear" or "sadness" or "anger") and strongestToneScore > .8:
            response.append(random.choice(self.therapyResponses))
        else:
            randNum = random.randint(0, 5)
            if randNum >= 4:
                response.append(random.choice(self.questions))
        return response

# The insult bot returns a random insult from our predefined list.
    def getMeanBotResponse(self, inputText):
        response = []
        strongestTone = toneAnalyzer.getStrongestTone(inputText)[1]
        if "I" in inputText:
            response.append("stop talking about yourself, did i ask?")
        if strongestTone == "joy":
            response.append("bruh why are u so happy? let's change that.")
        elif strongestTone == "sadness":
            response.append("haha u deserve that")
        elif strongestTone == "tentative":
            response.append("bruh could you be any more specific?")
        response.append(random.choice(self.insults))
        return response


# This runs at the beginning of the session to set the initial mode and greet the user.
def intro():
    global text
    global name
    print("Hello! I'm your therapyst! What is your name?")
    name = input()
    print("Hi " + name + "! What can I do for you today? (0 for theraPY, 1 for theraCRY)")
    text = input()
    myBot.setMode(text)

    # Continue asking for a mode until it is set.
    while mode == "":
        print("That was not a valid mode. Please try again. (0 for theraPY, 1 for theraCRY)")
        text = input()
        myBot.setMode(text)
    if mode == "py":
        print("I'm here to listen. How are you feeling today? ")
    elif mode == "cry":
        print("Oh boy I hate you already. How are you feeling today?")
    text = input()


# While the user hasn't pressed q, the bot continues to provide responses.
def conversation():
    global text
    while text != "Q":
        if mode == "cry":
            response = myBot.getMeanBotResponse(text)
        elif mode == "py":
            response = myBot.getNiceBotResponse(text)
        else:
            # Intellij wanted me to add an else condition so here we are
            response = ["this shouldn't happen"]
        myBot.printResponses(response)
        text = input()
        myBot.setMode(text)
    print("hope you enjoyed your session!")


# Here is the code that actually runs. First, our tone analyzer and bot objects are instantiated. Then, the intro and conversation happen.
def main():
    global myBot
    global toneAnalyzer
    myBot = Bot()
    toneAnalyzer = ToneAnalyzer()

    intro()
    conversation()


# calling main method here
main()