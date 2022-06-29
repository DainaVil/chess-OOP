from Figs import Rook, King, Queen, Knight, Pawn, Empty, Bishop, Checker, Damka
from Functions import get_enemy_color
from colorama import Back, Style

class Board:
    def __init__(self):
        self.moves = []
        self.board = []
        self.move_mask = []
        self.__generate_new_field()

    def __generate_new_field(self):
        self.moves = []
        self.board = [
            [Rook(0), Knight(0), Bishop(0), Queen(0), King(0), Bishop(0), Knight(0), Rook(0)],
            [Pawn(0) for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Pawn(1) for x in range(8)],
            [Rook(1), Knight(1), Bishop(1), Queen(1), King(1), Bishop(1), Knight(1), Rook(1)]
        ]
        self.move_mask = [[0 for x in range(8)] for y in range(8)]

    def show(self, moves=None):
        if moves is None:
            moves = []
        fields = []
        for move in moves:
            fields.append((move.ty, move.tx))
        res = '\n'
        res += '    A B C D E F G H  \n'
        res += '\n'
        for y in range(7,-1,-1):
            res += f'{y + 1}   '
            for x in range(8):
                if (y,x) in fields:
                    res += Back.YELLOW + str(self.board[y][x])
                else:
                    res += Style.RESET_ALL + str(self.board[y][x])
                res += Style.RESET_ALL + ' '
            res += f'   {y + 1}\n'

        res += '\n'
        res += '    A B C D E F G H  \n'
        return res

    def danger(self, for_player):
        moves = []
        for y in range(8):
            for x in range(8):
                cur_moves = self.get_val_moves(y, x, get_enemy_color(for_player))
                for move in cur_moves:
                    if move.mode == 'x':
                        moves.append(move)
        res = self.show(moves)
        if self.if_check(for_player):
            res += 'Шах!'
        return res

    def get_fig(self, y, x, color=None):
        if color is None:
            if 0 <= y <= 7 and 0 <= x <= 7:
                return self.board[y][x]
            else:
                return None
        else:
            fig = self.get_fig(y, x)
            if fig is not None and fig.color == color:
                return fig
            else:
                return None

    def is_empty(self, y, x):
        return self.get_fig(y, x, -1) is not None

    def get_moves(self, y, x, color):
        fig = self.get_fig(y, x, color)
        if fig is None:
            return []
        else:
            return fig.get_moves(y, x, self)

    def perform_move(self, move):
        fy, fx, ty, tx = move()
        self.board[ty][tx] = self.board[fy][fx]
        self.board[fy][fx] = Empty()
        self.__update_move_mask(move)

        if move.mode == 'xp':
            self.board[fy][tx] = Empty()

        if move.mode == '0-0':
            self.board[fy][5] = self.board[fy][7]
            self.board[fy][7] = Empty()

        if move.mode == '0-0-0':
            self.board[fy][3] = self.board[fy][0]
            self.board[fy][0] = Empty()
            
        self.moves.append(move)
        
        if move.key == '' and ty in (0, 7) and move.extra_info is None:
            return 'P'
        if move.key == '' and ty in (0, 7) and move.extra_info is not None:
            figs = {'Q': Queen, 'R': Rook, 'B': Bishop, 'N': Knight}
            color = 1 if ty == 0 else 0
            self.board[ty][tx] = figs[move.extra_info](color)
            
    def change_pawn(self, key):
        self.moves[len(self.moves) - 1].extra_info = key

    def __update_move_mask(self, move):
        fy, fx, ty, tx = move()
        self.move_mask[fy][fx] = 1
        self.move_mask[ty][tx] = 1
        for y in range(8):
            for x in range(8):
                if self.move_mask[y][x] == 2:
                    self.move_mask[y][x] = 1
        if move.mode == 'l':
            self.move_mask[(fy + ty) // 2][tx] = 2

    def is_in_danger(self, y, x, color):  
        for ny in range(8):
            for nx in range(8):
                fig = self.get_fig(ny, nx, color)
                if fig is not None:
                    fields = fig.get_attacked_fields(ny, nx, self)
                    if (y, x) in fields:
                        return True
        return False

    def if_check(self, color):  # color - цвет короля, шахи которому мы смотрим
        for y in range(8):
            for x in range(8):
                if self.get_fig(y, x, color) is not None and self.get_fig(y, x, color).key == 'K':

                    return self.is_in_danger(y, x, get_enemy_color(color))

    def undo(self):
        if len(self.moves) > 0:
            moves = self.moves.copy()
            moves.pop()
            self.__generate_new_field()
            for move in moves:
                self.perform_move(move)

    def get_val_moves(self, y, x, color):
        val_moves = []
        moves = self.get_moves(y, x, color)
        for move in moves:
            self.perform_move(move)
            if not self.if_check(color):
                val_moves.append(move)
            self.undo()
        return val_moves

    def if_checkmate(self, color):  
        val_moves = 0
        for y in range(8):
            for x in range(8):
                val_moves += len(self.get_val_moves(y, x, color))

        if val_moves == 0:
            return self.if_check(color)
        return False
        
class CheckersBoard(Board):
    
    def __init__(self):
        super().__init__()
        self._generate_new_field()
    
    def _generate_new_field(self):
        self.moves = []
        self.board = [
            [Checker(0), Empty(), Checker(0), Empty(), Checker(0), Empty(), Checker(0), Empty()],
            [Empty(), Checker(0), Empty(), Checker(0), Empty(), Checker(0), Empty(), Checker(0)],
            [Checker(0), Empty(), Checker(0), Empty(), Checker(0), Empty(), Checker(0), Empty()],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Empty(), Checker(1), Empty(), Checker(1), Empty(), Checker(1), Empty(), Checker(1)],
            [Checker(1), Empty(), Checker(1), Empty(), Checker(1), Empty(), Checker(1), Empty()],
            [Empty(), Checker(1), Empty(), Checker(1), Empty(), Checker(1), Empty(), Checker(1)]]
        self.move_mask = [[0 for x in range(8)] for y in range(8)]

    def perform_move(self, move):
        super().perform_move(move)
        if move.mode == 'x':
            if move.key == 'd':
                ny, nx = move.fy, move.fx
                dy = (move.ty - move.fy) // abs(move.ty - move.fy)
                dx = (move.tx - move.fx) // abs(move.tx - move.fx)
                while self.is_empty(ny, nx):
                    ny += dy
                    nx += dx
                self.board[ny][nx] = Empty()
            else:
                self.board[(move.ty + move.fy) // 2][(move.tx + move.fx) // 2] = Empty()

        if (move.ty == 0 and self.get_fig(move.ty, move.tx).color == 1) \
            or (move.ty == 7 and self.get_fig(move.ty, move.tx).color == 0):
            self.board[move.ty][move.tx] = Damka(abs((move.ty // 7)-1))
            move.extra_info = 'd'
            
        
        for m in self.get_val_moves(move.ty, move.tx, self.get_fig(move.ty, move.tx).color):
            if m.mode == 'x' == move.mode:
                return True
        return False
    
    def if_checkmate(self, color):
        
        for y in range(8):
            for x in range(8):
                if self.get_fig(y, x).color == color:
                    return False
        else:
            return True
    def get_val_moves(self, y, x, color):
        can_eat = False
        for ny in range(8):
            for nx in range(8):
                for move in self.get_moves(ny, nx, color):
                    if move.mode == 'x':
                        can_eat = True
        if can_eat:
            val_moves = []
            for move in self.get_moves(y, x, color):
                if move.mode == 'x':
                    val_moves.append(move)
            return val_moves
        return self.get_moves(y, x, color)
    