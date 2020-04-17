from flask import Flask, render_template, request

app = Flask(__name__)

text = ""
text = "hello i am your therapyst how are u feeling today?"

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


