from Minesweeper import Minesweeper
from AI import Knowledge_AI
from flask import Flask, request, jsonify, render_template as RT

app = Flask(__name__)

@app.route('/')
def root():
    return RT("main.html", board=None)


@app.route('/initialise', methods=['POST'])
def initialise():
    size = request.get_json()['size']

    global ms
    ms = Minesweeper(size)
    board = ms.get_board()

    global flagged
    flagged = set()

    global knowledge
    knowledge = Knowledge_AI(size)

    return jsonify({"board": board})


@app.route('/dig', methods=['POST'])
def dig():
    x, y = request.get_json()['coords'].split(" ")
    x, y = int(x), int(y)

    result = ms.turn(x, y)
    board = ms.get_board()
    uncovered = ms.get_uncovered()
    return jsonify({"board": board, "uncovered":uncovered, "flagged":list(flagged), "result":result})

@app.route('/flag', methods=['POST'])
def flag():
    x, y = request.get_json()['coords'].split(" ")
    x, y = int(x), int(y)

    flagged.add((x, y))
    return jsonify({"flagged":list(flagged)})

@app.route('/dig_ai', methods=['POST'])
def dig_ai():
    ai_board = ms.get_board()
    coords, flagged = knowledge.play(ai_board)
    result = ms.turn(coords[0], coords[1])

    board = ms.get_board()
    uncovered = ms.get_uncovered()

    return jsonify({"board":board, "uncovered":uncovered, "flagged":list(flagged), "result":result})



# Run the app
if __name__ == '__main__':
    app.run(debug=True)