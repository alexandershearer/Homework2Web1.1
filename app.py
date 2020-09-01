from flask import Flask, request, render_template
import random

app = Flask(__name__)

def sort_letters(message):
    """A helper method to sort the characters of a string in alphabetical order
    and return the new string."""
    return ''.join(sorted(list(message)))


@app.route('/')
def homepage():
    """A homepage with handy links for your convenience."""
    return render_template('home.html')

@app.route('/froyo', methods=['POST', 'GET'])
def choose_froyo():
    """Shows a form to collect the user's Fro-Yo order."""

    context = {
        "users_froyo_flavor": request.args.get('flavor'),
        "users_froyo_toppings": request.args.get('toppings')
    }

    return render_template('froyo_form.html', **context)


@app.route('/froyo_results')
def show_froyo_results():
    context = {
    "users_froyo_flavor": request.args.get('flavor'),
    "users_froyo_toppings": request.args.get('toppings')
    }
    return render_template("froyo_results.html", **context)

@app.route('/favorites', methods=['POST', 'GET'])
def favorites():
    return """
    <form action="/favorites_results" method="GET">
    <p>Favorite Color</p>
    <label for="color" value="Favorite Color">
    <input type="text" name="color"> <br/>
    <p>Favorite Animal</p>
    <label for"animal" value="Favorite Animal">
    <input type="text" name="animal"> <br/>
    <p>Favorite City</p>
    <label for="city" value="Favorite City">
    <input type="text" name="city"> <br/>
    <input type="submit" value="Submit">
    </form>
    """


@app.route('/favorites_results')
def favorites_results():
    favorite_color = request.args.get('color')
    favorite_animal = request.args.get('animal')
    favorite_city = request.args.get('city')
    return f"Wow, I didn't know {favorite_color} {favorite_animal} lived in {favorite_city}!"



@app.route('/secret_message')
def secret_message():
    """Shows the user a form to collect a secret message. Sends the result via
    the POST method to keep it a secret!"""
    return """
    <form action="/message_results", method="POST">
    <p>Enter a passphrase.</p>
    <input type="text" name="secret_message"> <br/>
    <input type="submit" value="Submit">
    </form>
    """

@app.route('/message_results', methods=['POST'])
def message_results():
    secret_message = request.form.get('secret_message')
    return f"{sort_letters(secret_message)}"

@app.route('/calculator')
def calculator():
    """Shows the user a form to enter 2 numbers and an operation."""
    return render_template('calculator_form.html')


@app.route('/calculator_results')
def calculator_results():
    """Shows the user the result of their calculation."""
    num1 = int(request.args.get('operand1'))
    num2 = int(request.args.get('operand2'))
    operation = request.args.get('operation')
    answer = None

    if operation == 'add':
        answer = num1 + num2
    elif operation == 'subtract':
        answer = num1 - num2
    elif operation == 'multiply':
        answer = num1 * num2
    elif operation == 'divide':
        answer = num1 / num2

    context = {
        'answer': answer,
        'operation': operation,
        'num1': num1,
        'num2': num2
    }


    return render_template('calculator_results.html', **context)


# List of compliments to be used in the `compliments_results` route (feel free 
# to add your own!) 
# https://systemagicmotives.com/positive-adjectives.htm
list_of_compliments = [
    'awesome',
    'beatific',
    'blithesome',
    'conscientious',
    'coruscant',
    'erudite',
    'exquisite',
    'fabulous',
    'fantastic',
    'gorgeous',
    'indubitable',
    'ineffable',
    'magnificent',
    'outstanding',
    'propitioius',
    'remarkable',
    'spectacular',
    'splendiferous',
    'stupendous',
    'super',
    'upbeat',
    'wondrous',
    'zoetic'
]

@app.route('/compliments')
def compliments():
    """Shows the user a form to get compliments."""
    return render_template('compliments_form.html')

@app.route('/compliments_results')
def compliments_results():
    """Show the user some compliments."""
    name = request.args.get('users_name')
    fetch_compliments = request.args.get('wants_compliments')
    num_compliments = int(request.args.get('num_compliments'))
    result = f'{name}, you are ' 
    dupe = False

    if fetch_compliments == 'no':
        result = f'Have a nice day, {name}!'
    else: 
        for index in range(0, num_compliments):
            word = random.choice(list_of_compliments)
            if word in result:
                dupe = True
            while dupe:
                word = random.choice(list_of_compliments)
                if word not in result:
                    break
            if index == num_compliments - 1:
                result += f'and {word}.'
            else:
                result += word + ', '

    return render_template('compliments_results.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
