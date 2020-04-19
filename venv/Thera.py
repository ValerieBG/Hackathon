import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import random
import time

text = ""
mode = ""
name = ""


def setUpToneAnalyzer():
    authenticator = IAMAuthenticator('5H5rGMsQV9k61CQreRRATfsZ45UjJUVtE-V-PsThD8z2')
    global tone_analyzer
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator
    )
    tone_analyzer.set_service_url(
        'https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/243e1e66-4f3a-43fc-a10e-37666cca200a')


def getTone(inputText):
    global tone_analysis
    global tone_analyzer
    tone_analysis = tone_analyzer.tone(
        {'text': inputText},
        content_type='application/json'
    ).get_result()


def setMode(inputText):
    global mode
    if inputText == "0":
        mode = "py"
        print("you are now in therapy mode. rant away!")
    elif inputText == "1":
        mode = "cry"
        print("you are now in theracry mode. i have no mercy.")


def getStrongestTone(inputText):
    global tone_analysis
    getTone(inputText)
    strongestToneScore = 0
    strongestTone = ""
    for tone in tone_analysis.get('document_tone').get('tones'):
        if tone.get('score') > strongestToneScore:
            strongestToneScore = tone.get('score')
            strongestTone = tone.get('tone_id')
    return strongestToneScore, strongestTone

class Bot():

    insults = []
    jokes = []
    negEmotionCounter = 0;

    def __init__(self):
        self.insults = ["you suck", "you're an idiot", "i hate you", "uhh did i ask?", "no one cares about you",
                   "you're closer to your death than you've ever been :)", name + " is such an ugly name",
                        "why are you wasting time talking to a bot", "sherry says hi!",
                        "i would love to insult you, but i'm afraid i can't do as well as nature did",
                        "wow. it must be difficult exhausting your entire vocabulary in one sentence.",
                        "i'd slap you, but that'd be animal abuse"]
        self.jokes = ["I would tell you a joke about time travel, but you didn't like it",
                      "I hate russian dolls. They're so full of themselves",
                      "You know what's remarkable? Whiteboards."
                      ]

    def getNiceBotResponse(self, inputText):
        response = []
        strongestToneScore = getStrongestTone(inputText)[0]
        strongestTone = getStrongestTone(inputText)[1]
        if strongestToneScore > 0.95:
            response.append("I understand you're feeling a lot of emotion right now and that's okay.")
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
            randNum = random.randint(0, 5)
            if randNum > 4:
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
            response.append("hmm can you elaborate on that?")
        if self.negEmotionCounter > 10:
            response.append("you sound like you're going through some rough stuff")
            response.append("i'm just a bot, so if you ever need real help call the suicide prevention hotline:")
            response.append("1-800-273-8255")
        response.append("Q to quit")
        return response

    def getMeanBotResponse(self, inputText):
        response = []
        strongestTone = getStrongestTone(inputText)[1]
        if "I" in inputText:
            response.append("stop talking about yourself, did I ask?")
        if strongestTone == "joy":
            response.append("bruh why are u so happy? let's change that.")
        elif strongestTone == "sadness":
            response.append("haha u deserve that")
        elif strongestTone == "tentative":
            response.append("bruh could you be any more specific?")
        response.append(random.choice(self.insults))
        return response


def intro():
    global text
    global name
    print("Hello! I'm your therapyst! What is your name?")
    name = input()
    print("Hi ", name, "! What can I do for you today? (0 for theraPY, 1 for theraCRY)")
    text = input()
    setMode(text)
    while mode == "":
        print("That was not a valid mode. Please try again.")
        text = input()
        setMode(text)
    if mode == "py":
        print("I'm ready to help! How are you feeling today? (1 at any time to switch to theraCRY mode, Q to quit)")
    elif mode == "cry":
        print("Oh boy I hate you already. How are you feeling today? "
              "(0 at any time to switch to theraPY mode, Q to quit")
    text = input()


def printResponses(response):
    for sentence in response:
        print(sentence)
        if sentence == "in" or sentence == "out":
            time.sleep(2)
        else:
            time.sleep(1)

def conversation():
    global text
    myBot = Bot()
    while text != "Q":
        if mode == "cry":
            response = myBot.getMeanBotResponse(text)
        elif mode == "py":
            response = myBot.getNiceBotResponse(text)
        else:
            response = ["this shouldn't happen"]
        printResponses(response)
        text = input()
        setMode(text)
    print("hope you enjoyed your session!")


def main():
    setUpToneAnalyzer()
    intro()
    conversation()

main()