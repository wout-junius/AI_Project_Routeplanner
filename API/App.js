const express = require("express");
const { send } = require("process");
const bodyParser = require("body-parser");

const app = express();
const router = express.Router();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json())
app.use(
    bodyParser.urlencoded({
      extended: true,
    })
  );

var movesQue = null;

/*
{
    moves: [
        {
            "OrderNr" : int //van 1 - x voor volgorde
            "Direction" : string,
             "Afstand" : int
        }
    ]
}
*/

app.get('/', (req, res) => {
    let html = `
    <script src="https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js"></script>
    <h1> /sendmoves </h1>
    <code class="prettyprint" lang-json>
    { </br>
    &nbsp;     moves: [ </br>
    &nbsp;&nbsp;        { </br>
    &nbsp;&nbsp;&nbsp;      "OrderNr" : int //van 1 - x voor volgorde </br>
    &nbsp;&nbsp;&nbsp;      "Direction" : string, </br>
    &nbsp;&nbsp;&nbsp;      "Afstand" : int </br>
    &nbsp;&nbsp;        } </br>
    &nbsp;    ] </br>
    }
    </code>
    <code class="prettyprint" lang-js>
    <h1> /plsSendNext </h1>
    {</br>
        &nbsp;   "OrderNr" : int //van 1 - x voor volgorde </br>
        &nbsp;  "Direction" : string, </br>
        &nbsp;   "Afstand" : int </br>
    }
    </code>
    `
    res.send(html)
})

app.post('/sendmoves', (req, res) => {
    console.log("POST moves");
    movesQue = []
    for(let move of req.body.moves){
        movesQue.push(move)
    }
     movesQue.sort((a, b) => (a.OrderNr < b.OrderNr) ? a.OrderNr : b.OrderNr);
    res.send({Message: "Success"})
})

app.get('/getmoves', (req, res) => {
    console.log("GET MOVES");
    if(movesQue != null) {RouteToMoves();}
    sendQue = (movesQue == null) ? [{"Empty": true}] : movesQue;
    movesQue = null;
    console.log(sendQue);
    res.send(sendQue);
})



function RouteToMoves(robotDirection){
    lastDirection = ""
    let ConverteMoves = [];
    movesQue.forEach(m => {
        lastDirection = m.Direction;
        if(m.OrderNr != 1){
            console.log(JSON.stringify(movesQue));
            console.log("stap " + m.OrderNr +" " + m.Direction + " " + movesQue[m.OrderNr-2].Direction);
            if(m.Direction == movesQue[m.OrderNr-2].Direction){
                console.log("-F");
                ConverteMoves.push({
                    "OrderNr" : m.OrderNr, //van 1 - x voor volgorde
                    "Direction" :  "F",
                     "Afstand" : 1
                })
            }else{
                switch(movesQue[m.OrderNr-2].Direction){
                    case "D":
                        console.log("D");
                        ConverteMoves.push({
                            "OrderNr" : m.OrderNr, //van 1 - x voor volgorde
                            "Direction" :  (m.Direction == "L") ? "R" : "L",
                             "Afstand" : 1
                        })
                    
                        console.log("-" + ConverteMoves[m.OrderNr - 1].Direction );
                        break;
                    case "U":
                        console.log("U");
                        ConverteMoves.push({
                            "OrderNr" : m.OrderNr, //van 1 - x voor volgorde
                            "Direction" :  (m.Direction == "L") ? "L" : "R",
                             "Afstand" : 1
                        })
                        console.log("-" + ConverteMoves[m.OrderNr - 1].Direction );
                        break;
                    case "R":
                        console.log("F");
                        ConverteMoves.push({
                            "OrderNr" : m.OrderNr, //van 1 - x voor volgorde
                            "Direction" :  (m.Direction == "U") ? "L" : "R",
                             "Afstand" : 1
                        })
                        console.log("-" + ConverteMoves[m.OrderNr - 1].Direction );
                    break;
                    case "L":
                        console.log("L");
                        ConverteMoves.push({
                            "OrderNr" : m.OrderNr, //van 1 - x voor volgorde
                            "Direction" :  (m.Direction == "D") ? "L" : "R",
                             "Afstand" : 1
                        })
                        console.log("-" + ConverteMoves[m.OrderNr - 1].Direction );
                    break;
                }
            }
        }else{
            ConverteMoves.push({
                "OrderNr" : m.OrderNr, //van 1 - x voor volgorde
                "Direction" :  m.Direction,
                 "Afstand" : 1
            })
        }
        console.log("--------------------------------------------------------");
    });
    let newDirection = "";
    switch(lastDirection){
        case "D":
            newDirection = "B"
            break;
        case "U":
            newDirection = "F"
            break;
        case "R":
            newDirection = "L"
        break;
        case "L":
            newDirection = "R"
        break;
    }
    
    ConverteMoves.push({
        "OrderNr" : movesQue.length + 1, //van 1 - x voor volgorde
        "Direction" : newDirection,
         "Afstand" : 1
    })

    movesQue = ConverteMoves
}

app.listen(PORT ,()=> {
    console.log(`Listening on port ${PORT}`);
    console.log();
});