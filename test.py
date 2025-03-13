import random


class Exceptions:
    @staticmethod
    def board_out_exception():
        raise Exception("Выход за границы игрового поля!")

    @staticmethod
    def ship_too_close_exception():
        raise Exception("Ошибка: корабли должны находиться на расстоянии минимум 1 клетка друг от друга!")


class Game:
    class Player:
        def __init__(self, name):
            self.name = name

        def get_coordinates(self):
            while True:
                x = input(f"{self.name}, введите букву (A-F): ").upper()
                y = input(f"{self.name}, введите цифру (1-6): ")
                if x in "ABCDEF" and y.isdigit() and 1 <= int(y) <= 6:
                    return x, y
                else:
                    print("Некорректный ввод. Попробуйте снова.")

        def choose_ship_direction(self):
            while True:
                direction = input("Выберите направление (H - горизонтально, V - вертикально): ").upper()
                if direction in ("H", "V"):
                    return direction
                else:
                    print("Некорректный ввод. Попробуйте снова.")

    class AIPlayer:
        def __init__(self):
            self.name = "ИИ"
            self.shots_taken = set()

        def get_coordinates(self):
            while True:
                x = random.choice(["A", "B", "C", "D", "E", "F"])
                y = str(random.choice([1, 2, 3, 4, 5, 6]))
                if (x, y) not in self.shots_taken:
                    self.shots_taken.add((x, y))
                    return x, y

    def __init__(self):
        self.player_board = [['-' for _ in range(6)] for _ in range(6)]
        self.ai_board = [['-' for _ in range(6)] for _ in range(6)]
        self.ships = {"трёхпалубный": 3, "двухпалубный": 2, "однопалубный": 1}
        self.ships_count = {"трёхпалубный": 1, "двухпалубный": 2, "однопалубный": 4}
        self.letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5}
        self.players = [self.Player("Игрок 1"), self.AIPlayer()]
        self.current_player_index = 0
        self.place_ships_player()
        self.place_ships_ai()

    def print_gameboard(self, board):
        columns = "  A B C D E F"
        print(columns)
        for i, row in enumerate(board, start=1):
            print(i, ' '.join(row))

    def is_within_bounds(self, x, y):
        return 0 <= x < 6 and 0 <= y < 6

    def count_hits(self, board):
        return sum(row.count("X") for row in board)

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def is_valid_placement(self, board, x, y, size, direction):
        for i in range(size):
            nx, ny = (x + i, y) if direction == 'H' else (x, y + i)
            if not self.is_within_bounds(nx, ny) or board[ny][nx] != '-':
                return False
        return True

    def place_ship(self, board, x, y, size, direction):
        for i in range(size):
            nx, ny = (x + i, y) if direction == 'H' else (x, y + i)
            board[ny][nx] = "■"

    def place_ships_player(self):
        print("Расставьте свои корабли.")
        for ship, size in self.ships.items():
            for _ in range(self.ships_count[ship]):
                while True:
                    try:
                        print(f"Установка {ship} (размер {size})")
                        x_letter, y_number = self.players[0].get_coordinates()
                        direction = self.players[0].choose_ship_direction()
                        x = self.letter_to_index[x_letter]
                        y = int(y_number) - 1

                        if self.is_valid_placement(self.player_board, x, y, size, direction):
                            self.place_ship(self.player_board, x, y, size, direction)
                            self.print_gameboard(self.player_board)
                            break
                        else:
                            print("Неверное размещение! Попробуйте снова.")
                    except ValueError:
                        print("Ошибка! Введите корректные координаты.")

    def place_ships_ai(self):
        for ship, size in self.ships.items():
            for _ in range(self.ships_count[ship]):
                while True:
                    x = random.randint(0, 5)
                    y = random.randint(0, 5)
                    direction = random.choice(['H', 'V'])
                    if self.is_valid_placement(self.ai_board, x, y, size, direction):
                        self.place_ship(self.ai_board, x, y, size, direction)
                        break

    def take_shot(self):
        while self.count_hits(self.ai_board) < 10 and self.count_hits(self.player_board) < 10:
            player = self.players[self.current_player_index]
            print(f"Ходит {player.name}")
            try:
                x_letter, y_number = player.get_coordinates()
                x = self.letter_to_index[x_letter]
                y = int(y_number) - 1

                target_board = self.ai_board if self.current_player_index == 0 else self.player_board
                display_board = [['-' if cell == '■' else cell for cell in row] for row in target_board]

                if target_board[y][x] == "■":
                    print("Попадание!")
                    target_board[y][x] = "X"
                elif target_board[y][x] == "-":
                    print("Промах!")
                    target_board[y][x] = "T"
                else:
                    print("Вы уже стреляли в эту клетку!")
                    continue

                display_board = [['-' if cell == '■' else cell for cell in row] for row in target_board] #Отображение доски после каждого выстрела
                self.print_gameboard(display_board)

                if self.count_hits(target_board) >= 10:  #Победный счетчик
                    print(f"{player.name} победил!")
                    break

                self.switch_player()
            except ValueError:
                print("Ошибка! Введите корректные координаты.")


game = Game()
game.take_shot()
