import queue
import requests

lijst = []

def printMaze(maze, path=""):
    for x, pos in enumerate(maze[0]):
        if pos == "O":
            start = x

    i = start
    j = 0
    pos = set()
    for move in path:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1
        pos.add((j, i))
    
    for j, row in enumerate(maze):
        for i, col in enumerate(row):
            if (j, i) in pos:
                print("+ ", end="")
            else:
                print(col + " ", end="")
        print()
        
def valid(maze, moves):
    for x, pos in enumerate(maze[0]):
        if pos == "O":
            start = x

    i = start
    j = 0
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

        if not(0 <= i < len(maze[0]) and 0 <= j < len(maze)):
            return False
        elif (maze[j][i] == "#"):
            return False

    return True

def findEnd(maze, moves):
    global lijst

    for x, pos in enumerate(maze[0]):
        if pos == "O":
            start = x

    i = start
    j = 0
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

    if maze[j][i] == "X":
        print("Found: " + moves)

        for num, move in enumerate(moves, start=1):
          #print(move)
          lijst.append({"OrderNr": num,"Direction": move,"Afstand" : 5})

        print(lijst)  
        requests.post("http://127.0.0.1:3000/sendmoves" , json= {"moves": lijst})

        printMaze(maze, moves)
        return True

    return False

def readmap(map):
    f = open(map + ".txt", "r")
    content = f.read()
    split = content.splitlines()

    data = []

    for el in split:
        temp = []
        for ch in el:
            if ch == "E":
                temp.append(" ")
            elif ch == "#":
                temp.append("#")
            elif ch == "X":
                temp.append("X")
            elif ch == "O":
                temp.append("O")

        data.append(temp)


    for el in data:
        print(el)

    f.close()

    return data

def printLinebreak():
    print()
    print("-------------------------------------")
    print()

def solve(maze):       
    nums = queue.Queue()
    nums.put("")
    add = ""

    data = []

    while not findEnd(maze, add): 
        add = nums.get()

        for j in ["L", "R", "U", "D"]:
            put = add + j
            if valid(maze, put):
                nums.put(put)


stop = True

mappen = ["1", "2", "3", "4", "5"]

while stop:
    print("Choose a map: ")
    print("1. Map 1")
    print("2. Map 2")
    print("3. Map 3")
    print("4. Map 4")
    print("5. Map 5")

    ans = input()

    map = [] 
    
    printLinebreak()

    if ans in mappen:
        map = readmap("map" + ans)

        printLinebreak()

        print("Solve map? y/n")
        x = input()
        printLinebreak()

        if x == "y":
            solve(map)
            
            printLinebreak()


    else:
        stop = False





        