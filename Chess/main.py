import random

class ChessGame:
    def __init__(self):
        self.pieces = {
            'white': {
                'Pawn': '\u2659',
                'Rook': '\u2656',
                'Knight': '\u2658',
                'Bishop': '\u2657',
                'Queen': '\u2655',
                'King': '\u2654'
            },
            'black': {
                'Pawn': '\u265F',
                'Rook': '\u265C',
                'Knight': '\u265E',
                'Bishop': '\u265D',
                'Queen': '\u265B',
                'King': '\u265A'
            }
        }
        self.board = self.initialize_board()

    @staticmethod
    def initialize_board():
        # Unicode characters for the chess pieces
        pieces = {
            'white': {
                'Pawn': '\u2659',
                'Rook': '\u2656',
                'Knight': '\u2658',
                'Bishop': '\u2657',
                'Queen': '\u2655',
                'King': '\u2654'
            },
            'black': {
                'Pawn': '\u265F',
                'Rook': '\u265C',
                'Knight': '\u265E',
                'Bishop': '\u265D',
                'Queen': '\u265B',
                'King': '\u265A'
            }
        }

        # Initialize an 8x8 chess board
        board = [[' ' for _ in range(8)] for _ in range(8)]

        # Place the pieces on the board
        for i in range(8):
            board[1][i] = pieces['black']['Pawn']
            board[6][i] = pieces['white']['Pawn']

        # Rooks
        board[0][0] = board[0][7] = pieces['black']['Rook']
        board[7][0] = board[7][7] = pieces['white']['Rook']

        # Knights
        board[0][1] = board[0][6] = pieces['black']['Knight']
        board[7][1] = board[7][6] = pieces['white']['Knight']

        # Bishops
        board[0][2] = board[0][5] = pieces['black']['Bishop']
        board[7][2] = board[7][5] = pieces['white']['Bishop']

        # Queens
        board[0][3] = pieces['black']['Queen']
        board[7][3] = pieces['white']['Queen']

        # Kings
        board[0][4] = pieces['black']['King']
        board[7][4] = pieces['white']['King']

        return board

    def get_piece_color(self, piece):
        if piece in self.pieces['white'].values():
            return 'white'
        elif piece in self.pieces['black'].values():
            return 'black'
        else:
            return None
    
    def print_board(self):
        print('    a   b   c   d   e   f   g   h  ')
        print('  +---+---+---+---+---+---+---+---+')
        for i, row in enumerate(self.board):
            print(f'{8-i} | ' + ' | '.join(row) + ' |')
            print('  +---+---+---+---+---+---+---+---+')

    def play_game(self):
        num_players = input("Enter the number of players (1 or 2): ")
        while num_players not in ['1', '2']:
            num_players = input("Invalid input. Please enter the number of players (1 or 2): ")

        if num_players == '1':
            players = [('Player', 'white'), ('Computer', 'black')]
        else:
            players = [('Player 1', 'white'), ('Player 2', 'black')]

        while True:
            for player, color in players:
                self.print_board()
                if player == 'Computer':
                    piece_position, new_position = self.computer_move()
                else:
                    piece_position = input(f"{player}, enter the position of the piece to move (e.g., 'e2'): ")
                    new_position = input(f"{player}, enter the new position for the piece (e.g., 'e4'): ")
                self.move_piece(piece_position, new_position, color)

    def move_piece(self, piece_position, new_position, color):
        # Convert chess notation to board indices
        piece_x, piece_y = ord(piece_position[0]) - ord('a'), 8 - int(piece_position[1])
        new_x, new_y = ord(new_position[0]) - ord('a'), 8 - int(new_position[1])

        # Check if the move is allowed
        piece = self.board[piece_y][piece_x]
        target = self.board[new_y][new_x]
        if self.get_piece_color(piece) != color:
            print("Invalid move: the piece to move is not of your color.")
            return
        if self.get_piece_color(piece) == self.get_piece_color(target):
            print("Invalid move: cannot move to a position occupied by a piece of the same color.")
            return

        # Move the piece
        self.board[new_y][new_x] = self.board[piece_y][piece_x]
        self.board[piece_y][piece_x] = ' '

    def computer_move(self):
        # This is a very basic AI that chooses a random move.
        # You could replace this with a more sophisticated AI if you want.
        while True:
            piece_x = random.randint(0, 7)
            piece_y = random.randint(0, 7)
            new_x = random.randint(0, 7)
            new_y = random.randint(0, 7)
            if self.board[piece_y][piece_x] != ' ' and self.board[new_y][new_x] == ' ':
                piece_position = chr(piece_x + ord('a')) + str(8 - piece_y)
                new_position = chr(new_x + ord('a')) + str(8 - new_y)
                return piece_position, new_position


game = ChessGame()
game.print_board()
game.play_game()

