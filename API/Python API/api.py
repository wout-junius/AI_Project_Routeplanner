from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import render_template
from switchcase import switch
import json

app = Flask(__name__)
api = Api(app)
moveQue = []


class index(Resource):
    def get(self):
        return "test"

class moves(Resource):
    def get(self):
        return MoveQue

class position(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Start')
        parser.add_argument('dest')
        args = parser.parse_args()
        #Import AI
        #moveQue = getRout(args, map)
        return {'mssg': "Success"}

api.add_resource(index, '/')

api.add_resource(position, '/position')
api.add_resource(moves, '/moves')

if __name__ == '__main__':
    app.run(debug=True)

def RouteToMoves(robotDirection):
    lastDirection = ""
    for m in moveQue:
        lastDirection = m.lastDirection
        if m.Direction == moveQue[m.OrderNr-1].Direction:
            m.Direction = 'F'
        else:
            for case in switch(0):
                if case("D"):
                    m.Direction = "R" if m.Direction == "L" else "L"
                    break
                if case("R"):
                    m.Direction = "L" if m.Direction == "U" else "R"
                    break
                if case("L"):
                    m.Direction = "L" if m.Direction == "D" else "R"
                    break
    for case in switch(lastDirection):
        if case("D"):
            newDirection = "B"
            break
        if case("U"):
            newDirection = "F"
            break
        if case("R"):
            newDirection = "L"
            break
        if case("L"):
            newDirection = "R"
    
    moveQue.append({
        "OrderNr" : moveQue.__len__ + 1,
        "Direction" : newDirection,
        "Afstand" : 1  
    })


