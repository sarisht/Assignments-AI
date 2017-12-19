# Reference: http://math.ku.sk/~trenkler/05-MagicCube.pdf for general mathematical algorithm for magic cube

# Importing Required Libraries

import pandas as pd
import numpy as np
import copy
import operator

# Algorithm with user input size
size = int(input("Size of the cube (nxnxn) (integer value of n): "))

# initializing a 3d array with 0 as all elements
magic_cube = [[[0 for i in range(size)] for j in range(size)] for k in range(size)]

# fills the magic cube. It is called only when the given input of size is odd
def fill_magic_cube_odd(n):
    # Helper function required in the Algorithm
    def a(i,j,k,n) : return (i -j +k)%n
    def b(i,j,k,n) : return (i -j -k-1)%n
    def c(i,j,k,n) : return (i +j +k +1)%n
    if n%2 == 1:
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    magic_cube[i][j][k] = a(i,j,k,n) *n*n + b(i,j,k,n)*n+c(i,j,k,n)+1 
        return magic_cube

# Proof why this works for n = 3:
# magic_cube[i][j][k]= ((i-j+k)%3)*3*3 + ((i-j-k-1)%3)*3 + ((i+j+k+1)%3) + 1
# rows,columns => since the remainder of any consecutive values of linear combination of i, j, k with 1 as their multiplier
#                has to take values 0,1,2, the sum of them will be (0+1+2)*3*3 + (0+1+2)*3+(0+1+2)*1 +1 +1 +1 = 27+9+3+1+1+1 = 42
# body diagonals => starts from (0,0,0) -> increase in all i,j,k by 1 =>in i-j+k and i-j-k value change by 1 and i+j+k no change modulo 3 
#                                             thus (0+1+2)*3*3+(0,1,2)*3+(1+1+1)+1+1+1 = 42
#                            or (0,0,2) -> increase in i,j by 1, decrease in k by 1 => change in i-j-k, i-j+k and i+j+k by 1 modulo 3 
#                                             thus (0+1+2)*9+(0,1,2)*3+(0+1+2)+1+1+1 = 42

#Function to generate magic cube for even numbers(of type 4n)
def fill_magic_cube_4n(n) :
     if n%4 == 0:
        def bar(x): 
            return n-x
        def tilda(x):
            if x < n/2 : return 0
            else: return 1
        def F(i,j,k):
            return (i+j+k+tilda(i)+tilda(j)+tilda(k)+1)%2
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if F(i,j,k)== 0:
                        magic_cube[j][i][k] = ((bar(i) - 1)*n*n + (bar(j) - 1)*n + bar(k))
                    else:
                        magic_cube[j][i][k] = (i*n*n + j*n +k+1)
        return magic_cube

#Function to generate magic cube for even numbers(of type 4n+2)
def fill_magic_cube_4nplus2(n): 
    d_table = pd.DataFrame(columns = (np.arange(8)+1))
    d_table.loc[1] = [7,3,6,2,5,1,4,0]
    d_table.loc[2] = [3,7,2,6,1,5,0,4]
    d_table.loc[3] = [0,1,3,2,5,4,6,7]
    for u in range(4,int(size/2)+1):
        if u%2 == 0:
            d_table.loc[u] = [0,1,2,3,4,5,6,7]
        else:
            d_table.loc[u] = [7,6,5,4,3,2,1,0]
    if n%4 == 2:
        def bar(x): 
            return n-x
        def star(x):
            return min(x+1,bar(x))
        def tilda(x):
            if x < n/2 : return 0
            else: return 1
        t = int(n/2)
        temp = copy.deepcopy(fill_magic_cube_odd(t))
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    magic_cube[i][j][k] = d_table.loc[(star(i)-star(j)+star(k))%t + 1, 4*tilda(i)+2*tilda(j)+tilda(k)+1]*t*t*t + temp[star(i)-1][star(j)-1][star(k)-1]
        return magic_cube

#function to generate magic cube
def fill_magic_cube(n):
    if n%1 !=0 :
        return 'Please give an integral value'
    if n <= 0:
        return 'Please give a valid positive number'
    if n ==2:
        return 'No Such Cube Exists'
    if n%2 == 1:
        return fill_magic_cube_odd(n)
    elif n%4 == 0:
        return fill_magic_cube_4n(n)
    else:
        return fill_magic_cube_4nplus2(n)

#function to print magic cube
def print_cube(size, bool_val):
    if pd.isnull(size) == 1: size = size
    if pd.isnull(bool_val) == 1: bool_val = True
    stir = ''
    for i in range(size):
        a=0
        for j in range(size):

            print(stir+('   ')*(size-a), end='')
            if bool_val:
                for k in range(size):
                    if(magic_cube[i][j][k] in compu):
                        print('O   ',end='')
                    elif(magic_cube[i][j][k] in human):
                        print('X   ',end= '')
                    else:
                        print('_   ', end='')
                print('             ',end='')
            for k in range(size):
                print(str(magic_cube[i][j][k])+'   ', end='')
            a+=1
            print()
        print()
  

magic_cube = fill_magic_cube(size)
print_cube(size, False)

#Program to make matrix of all the faces
cube = [[[0 for i in range(size+1)] for j in range(size+1)] for k in range(3*size+6)]
l=0
list=[]
for i in range(size):
    for j in range(size):
        for k in range(size):
            cube[l][j][k]=magic_cube[i][j][k]
            cube[l][j][size]+=cube[l][j][k]
            cube[l][size][k]+=cube[l][j][k]
            
    for j in range(size):
        cube[l][size][size]+=cube[l][j][j]
    l=l+1
    
for j in range(size):
    for i in range(size):
        for k in range(size):
            cube[l][k][i]=magic_cube[i][j][k]
            cube[l][k][size]+=cube[l][k][i]
            cube[l][size][i]+=cube[l][k][i]
    for j in range(size):
        cube[l][size][size]+=cube[l][j][j]
    l=l+1
    
for k in range(size):
    for j in range(size):
        for i in range(size):
            cube[l][i][j]=magic_cube[i][j][k]
            cube[l][i][size]+=cube[l][i][j]
            cube[l][size][j]+=cube[l][i][j]
    for j in range(size):
        cube[l][size][size]+=cube[l][j][j]
    l=l+1
    
for i in range(size):
    for j in range(size):
        cube[l][i][j]=magic_cube[i][i][j]
        cube[l][i][size]+=cube[l][i][j]
        cube[l][size][j]+=cube[l][i][j]
        cube[l+1][i][j]= magic_cube[i][size-1-i][j]
        cube[l+1][i][size]+=cube[l+1][i][j]
        cube[l+1][size][j]+=cube[l+1][i][j]
for j in range(size):
    cube[l][size][size]+=cube[l][j][j]
l=l+1
for j in range(size):
    cube[l][size][size]+=cube[l][j][j]
l=l+1

for i in range(size):
    for j in range(size):
        cube[l][i][j]=magic_cube[i][j][i]
        cube[l][i][size]+=cube[l][i][j]
        cube[l][size][j]+=cube[l][i][j]
        cube[l+1][i][j]= magic_cube[i][j][size-1-i]
        cube[l+1][i][size]+=cube[l+1][i][j]
        cube[l+1][size][j]+=cube[l+1][i][j]
for j in range(size):
    cube[l][size][size]+=cube[l][j][j]
l=l+1
for j in range(size):
    cube[l][size][size]+=cube[l][j][j]
l=l+1

for i in range(size):
    for j in range(size):
        cube[l][i][j]=magic_cube[j][i][i]
        cube[l][i][size]+=cube[l][i][j]
        cube[l][size][j]+=cube[l][i][j]
        cube[l+1][i][j]= magic_cube[j][i][size-1-i]
        cube[l+1][i][size]+=cube[l+1][i][j]
        cube[l+1][size][j]+=cube[l+1][i][j]
for j in range(size):
    cube[l][size][size]+=cube[l][j][j]
l=l+1
for j in range(size):
    cube[l][size][size]+=cube[l][j][j]
l=l+1

#Program to print all faces
for i in range(3*size+6):
    for j in range(size+1):
        print (cube[i][j])
    print ('\n')

if size == 3: 
    bool1=input("Want to input magic cube manually??(y/n): ")
else: bool1 ='y'

if(bool1=='y'):
    a=1
    for i in range(3):
        for j in range(3):
            for k in range(3):
                magic_cube[i][j][k]= int(input(str(a)+': '))
                a+=1

# Program to generate exceptions
lst=[]
for i in range(15):
    for j in range(3):
        lst.append([cube[i][j][0],cube[i][j][1],cube[i][j][2]])
        lst.append([cube[i][0][j],cube[i][1][j],cube[i][2][j]])
    lst.append([cube[i][0][0],cube[i][1][1],cube[i][2][2]])
    lst.append([cube[i][0][2],cube[i][1][1],cube[i][2][0]])

for i in range(len(lst)):
    lst[i].sort()
lst.sort()

s=[]
for i in lst:
    if i not in s:
        s.append(i)

lst2=[]
for i in range(1,28):
    for j in range(1,28):
        a=42-i-j
        if((a>0)and(a<=27)and(a!=i)and(a!=j)and(i!=j)):
            lst2.append([i,j,a])
for i in range(len(lst2)):
    lst2[i].sort()
lst2.sort()
s2=[]
for i in lst2:
    if i not in s2:
        s2.append(i)
s3=[]
for i in s2:
    if i not in s:
        s3.append(i)


s4=[]
for i in s:
    if i not in s2:
        s4.append(i)


#3D Tic-Tac-Toe

bool=input("Want to move first??(y/n): ")

#Function that find triplet from exceptions given 2 numbers of the triplet as input
def find(a,b,lst):
    for item in lst:
        if a in item and b in item:
            for items in item:
                if items!= a and items!= b:
                    return items


#function to print faces 
def print_faces():
    i=0
    while(i<15):
        for j in range(3):
            for a in range(5):
                for k in range(3):
                    if(cube[i+a][j][k] in compu):
                        print('O   ',end='')
                    elif(cube[i+a][j][k] in human):
                        print('X   ',end= '')
                    else:
                        print(str(cube[i+a][j][k])+'   ', end='')
                print('      ',end='')

            print()
        i=i+5  
        print ()


#function that tells move possibilities for the bot
def move_possibilities():
    possibilities = {}
    for mymoves in range(1,28):
        possibilities[mymoves] = 0
        if mymoves not in occupied_places:
            predicted_occupied_places = (copy.copy(occupied_places))
            predicted_occupied_places.append(mymoves)
            predicted_compu = (copy.copy(compu))
            predicted_compu.append(mymoves)
            move1 = mymoves
            for moves in predicted_compu:
                if move1!=moves:
                    k = [move1, moves, 42-move1-moves]
                    k.sort()
                    if (k not in s3) and ((42-move1-moves) not in predicted_occupied_places):
                        # if compu is getting a line(sum 42, not in exception list, not occupied)
                        if 42-move1-moves > 0 and 42-move1-moves <28:
                            possibilities[mymoves]+=1
                    elif (pd.isnull(find(move1,moves,s4)) == 0):
                        if (find(move1,moves,s4) not in occupied_places):# exceptional case (getting a line)
                            if find(move1,moves,s4) > 0 and find(move1,moves,s4) < 28:
                                possibilities[mymoves]+=1
    return possibilities


#function to calculate score
def score(comp):
    score = 0
    m = len(comp)
    for i in range(m):
        for j in range(i+1,m):
            for k in range(j+1,m):
                lst = [comp[i],comp[j],comp[k]]
                lst.sort()
                if comp[i]+comp[j]+comp[k] == 42:
                    if lst not in s3:
                        score+=1
                elif lst in s4:
                    score+=1
    return score


#function 
def score_possibilities(comp):
    possibilities = {}
    x = score(comp)
    for mymoves in range(1,28):
        possibilities[mymoves] = 0
        if mymoves not in occupied_places:
            temp = copy.copy(comp)
            temp.append(mymoves)
            y = score(temp)
            possibilities[mymoves] = y-x
    return possibilities

# Program computes the next move for a given move and this is looped till total 20 moves
human = []
compu = []
move_number = 0
occupied_places = []
moved = False

print('Type display to show all faces, exit to quit')

if (bool == "n"):# if computer moves first it will take the center position
    compu.append(magic_cube[1][1][1])
    occupied_places.append(magic_cube[1][1][1])
    print('Computer: '+ str(magic_cube[1][1][1]))
    move_number+=1
        
while True:
    print_cube(3,True)
    if move_number >=20:
        break
    move = (input('Human: '))# inputs the move the player wants to play
    try:
        move = int(move)
        if move > 27 or move<1:
            print('Number should be between 0-27')
            continue
    except:
        if move == 'display': 
            print_faces()
            continue
        elif move == 'exit': break
        else: 
            'Please refer to the positions in the cube'
            continue
        break
    moved = False
    if move in occupied_places:
        print('Position already occupied')
        continue
    occupied_places.append(move)
    move_number+=1
    human.append(move)
    if move_number in [1,2]: # First move or second move: take center or else a corner
        if magic_cube[1][1][1] in occupied_places:
            if magic_cube[0][0][0] in occupied_places:
                compu.append(magic_cube[2][0][0])
                occupied_places.append(magic_cube[2][0][0])
                print('Computer: '+ str(magic_cube[2][0][0]))
                move_number+=1
                continue
            else:
                compu.append(magic_cube[0][0][0])
                occupied_places.append(magic_cube[0][0][0])
                print('Computer: '+ str(magic_cube[0][0][0]))
                print()
                move_number+=1
                continue
        else:
            compu.append(magic_cube[1][1][1])
            occupied_places.append(magic_cube[1][1][1])
            print('Computer: '+ str(magic_cube[1][1][1]))
            print()
            move_number+=1
            continue
    scoring_possibilities_human = max(score_possibilities(human).items(), key=lambda k: k[1])
    # max scoring (value,score increase) move for human
    scoring_possibilities_compu = max(score_possibilities(compu).items(), key=lambda k: k[1])
    # max scoring (value,score increase) move for computer
    if scoring_possibilities_compu[1] >= scoring_possibilities_human[1]:
        # if computer can get a higher score then it gladly accepts else it stops the humans best move
        if scoring_possibilities_compu[1] != 0:
            print('Computer: '+ str(scoring_possibilities_compu[0]))
            compu.append(scoring_possibilities_compu[0])
            occupied_places.append(scoring_possibilities_compu[0])
            moved = True
            move_number+=1
        else: # if computer and human both cant score then a double attack is formed
            moved = True
            mymve = max(move_possibilities().items(), key=lambda k: k[1])[0]
            occupied_places.append(mymve)
            compu.append(mymve)
            print('Computer: '+ str(mymve))
            move_number+=1
    else: # stopping human from hetting a higher score
        print('Computer: '+ str(scoring_possibilities_human[0]))
        compu.append(scoring_possibilities_human[0])
        occupied_places.append(scoring_possibilities_human[0])
        moved = True
        move_number+=1


#Program that finally prints the played cube
print('Final 3D Tic Tac Toe looks like: ')
print_cube(3,True)

#Program to print win/loss scenerio
if len(occupied_places)!= 20:
    print('You QUIT!!!')
elif(score(compu)>score(human)):
    print("You LOST!!!!!!!!!!!\nBetter luck next time")
elif(score(compu)<score(human)):
    print("Congratulations, You WON!!!!!!!\nWell Played")
else:
    print("Its a DRAW!!!!!")
print('Your Score: '+ str(score(human)))
print('Computer: '+str(score(compu)))
