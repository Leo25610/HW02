import random
class Exceptions:
    @staticmethod
    def board_out_exception():
        raise Exception("Выход за границы игрового поля!")

    @staticmethod
    def ship_too_close_exception():
        raise Exception("Ошибка: корабли должны находиться на расстоянии минимум 1 клетка друг от друга!")


class Game:
    class Player:   #Подкласс для реального игрока
        def __init__(self,name):
            self.name=name
        def get_coordinates(self):
            x=input(f'{self.name}, введите координаты (A-F): ').upper()
            y=input(f'{self.name}, введите координаты (1-6): ')
            return x,y
        def choose_directions(self):
            while True:
                direction=input('Выбирете направление (H-горизонтально или V-вертикально)')
                if direction in ("H","v"):
                    return direction
                else:
                    print("Ошибка ввода! В  ведите корректное значение!")



    class AIPlayer:   #Подкласс для ИИ
        def __init__(self):
            self.name= "AI"

        def get_coordinates(self):
            x = random.choice(["A","B","C","D","E","F",""])
            y = str(random.choice([1,2,3,4,5,6]))
            return x,y


    def __init__(self):
        self.game_board = [['-' for _ in range(6)] for _ in range(6)]
        self.ai_board = [['-'for _ in range(6)] for _ in range(6)]
        self.ships = {"трёхпалубный": 3, "двухпалубный": 2, "однопалубный": 1}
        self.ships_count = {"трёхпалубный": 1, "двухпалубный": 2, "однопалубный": 4}
        self.letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5}
        self.players=[self.Player("Игрок 1"),self.AIPlayer()]
    def print_gameboard(self):  # Вывод игрового поля в консоль
        columns = "  A B C D E F"
        print(columns)
        for i, row in enumerate(self.game_board, start=1):
            print(i, ' '.join(row))

    def is_within_bounds(self, x, y):  # Проверка координат
        if not (0 <= x < 6 and 0 <= y < 6):
            Exceptions.board_out_exception()
        return True

    def is_valid_placement(self, x, y, size, direction):  # Проверка возможности размещения
        for i in range(size):
            nx, ny = (x + i, y) if direction == 'H' else (x, y + i)
            if not (0 <= nx < 6 and 0 <= ny < 6) or self.game_board[ny][nx] != '-':
                return False
        return True

    def mark_ship_on_board(self, x, y, size, direction):  # Установка корабля на поле
        for i in range(size):
            nx, ny = (x + i, y) if direction == 'H' else (x, y + i)
            self.game_board[ny][nx] = '■'
        self.mark_surrounding_area(x, y, size, direction)

    def mark_surrounding_area(self, x, y, size, direction):  # Отмечаем клетки вокруг корабля
        for i in range(-1, size + 1):
            for j in [-1, 0, 1]:
                nx, ny = (x + i, y + j) if direction == 'H' else (x + j, y + i)
                if 0 <= nx < 6 and 0 <= ny < 6 and self.game_board[ny][nx] == '-':
                    self.game_board[ny][nx] = '.'

    def display_ship_info(self):  # Вывод информации о кораблях
        print("Необходимо расставить следующие корабли:")
        for ship, count in self.ships_count.items():
            print(f"{ship}: {count} шт.")

    def setup_ships(self):  # Функция расстановки кораблей
        print("Расставьте свои корабли на поле")
        self.print_gameboard()
        for ship, count in self.ships_count.items():
            size = self.ships[ship]
            for _ in range(count):
                while True:
                    player = self.Player()
                    player.get_coordinates()
                    try:
                        x = self.letter_to_index.get(player.x, -1)
                        y = int(player.y) - 1
                        self.is_within_bounds(x, y)
                        if player.direction not in ('H', 'V'):
                            raise ValueError("Ошибка: направление должно быть H или V!")
                        if self.is_valid_placement(x, y, size, player.direction):
                            self.mark_ship_on_board(x, y, size, player.direction)
                            self.print_gameboard()
                            break
                        else:
                            print("Ошибка: невозможно разместить корабль здесь!")
                    except Exception as e:
                        print(e)
                    except ValueError:
                        print("Ошибка: введите корректные координаты!")
    def count_hits(self):
        return sum(row.count("X") for row in self.game_board)
    def take_shot(self):
        print("Введите координаты выстрела")
        while self.counts_hit() <10:
            try:
                x_letter = input("Введите букву (A-F): ").upper()
                y_number = input("Введите цифру (1-6): ")

                x = self.letter_to_index.get(x_letter, -1)
                y = int(y_number) - 1

                if not self.is_within_bounds(x, y):
                    print("Координаты вне поля. Попробуйте снова.")
                    continue  # Запрос координат заново

                if self.game_board[y][x] == "■":
                    print("Попадание!")
                    self.game_board[y][x] = "X"  # Помечаем попадание
                elif self.game_board[y][x] == "-":
                    print("Промах!")
                    self.game_board[y][x] = "T"  # Теперь промахи обозначаются буквой "T"
                else:
                    print("Вы уже стреляли в эту клетку!")
                    continue  # Запрос нового выстрела

                self.print_gameboard()  # Вывести обновлённое поле
                if "X">=10:
                    break

            except ValueError:
                print("Ошибка! Введите корректные координаты.")


game = Game()
game.display_ship_info()
game.setup_ships()
game.take_shot()
