from Board import Board, CheckersBoard
from Functions import str2coord, get_enemy_color


class App:
    def __init__(self):
        self.player = 0
        self.board = Board()
        self.moves = []
        # self.moves_log = []
        # self.notation = False
        # self.chosen_fig = None

    def choose(self, inp):
        y, x = str2coord(inp[1])
        self.moves = self.board.get_val_moves(y, x, self.player)
        if self.board.is_empty(y, x):
            return 'Выбор не сделан'
            # self.chosen_fig = self.board.get_fig(y, x)
            # self.chosen_fig.coord = (y, x)
        return f'Выбрана фигура {self.board.get_fig(y,x)}'
        

    def show(self, inp = []):
        if inp[0] == 'H':
            return self.board.show(moves=self.moves)
        else:
            return self.board.show()

    def move(self, inp, notation=False):
        y, x = str2coord(inp[1])
        for move in self.moves:
            if move.tx == x and move.ty == y:
                do = self.board.perform_move(move)
                if do == 'P':
                    self.change_pawn()
                # if self.notation == True:
                #     self.moves_log.append(move)
                self.player = get_enemy_color(self.player)
                self.moves = []
                
                if self.board.if_checkmate(self.player):
                    return f'{"Белые" if self.player == 0 else "Черные"} получают мат!'
                print(self.board.show())
                return f'Ходят {"белые" if self.player == 0 else "черные"}'
        return 'Такой ход невозможен'

    def undo(self, inp):
        if len(self.board.moves) > 0:
            self.board.undo()
            self.player = get_enemy_color(self.player)
            self.moves = []
            print(self.board.show())
            return 'Отменен последний ход'
        return 'Нельзя дальше отменить'

    def danger(self, inp):
        return self.board.danger(self.player)
    
    def change_pawn(self):
        new = input('ЗВведите новыю фигуру Q/B/N/R: ')
        while new.upper() not in ('Q', 'B', 'N', 'R'):
            new = input('Введите новыю фигуру Q/B/N/R: ')
        self.board.change_pawn(new.upper())
        
    def test(self):
        from Figs import Rook, King, Queen, Knight, Pawn, Empty, Bishop
        
        self.board.board = [
            [Rook(0), Empty(), Empty(), Empty(), King(0), Bishop(0), Knight(0), Rook(0)],
            [Pawn(0) for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Pawn(1) for x in range(8)],
            [Rook(1), Knight(1), Bishop(1), Queen(1), King(1), Empty(), Empty(), Rook(1)]]
            
        print('''S - Вывести поле
C <координаты фигуры> - Выбор фигуры
M <координаты клетки> - Переставить выбранную фигуру 
H <координаты клетки> - Посмотреть возможные ходы (сначала надо выбрать фигуру)
D - Посмотреть угрожаемые фигуры
U - Отмена хода
E - Выход''')
        print(self.board.show())
        funcs = {'C': self.choose, 'S': self.show, 'M': self.move, 'U': self.undo, 'D': self.danger, 'H': self.show}
        command = ''
            
            
        while command.upper() != 'E':
            command = input('Введите команду: ')
            inp = command.upper().split()
            while not inp[0].isalpha() or inp[0].upper() not in ('C', 'D', 'U', 'S', 'M', 'H', 'E'):
                command = input('Введите команду: ')
                inp = command.upper().split()
            if command.upper() == 'E':
                break
            print(funcs[inp[0].upper()](inp))

    def run(self):
        # notation = input('Записывать партию? [y/n]')
        # while notation not in ('y','n'):
        #     notation = input('Записывать партию? [y/n]')
            
        # if notation == 'y':
        #     self.notation = True
        #     name = input('Введите название файла: ')
        #     f = open(name,'a')
            
        print('''S - Вывести поле
C <координаты фигуры> - Выбор фигуры
M <координаты клетки> - Переставить выбранную фигуру 
H <координаты клетки> - Посмотреть возможные ходы (сначала надо выбрать фигуру)
D - Посмотреть угрожаемые фигуры
U - Отмена хода
E - Выход''')
        print(self.board.show())
        funcs = {'C': self.choose, 'S': self.show, 'M': self.move, 'U': self.undo, 'D': self.danger, 'H': self.show}
        command = ''
            
            
        while command.upper() != 'E':
            command = input('Введите команду: ')
            inp = command.upper().split()
            while not inp[0].isalpha() or inp[0].upper() not in ('C', 'D', 'U', 'S', 'M', 'H', 'E'):
                command = input('Введите команду: ')
                inp = command.upper().split()
            if command.upper() == 'E':
                break
            print(funcs[inp[0].upper()](inp))
        
        # m = [str(i) for i in self.moves_log]
        # print(m)
        # if notation == True:
        #     f.close()
            
            
class CheckersApp(App):
    
    def __init__(self):
        super().__init__()
        self.board = CheckersBoard()
        self.blocked = False

    def move(self, inp):
        y, x = str2coord(inp[1])
        for move in self.moves:
            if move.tx == x and move.ty == y:
                do = self.board.perform_move(move)
                # print(do)
                self.moves = [] if not do else self.board.get_val_moves(y, x, self.player)
                self.player = get_enemy_color(self.player) if not do else self.player
                self.blocked = do
                print(self.board.show())
                
                if self.board.if_checkmate(self.player):
                    return f'{"Белые" if self.player == 1 else "Черные"} выиграли!'
                
                return f'Ходят {"белые" if self.player == 0 else "черные"}' if not do else 'Ешьте на здоровье!'
        return 'Такой ход невозможен'
    
    def choose(self, inp):
        if not self.blocked:
            return super().choose(inp)
        else:
            return 'Продолжайте есть'
        
    def test(self):
        from Figs import Empty, Checker, Damka
        self.board.board = [
            [Empty() for x in range(8)],
            [Empty(), Checker(0), Empty(), Checker(0), Empty(), Checker(0), Empty(), Checker(0)],
            [Empty() for x in range(8)],
            [Empty(), Checker(0), Empty(), Empty(), Empty(), Empty(), Empty(), Empty()],
            [Empty(), Empty(), Checker(1), Empty(), Empty(), Empty(), Checker(0), Empty()],
            [Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty()],
            [Checker(1), Empty(), Checker(1), Empty(), Checker(1), Empty(), Checker(1), Empty()],
            [Empty() for x in range(8)]]
        
        # self.board.board = [
        #     [Empty() for x in range(8)],
        #     [Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty()],
        #     [Empty(), Empty(), Empty(), Checker(0), Empty(), Empty(), Empty(), Empty()],
        #     [Empty(), Empty(), Checker(1), Empty(), Empty(), Empty(), Empty(), Empty()],
        #     [Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty()],
        #     [Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty()],
        #     [Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty()],
        #     [Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty()]]
            

        print('''S - Вывести поле
C <координаты фигуры> - Выбор фигуры
M <координаты клетки> - Переставить выбранную фигуру 
H <координаты клетки> - Посмотреть возможные ходы (сначала надо выбрать фигуру)
D - Посмотреть угрожаемые фигуры
U - Отмена хода
E - Выход''')
        print(self.board.show())
        funcs = {'C': self.choose, 'S': self.show, 'M': self.move, 'U': self.undo, 'D': self.danger, 'H': self.show}
        command = ''
            
            
        while command.upper() != 'E':
            command = input('Введите команду: ')
            inp = command.upper().split()
            while not inp[0].isalpha() or inp[0].upper() not in ('C', 'D', 'U', 'S', 'M', 'H', 'E'):
                command = input('Введите команду: ')
                inp = command.upper().split()
            if command.upper() == 'E':
                break
            print(funcs[inp[0].upper()](inp))