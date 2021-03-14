from flask import render_template, Blueprint

main = Blueprint(name='main', import_name='main')


@main.route("/", methods=['GET'])
@main.route("/home", methods=['GET'])
def home():
    return render_template('home.html')
