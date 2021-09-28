from flask import Flask, render_template, request

import scrapper
app = Flask(__name__)


@app.route('/', methods=["GET","POST"])
def hello_world():  # put application's code here
    if request.method == 'POST':
        # url = 'https://www.4match.nl/wachtwoord-vergeten'
        email = request.form['InputEmail']
        results = scrapper.mainscrapper(email)
        return render_template('index.html',results=results,display="block")
    return render_template('index.html',display='none')


if __name__ == '__main__':
    app.run(debug=True)
