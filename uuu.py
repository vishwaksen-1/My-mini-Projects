#code to build a CLI tic-tac-toe game using oops
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)] # we will use a single list to rep 3x3 board
        self.current_winner = None # keep track of winner!

    def print_board(self):
        # this is just getting the rows
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc (tells us what number corresponds to what box)
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        # if valid move, then make the move (assign square to letter)
        # then return true. if invalid, return false
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # winner if 3 in a row anywhere. We have to check all of these!
        # first let's check the row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        # check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        # check diagonals
        # but only if the square is an even number (0, 2, 4, 6, 8)
        # these are the only moves possible to win a diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # left to right diagonal
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        # if all of these checks fail
        return False

#defining human player
class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-9): ')
            # we're going to check that this is a correct value by trying to cast
            # it to an integer, and if it's not, then we say it's invalid
            # if that spot is not available on the board, we also say it's invalid
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True # if these are successful, then yay!
            except ValueError:
                print('Invalid square. Try again.')
        return val

#defining random computer player
class RandomComputer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square
    
def play(game, x_player, o_player, print_game=True):
    # returns the winner of the game(the letter)! or None for a tie
    if print_game:
        game.print_board_nums()

    letter = 'X' # starting letter
    # iterate while the game still has empty squares
    # (we don't have to worry about winner because we'll just return that
    # which breaks the loop)
    while game.empty_squares():
        # get the move from the appropriate player
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        # let's define a function to make a move!
        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('') # just empty line

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            # after we made our move, we need to alternate letters
            letter = 'O' if letter == 'X' else 'X'  # switches player

        # tiny break to make things a little easier to read
        if print_game:
            print('')

    if print_game:
        print('It\'s a tie!')
    
#let's also create a bot that uses strategies rather than playing random
class SmartComputer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) # randomly choose one
        else:
            # get the square based off the minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter # yourself!
        other_player = 'O' if player == 'X' else 'X' # the other player...

        # first, we want to check if the previous move is a winner
        # this is our base case
        if state.current_winner == other_player:
            # we should return position AND score because we need to keep track of the score
            # for minimax to work
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                            state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            # no empty squares
            return {'position': None, 'score': 0}

        # initialize some dictionaries
        if player == max_player:
            best = {'position': None, 'score': -float('inf')}  # each score should maximize
        else:
            best = {'position': None, 'score': float('inf')}  # each score should minimize

        for possible_move in state.available_moves():
            # step 1: make a move, try that spot
            state.make_move(possible_move, player)
            # step 2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player)  # now, we alternate players
            # step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            # step 4: update the dictionaries if necessary
            if player == max_player:  # we are trying to maximize the max_player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
            
        return best
    #is it done? let's test it

#let's also make a semi-smart computer player that switches from random computer to minimax in between the moves randomly
#instead of writing the whole code, we write it to randomly switch between the two using inheritance
#start with a daughter class that has both random and smart computers as parents

#now lets make the game to have the intelligence of the semi-smart computer player variable i.e., set at the beginning of the game as a floating point number between (0 and 1) that sets the random number's threshold.

class SemiSmartComputer(RandomComputer, SmartComputer):
    #now the random number and switching
    def __init__(self, letter, lvl=0.5):
        self.letter = letter
        self.random = RandomComputer(letter)
        self.smart = SmartComputer(letter)
    # generate a random number before every move and if it is greater than lvl, use random computer, else use smart computer
    def get_move(self, game):
        if random.random() > lvl:
            square = self.random.get_move(game)
        else:
            square = self.smart.get_move(game)
        return square
    #is it done? let's test it
    
if __name__ == '__main__':
    lvl = float(input('Enter the intelligence level of the computer (1-10): '))
    lvl = (lvl-1)/10
    x_player = HumanPlayer('X')
    o_player = SemiSmartComputer('O', lvl=lvl)
    
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)
    
    