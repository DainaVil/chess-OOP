from Functions import get_enemy_color
from Move import Move


class Fig():
    letter = None
    key = None

    def __init__(self, color):
        self.color = color

    def __str__(self):
        res = ''

        return res + self.letter[self.color]

    def get_moves(self, y, x, board):
        return []

    def get_attacked_fields(self, y, x, board):
        moves = self.get_moves(y, x, board)
        fields = []
        for move in moves:
            fields.append((move.ty, move.tx))
        return fields


class Empty(Fig):
    def __init__(self):
        super().__init__(-1)

    def get_moves(self, y, x, board):
        print('На этом поле нет фигуры')

    def __str__(self):
        return '.'


class King(Fig):
    letter = ('K', 'k')
    key = 'K'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        poss_moves = []
        dirs = ((1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0))
        for d in dirs:
            ty, tx = y + d[0], x + d[1]
            if board.is_empty(ty, tx):
                poss_moves.append(Move(y, x, ty, tx, self.key, '-'))
            elif board.get_fig(ty, tx, get_enemy_color(self.color)) is not None:
                poss_moves.append(Move(y, x, ty, tx, self.key, 'x'))

        # Рокировка в короткую сторону
        if board.is_empty(y, 5) and board.is_empty(y, 6)\
            and not board.is_in_danger(y, 4, get_enemy_color(self.color)) \
            and not board.is_in_danger(y, 5, get_enemy_color(self.color))\
            and not board.is_in_danger(y, 6, get_enemy_color(self.color))\
            and board.move_mask[y][4] == 0 and board.move_mask[y][7] == 0:
            poss_moves.append(Move(y, x, y, 6, self.key, '0-0'))
        
        # Рокировка в длинную сторону
        if board.is_empty(y, 1) and board.is_empty(y, 2) and board.is_empty(y, 3)\
                and not board.is_in_danger(y, 2, get_enemy_color(self.color)) \
                and not board.is_in_danger(y, 3, get_enemy_color(self.color)) \
                and not board.is_in_danger(y, 4, get_enemy_color(self.color)) \
                and board.move_mask[y][4] == 0 and board.move_mask[y][0] == 0:
            poss_moves.append(Move(y, x, y, 2, self.key, '0-0-0'))
        return poss_moves

    def get_attacked_fields(self, y, x, board):
        fields = []
        dirs = ((1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0))
        for d in dirs:
            fields.append((y + d[0], x + d[1]))
        return fields
    

class Queen(Fig):
    letter = ('Q', 'q')
    key = 'Q'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        poss_moves = []
        dirs = ((1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0))
        for d in dirs:
            ty, tx = y + d[0], x + d[1]
            while True:
                if board.is_empty(ty, tx):
                    poss_moves.append(Move(y, x, ty, tx, self.key, '-'))
                elif board.get_fig(ty, tx, get_enemy_color(self.color)) is not None:
                    poss_moves.append(Move(y, x, ty, tx, self.key, 'x'))
                    break
                else:
                    break
                ty, tx = ty + d[0], tx + d[1]
        return poss_moves
    
    
class Knight(Fig):
    letter = ['N', 'n']
    key = 'N'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        poss_moves = []
        dirs = ((-2, -1), (-1, -2), (-2, 1), (1, -2), (2, -1), (-1, 2), (2, 1), (1, 2))
        for d in dirs:
            ty = y + d[0]
            tx = x + d[1]
            if board.is_empty(ty, tx):
                poss_moves.append(Move(y, x, ty,tx, self.key, '-'))

            if board.get_fig(ty, tx, get_enemy_color(self.color)) is not None:
                poss_moves.append(Move(y, x, ty, tx, self.key, 'x'))

        return poss_moves


class Rook(Fig):
    letter = ('R', 'r')
    key = 'R'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        poss_moves = []
        dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
        for d in dirs:
            ty, tx = y + d[0], x + d[1]
            while True:
                if board.is_empty(ty, tx):
                    poss_moves.append(Move(y, x, ty, tx, self.key, '-'))
                elif board.get_fig(ty, tx, get_enemy_color(self.color)) is not None:
                    poss_moves.append(Move(y, x, ty, tx, self.key, 'x'))
                    break
                else:
                    break
                ty, tx = ty + d[0], tx + d[1]
        return poss_moves


class Bishop(Fig):
    letter = ('B', 'b')
    key = 'B'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        poss_moves = []
        dirs = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        for d in dirs:
            ty, tx = y + d[0], x + d[1]
            while True:
                if board.is_empty(ty, tx):
                    poss_moves.append(Move(y, x, ty, tx, self.key, '-'))
                elif board.get_fig(ty, tx, get_enemy_color(self.color)) is not None:
                    poss_moves.append(Move(y, x, ty, tx, self.key, 'x'))
                    break
                else:
                    break
                ty, tx = ty + d[0], tx + d[1]
        return poss_moves


class Pawn(Fig):
    letter = ('P', 'p')
    key = ''

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        poss_moves = []
        
        # Для черной пешки
        if self.color == 1:
            # Обычный ход вперед
            if board.is_empty(y - 1, x):
                poss_moves.append(Move(y, x, y - 1, x, self.key, '-'))
            # Длинный ход вперед
            if board.is_empty(y - 1, x) \
                    and board.is_empty(y - 2, x) \
                    and y == 6:
                poss_moves.append(Move(y, x, y - 2, x, self.key, 'l'))

            # Взятия влево и вправо
            if board.get_fig(y - 1, x - 1, get_enemy_color(self.color)):
                poss_moves.append(Move(y, x, y - 1, x - 1, self.key, 'x'))
            if board.get_fig(y - 1, x + 1, get_enemy_color(self.color)):
                poss_moves.append(Move(y, x, y - 1, x + 1, self.key, 'x'))

            # Взятия на проходе
            if board.is_empty(y - 1, x - 1) and board.move_mask[y - 1][x - 1] == 2:
                poss_moves.append(Move(y, x, y - 1, x - 1, self.key, 'xp'))
            if board.is_empty(y - 1, x + 1) and board.move_mask[y - 1][x + 1] == 2:
                poss_moves.append(Move(y, x, y - 1, x + 1, self.key, 'xp'))

        # Для белой пешки
        if self.color == 0:
            #Обычный ход вперед
            if board.is_empty(y + 1, x):
                poss_moves.append(Move(y, x, y + 1, x, self.key, '-'))
            # Длинный ход вперед
            if board.is_empty(y + 1, x) and board.is_empty(y + 2, x) and y == 1:
                poss_moves.append(Move(y, x, y + 2, x, self.key, 'l'))
                
            # if board.is_empty(y, x + 1 ):
            #     poss_moves.append(Move(y, x, y, x+1, self.key, '-'))
            # # Длинный ход вперед
            # if board.is_empty(y, x+1) \
            #         and board.is_empty(y, x+2) \
            #         and y == 1:
            #     poss_moves.append(Move(y, x, y, x +2, self.key, 'l'))

            # Взятия влево и вправо
            if board.get_fig(y + 1, x - 1, get_enemy_color(self.color)):
                poss_moves.append(Move(y, x, y + 1, x - 1, self.key, 'x'))
            if board.get_fig(y + 1, x + 1, get_enemy_color(self.color)):
                poss_moves.append(Move(y, x, y + 1, x + 1, self.key, 'x'))

            # Взятия на проходе
            if board.is_empty(y + 1, x - 1) and board.move_mask[y + 1][x - 1] == 2:
                poss_moves.append(Move(y, x, y + 1, x - 1, self.key, 'xp'))
            if board.is_empty(y + 1, x + 1) and board.move_mask[y + 1][x + 1] == 2:
                poss_moves.append(Move(y, x, y + 1, x + 1, self.key, 'xp'))
        return poss_moves

    def get_attacked_fields(self, y, x, board):
        if self.color == 0:
            return [(y + 1, x - 1), (y + 1, x + 1)]
        else:
            return [(y - 1, x - 1), (y - 1, x + 1)]
        
class Checker(Fig):
    letter = (chr(9679), chr(9675))
    key = 'p'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        moves = []
        # dirs = ((1 - 2 * self.color, -1),(1 - 2 * self.color, 1))
        dirs = ((1,1), (1,-1), (-1,-1), (-1,1))
        
        for d in dirs:
            if board.get_fig(d[0] + y, d[1] + x, color=get_enemy_color(self.color)) is not None and \
                    board.is_empty(2 * d[0] + y, 2 * d[1] + x):
                moves.append(Move(y, x, 2 * d[0] + y, 2 * d[1] + x, self.key, 'x',\
                                  extra_info='d' if d[0] + y == self.color * 7 else None))
        # Для белой шашки
        if self.color == 0:
            for d in dirs[:2]:
                if board.is_empty(d[0] + y, d[1] + x):
                    moves.append(Move(y, x, d[0] + y, d[1] + x, self.key, '-',\
                                      extra_info='d' if 2 * d[0] + y == self.color * 7 else None))
        # Для черной шашки
        if self.color == 1:
            for d in dirs[2:]:
                if board.is_empty(d[0] + y, d[1] + x):
                    moves.append(Move(y, x, d[0] + y, d[1] + x, self.key, '-',\
                                      extra_info='d' if 2 * d[0] + y == self.color * 7 else None))
                    
        return moves

    def get_attacked_fields(self, y, x, board):
        fields = []
        for move in self.get_moves(y, x, board):
            if move.mode == 'x':
                fields.append(((move.ty + move.fy) / 2, (move.tx + move.fx) / 2))
        return fields

class Damka(Fig):
    letter = (chr(9734), chr(9735))
    key = 'd'

    def __init__(self, color):
        super().__init__(color)

    def __stopper(self, ty, tx, board, eaten):
        if eaten:
            return board.is_empty(ty, tx)
        else:
            return board.get_fig(ty, tx, color=self.color) is None and 0 <= ty <= 7 and 0 <= tx <= 7

    def get_moves(self, y, x, board):
        moves = []
        dirs = ((-1, -1),(-1, 1),(1, -1),(1, 1))
        
        # for d in dirs:
        #     eaten = False
        #     ty, tx = d
        #     while 0 <= ty <= 7 and 0 <= tx <= 7: 
        #         ty += d[0]
        #         tx += d[1]
        #         if not eaten:
        #             if board.is_empty(ty, tx):
        #                 moves.append(Move(y, x, ty, tx, self.key, '-'))
        #             elif board.get_fig(ty, tx, color=get_enemy_color(self.color)) is not None and board.is_empty(ty+d[0], tx+d[1]):
        #                 eaten = True
        #                 moves.append(Move(y, x, ty+d[0], tx+d[1], self.key, 'x'))
        #         else:
        #             break
            
        
        for d in dirs:
            ty, tx = y + d[0], x + d[1]
            eat = False
            while self.__stopper(ty, tx, board, eat):
                if eat:
                    moves.append(Move(y, x, ty, tx, self.key, 'x'))
                else:
                    if board.is_empty(ty, tx):
                        moves.append(Move(y, x, ty, tx, self.key, '-'))
                    elif board.get_fig(ty, tx, color=get_enemy_color(self.color)) is not None:
                        eat = True
                ty += d[0]
                tx += d[1]
        return moves
