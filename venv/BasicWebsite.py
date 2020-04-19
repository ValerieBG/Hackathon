from flask import Flask, render_template, request

"""
Our initial idea was to have the therapyst run on a website.
After experimenting with flask ( and some borrowed code ), we were able to create this basic website.
However, with the time constraint we were unable to integrate our terminal based bot with our website in time.
If you run this, you get a very nice looking but ultimately very useless therapyst.
In the future, we hope to host our bot on a website for easy access.
"""

app = Flask(__name__)

text = "Hello! I am your therapyst, how are u feeling today?"

@app.route("/")
def home():
    return render_template("home.html")

class Bot:
    response = ""
    def __init__(self):
        self.response = "hello"
    def get_response(self, txt):
        return self.response

bot = Bot()

def get_bot_response():
    userText = request.args.get('msg')
    return str(bot.get_response(userText))

def runApp():
    if __name__ == "__main__":
        app.run()

def main():
    runApp()

main()


