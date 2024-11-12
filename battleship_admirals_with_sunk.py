import math
import random
from IPython.display import clear_output
import time

def validate_size(size: int):
    side_length = int(math.sqrt(size))
    if side_length * side_length != size:
        raise ValueError("Size must create perfect square")

def print_game(grids, shots, hits):
    print("                Battleship Admirals")
    print()
    print("        Player 1                  Player 2")
    print_dual_grids(grids[0], grids[1])
    print(f'   Shots: {shots[0]}   Hits: {hits[0]}        Shots: {shots[1]}   Hits: {hits[1]}')
    print()
    print_dual_grids(grids[2], grids[3])
    
    print()
    
def print_grid(grid: list):
    row_labels = 'A B C D E F G H I J K L M N'.split()
    print ('   ' + ' '.join([f'{i}' for i in range(len(grid))]))
    
    for i, row in enumerate(grid):
        print(f'{row_labels[i]:2}', end=' ')
        for cell in row:
            print(cell, end=' ')
        print()

def print_dual_grids(grid1: list, grid2: list):
    row_labels = 'A B C D E F G H I J K L M N'.split()
    print ('   ' + ' '.join([f'{i}' for i in range(len(grid1))]) + '       ' + ' '.join([f'{i}' for i in range(len(grid2))]))
    
    for i in range(len(grid1)):
        print(f'{row_labels[i]:2}', end=' ')
        for cell in grid1[i]:
            print(cell, end=' ')

        print('   ', end= '')
        
        print(f'{row_labels[i]:2}', end=' ')
        for cell in grid2[i]:
            print(cell, end=' ')
            
        print()

def bitstring_to_grid(bitstring: str):
    size = len(bitstring)
    validate_size(size)
    side_length = int(math.sqrt(size))
    
    grid = [
        ['.' if bitstring[i * side_length + j] == '1' else 'O' for j in range(side_length)]
        for i in range(side_length)
    ]
    return grid

def grid_to_bitstring(grid: list):
    bitstring = ''.join('1' if cell == '.' else '0' for row in grid for cell in row)
    return bitstring

def bitstring_to_int(bitstring: str):
    return int(bitstring,2)

def int_to_bitstring(value: int, length=100):
    bitstring = f'{value:0{length}b}'
    return bitstring

def blank_bitstring(size=100):
    validate_size(size)
    
    return '1' * size

def random_bit():
    return random.choice([0,1])

def random_int(max: int):
    return random.randint(0,max)

def random_location(ship_size: int, grid_size: int):
    return random_int(grid_size-ship_size)

#edited to add sunk ships
def random_ship_placement(ship_size: int, grid: list, ships_dict: dict):
    clear = 0
    ship_list = [] #list of list pairs
    while clear == 0:
        orientation = random_bit()
        row = random_location(ship_size, len(grid))
        column = random_location(ship_size, len(grid[0]))
    
        if orientation == 0:
            for i in range(ship_size):
                if grid[row+i][column] == '.':
                    clear = 1
                else:
                    clear = 0
                    break
                
            if clear == 1:
                for i in range(ship_size):
                    grid[row+i][column] = ship_size
                    ship_list.append([(row+i,column),1])
            else:
                continue
        else:
            for i in range(ship_size):
                if grid[row][column+i] == '.':
                    clear = 1
                else:
                    clear = 0
                    break
            if clear == 1:
                for i in range(ship_size):
                    grid[row][column+i] = ship_size
                    ship_list.append([(row,column+i),1])
            else:
                continue 

    ships_dict.append([ship_list, 1])
    return grid, ships_dict

def setup_game(grid_size: int, ships: list):
    bit_string = blank_bitstring(grid_size*grid_size)
    ship_grid1 = bitstring_to_grid(bit_string)
    ship_grid2 = bitstring_to_grid(bit_string)
    shot_grid1 = bitstring_to_grid(bit_string)
    shot_grid2 = bitstring_to_grid(bit_string)
    ships_dict1, ships_dict2 = [], []
    
    for i in range(len(ships)):
        ship_grid1, ships_dict1 = random_ship_placement(ships[i], ship_grid1, ships_dict1)

    for i in range(len(ships)):
        ship_grid2, ships_dict2 = random_ship_placement(ships[i], ship_grid2, ships_dict2)
        
    return shot_grid1, shot_grid2, ship_grid1, ship_grid2, ships_dict1, ships_dict2

def play_turn(grids, turn):
    clear = 0
    while clear ==0:
        row = random_int(len(grids[turn])-1)
        column = random_int(len(grids[turn][0])-1)
        #print("trying: ", turn , row, column)
        if grids[turn][row][column] == '.':
            clear = 1
    return row, column

def play(grid_size, ships):
    grid1, grid2, grid3, grid4, dict1, dict2= setup_game(grid_size, ships)
    grids = [grid1,grid2,grid3,grid4]
    sunk = [dict1,dict2]
    hits_to_win = sum(ships)
    max_shots = grid_size*grid_size
    shots = [0, 0]
    hits = [0, 0]
    turn = 0
    while shots[0] < max_shots and shots[1] < max_shots and hits[0] < hits_to_win and hits[1] < hits_to_win:
        clear_output(wait=True)
        current_shot = play_turn(grids, turn)
        if grids[turn+2][current_shot[0]][current_shot[1]] == '.':
            grids[turn][current_shot[0]][current_shot[1]] = 'O'
        else:
            grids[turn][current_shot[0]][current_shot[1]] = 'X'
            hits[turn] = hits[turn] + 1
            for i in sunk[turn]: #list of player boats
                index1 = sunk[turn].index(i) #the particular boat
                for j in i[0]: #list of just the tiles
                    index2 = i[0].index(j) #the particular tile
                    if j[0] == (current_shot[0],current_shot[1]):
                        sunk[turn][index1][0][index2][1] = 0
                        is_sunk=0
                        for k in sunk[turn][index1][0]:
                            is_sunk+=k[1]
                        if is_sunk == 0:
                            sunk[turn][index1][1] = 0
                if i[1] == 0:
                    for l in i[0]:
                        grids[turn][l[0][0]][l[0][1]] = '*'  
        shots[turn] = shots[turn] + 1
        if turn == 0:
            turn = 1
        else:
            turn = 0
        time.sleep(1)
grid_size = 10
ships = [5, 4, 3, 3, 2]

play(grid_size, ships)
