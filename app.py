from flask import Flask, request, render_template
from cosmos_requests import init_container, add_guest_cosmos, get_guest_list_cosmos, mark_guest_arrived_cosmos
from config import endpoint, key

app = Flask(__name__)

cosmos_container = init_container(endpoint, key)


@app.route("/")
def main_page():
    return render_template('main_page.html')


@app.route('/add_guest', methods=['POST'])
def add_guest():
    guest_name = request.form['nm']

    add_guest_cosmos(cosmos_container, guest_name)

    guest_lst = get_guest_list_cosmos(cosmos_container)

    return render_template('guest_list.html', guest_list=guest_lst)  # change


@app.route('/show_guest_list', methods=['POST'])
def show_guest_list():

    guest_lst = get_guest_list_cosmos(cosmos_container)
    return render_template('guest_list.html', guest_list=guest_lst)  # change


@app.route('/mark_guest_arrived', methods=['POST'])
def mark_guest_arrived():

    guest_name = request.form['nm']

    mark_guest_arrived_cosmos(cosmos_container, guest_name)
    guest_lst = get_guest_list_cosmos(cosmos_container)

    return render_template('guest_list.html', guest_list=guest_lst)  # change


if __name__ == '__main__':
   app.run()
