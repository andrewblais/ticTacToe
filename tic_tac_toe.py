from random import choice


class TicTacToe:
    """A class for a text-based Tic-Tac-Toe game playable in the command line.

        :ivar amt_players: Determines one or two players. :type: int
        :ivar player_1: Player 1's symbol 'X'. :type: str
        :ivar player_2: Player 2's symbol 'O'. :type: str
        :ivar current_symbol: Active player's symbol. :type: str
        :ivar current_board: Current game board. :type: dict
        :ivar routes: List of strings for current rows, columns and diagonals. :type: list
        :ivar current_player: Active player. :type: int
        :ivar player_1_win: Player 1's total wins. :type: int
        :ivar player_2_win: Player 2's total wins. :type: int
        :ivar turn_count: Number of turns played, maxes out at 9. :type: int
    """

    def __init__(self):
        """The constructor for TicTacToe class."""
        self.amt_players = 2
        self.player_1 = "X"
        self.player_2 = "O"
        self.current_symbol = ""
        self.current_board = self.reset()
        self.routes = list()
        self.current_player = 1
        self.player_1_win = 0
        self.player_2_win = 0
        self.turn_count = 0

    @staticmethod
    def check_quit(user_input: str):
        """Checks input for exit request."""
        if user_input and user_input[0].lower() in ["q", "e"]:
            exit()

    @staticmethod
    def trim_space(vals: list) -> str:
        """Trim spaces from list of winning route values.

        :param vals: List of strings representing a row, column or diagonal. :type: list
        :return trimmed_route: The given row, column or diagonal without spaces. :type: str
        """
        trimmed_route = "".join(vals).replace(" ", "")
        return trimmed_route

    def reset(self):
        """Resets the game board dictionary.

        :return brd_reset: Fresh version of the game board. :type: dict
        """
        brd_reset = {f"row{i}_col{j}": "  -  " for i in range(1, 4) for j in range(1, 4)}
        self.turn_count = 1
        return brd_reset

    def switch_player(self):
        """Logic to alternate players."""
        if self.current_player == 1:
            self.current_player = 2
            self.turn_count += 1
        else:
            self.turn_count += 1
            self.current_player = 1

    def align_symbol(self):
        """Switches user upon turn end."""
        if self.current_player == 1:
            self.current_symbol = self.player_1
        elif self.current_player == 2:
            self.current_symbol = self.player_2

    @staticmethod
    def intro_banner():
        """Defines the initial text the user sees."""
        print("TIC\n     TAC\n          TOE\n")

    def run(self):
        """Introduces the game and prompts the user to play. Offers user option to exit program."""
        self.intro_banner()
        play = input("Continue? (y/n) ")
        if not play or play.lower()[0] not in ["e", "q", "y", "n"]:
            self.run()
        if play.lower()[0] in ["n"]:
            exit()
        amt_players = input("1 or 2 players? (1/2) ")
        self.check_quit(amt_players)
        while not amt_players or amt_players not in ["1", "2"]:
            amt_players = input("1 or 2 players? (1/2) ")
        self.amt_players = int(amt_players)
        self.check_quit(play)
        if play.lower()[0] == "y":
            self.current_board = self.reset()
            self.play_game()
        else:
            exit()

    def display_board(self):
        """Displays the current game board in a readable format."""
        vals = list(self.current_board.values())
        s = "      "
        print(f"\n{s}{''.join(vals[:3])}\n\n{s}{''.join(vals[3:6])}\n\n{s}{''.join(vals[6:])}\n")

    def user_choice(self, row_column_str: str):
        """Function to create variable when asking user input for row or column."""
        row_or_column = input(f"{row_column_str}: (1, 2, 3) ")
        # Handle user input for row or column:
        self.check_quit(row_or_column)
        while not row_or_column or row_or_column not in ["1", "2", "3"]:
            row_or_column = input(f"{row_column_str}: (1, 2, 3) ")
            self.check_quit(row_or_column)
        if row_column_str == "Column":
            print()
        return row_or_column

    @staticmethod
    def generate_choice():
        row_or_column = choice(["1", "2", "3"])
        return row_or_column

    def play_game(self):
        """Logic to play game. Alternates between users with appropriate symbols."""
        # Conditional checks if game board is full:
        if self.turn_count <= 9:
            self.display_board()
            self.align_symbol()
            if self.amt_players == 1 and self.current_symbol == "O":
                row = self.generate_choice()
                col = self.generate_choice()
            else:
                # Get user input for row:
                print(f"\nPlayer {self.current_player}, play your {self.current_symbol}:")
                row = self.user_choice("Row")
                col = self.user_choice("Column")
            play = f"row{row}_col{col}"
            current = self.current_board[play]
            if "-" in current:
                if self.amt_players == 1 and self.current_symbol == "O":
                    print(f"Computer chose row: {row}, col: {col}.")
                else:
                    print(f"You chose row: {row}, col: {col}.")
                current = current.replace("-", self.current_symbol)
                self.current_board[play] = current
                self.win_logic()
                self.play_game()
            else:
                print("That space is already taken. Try again.\n")
                self.play_game()
        # Else logic if game board is full:
        else:
            self.display_board()
            print("NO WINNER THIS ROUND.\n")
            print("OVERALL SCORE:")
            print(f"Player 1: {self.player_1_win}")
            print(f"Player 2: {self.player_2_win}\n")
            self.run()

    def game_status(self):
        """Credits appropriate player with victory in running match score."""
        for i in self.routes:
            if i == "XXX":
                self.display_board()
                self.player_1_win += 1
                print("X WINS THIS ROUND!\n")
                print("OVERALL SCORE:")
                print(f"Player 1: {self.player_1_win}")
                print(f"Player 2: {self.player_2_win}\n")
                self.run()
            elif i == "OOO":
                self.display_board()
                self.player_2_win += 1
                print("O WINS THIS ROUND!\n")
                print("OVERALL SCORE:")
                print(f"Player 1: {self.player_1_win}")
                print(f"Player 2: {self.player_2_win}\n")
                self.run()

    def win_logic(self):
        """Checks for game winner. Tabulates overall match score."""
        vals = list(self.current_board.values())
        row_1 = self.trim_space(vals[:3])
        row_2 = self.trim_space(vals[3:6])
        row_3 = self.trim_space(vals[6:])
        col_1 = self.trim_space(vals[0::3])
        col_2 = self.trim_space(vals[1::3])
        col_3 = self.trim_space(vals[2::3])
        diag_1 = self.trim_space(vals[0::4])
        diag_2 = self.trim_space(vals[2:7:2])
        self.routes = [row_1, row_2, row_3, col_1, col_2, col_3, diag_1, diag_2]
        self.game_status()
        self.switch_player()


# # # Give it a whirl!
ttt = TicTacToe()
ttt.run()

# # Access the Class docstring using help()
# help(TicTacToe)

# # Access the run method docstring using help()
# help(TicTacToe.run)
