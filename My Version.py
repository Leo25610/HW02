import random


class BoardOutException(Exception):
    def __init__(self,message ='Выход за границы игрового поля'):
        super.__init__(message)


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:
    def __init__(self, length, nose, direction):
        self.length = length
        self.nose = nose
        self.direction = direction
        self.lives = length

    def dots(self):
        ship_dots = []
        for i in range(self.length):
            if self.direction == 0:
                ship_dots.append(Dot(self.nose.x, self.nose.y + i))
            else:
                ship_dots.append(Dot(self.nose.x + i, self.nose.y))
        return ship_dots


class Board:
    def __init__(self, size=6, hid=False):
        self.size = size
        self.hid = hid
        self.field = [['◯'] * size for _ in range(size)]
        self.ships = []
        self.alive_ships = 0

    def can_place_ship(self, ship):              #Проверка на минимальное расстояние в 1 клетку
        for dot in ship.dots():
            if self.out(dot) or self.field[dot.x][dot.y] != '◯':
                return False
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    cur = Dot(dot.x + dx, dot.y + dy)
                    if not self.out(cur) and self.field[cur.x][cur.y] == '■':
                        return False
        return True

    def add_ship(self, ship):
        if not self.can_place_ship(ship):
            raise ValueError("Нельзя разместить корабль здесь!")
        for dot in ship.dots():
            self.field[dot.x][dot.y] = '■'
        self.ships.append(ship)
        self.alive_ships += 1

    def print_board(self, reveal=False):
        columns = "  A B C D E F"
        print(columns)
        for i, row in enumerate(self.field, start=1):
            if self.hid and not reveal:
                row_display = ["◯" if cell in ("◯", "■") else cell for cell in row]
            else:
                row_display = row
            print(i, ' '.join(row_display))

    def out(self, dot):
        return not (0 <= dot.x < self.size and 0 <= dot.y < self.size)

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()
        if self.field[dot.x][dot.y] in ('X', 'T'):
            raise ValueError("В эту клетку уже стреляли!")
        for ship in self.ships:
            if dot in ship.dots():
                self.field[dot.x][dot.y] = "X"
                ship.lives -= 1
                if ship.lives == 0:
                    self.alive_ships -= 1
                    return "Корабль уничтожен!"
                return "Попадание!"
        self.field[dot.x][dot.y] = "T"
        return "Мимо!"


class Player:
    def __init__(self, own_board, enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board

    def ask(self):
        return Dot(random.randint(0, self.own_board.size - 1), random.randint(0, self.own_board.size - 1))

    def move(self):
        while True:
            try:
                print("Ваше поле:")
                self.own_board.print_board(reveal=True)
                print("Поле противника:")
                self.enemy_board.print_board()

                target = self.ask()
                result = self.enemy_board.shot(target)
                print(f"Выстрел по ({chr(target.y + 65)}{target.x + 1}) - {result}")
                return result == "Попадание!"
            except BoardOutException as e:
                print(e)
            except ValueError as e:
                print(e)


class User(Player):
    def ask(self):
        while True:
            try:
                coord = input("Введите координаты выстрела (например, A1): ").upper()
                if len(coord) < 2 or len(coord) > 3:
                    raise ValueError
                col, row = coord[0], coord[1:]
                if col not in "ABCDEF" or not row.isdigit():
                    raise ValueError
                x = int(row) - 1
                y = ord(col) - 65
                return Dot(x, y)
            except ValueError:
                print("Неверный формат ввода! Введите букву (A-F) и цифру (1-6), например, A1.")


class Game:
    def __init__(self, size=6):
        self.size = size
        self.user_board = Board(size)
        self.ai_board = Board(size, hid=True)
        self.user = User(self.user_board, self.ai_board)
        self.ai = Player(self.ai_board, self.user_board)

    def random_board(self, board):
        ship_sizes = [3, 2, 2, 1, 1, 1, 1]
        for size in ship_sizes:
            placed = False
            while not placed:
                try:
                    x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                    direction = random.randint(0, 1)
                    ship = Ship(size, Dot(x, y), direction)
                    board.add_ship(ship)
                    placed = True
                except ValueError:
                    continue

    def greet(self):
        print("Добро пожаловать в игру Морской бой!")
        print("Формат ввода: буква (A-F) и цифра (1-6), например, A1")

    def loop(self):
        while self.user_board.alive_ships > 0 and self.ai_board.alive_ships > 0:
            self.user.move()
            if self.ai_board.alive_ships == 0:
                print("Вы победили!")
                break
            self.ai.move()
            if self.user_board.alive_ships == 0:
                print("ИИ победил!")
                break

    def start(self):
        self.greet()
        self.random_board(self.user_board)
        self.random_board(self.ai_board)
        self.loop()


if __name__ == "__main__":
    game = Game()
    game.start()
