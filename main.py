from App import App, CheckersApp

# d = {'0': App, '1': CheckersApp}
# app = input('Выберете игру: (chess - 0, checkers - 1): ').lower()
# while app.lower() not in d.keys():
#     app = input('Выберете игру: (chess - 0, checkers - 1): ').lower()
# app = d[app]()
# app.run()


# тест шашек

# a = CheckersApp()
# a.test()


# Проверка рокировки

a = App()
a.test()

# Проверка превращения пешки - не работает

# from Figs import Rook, King, Queen, Knight, Pawn, Empty, Bishop
# from Board import Board
# from Functions import str2coord
# b = Board()
# b.board = [
#             [Rook(0), Empty(), Empty(), Empty(), King(0), Bishop(0), Knight(0), Rook(0)],
#             [Pawn(1) for x in range(8)],
#             [Empty() for x in range(8)],
#             [Empty() for x in range(8)],
#             [Empty() for x in range(8)],
#             [Empty() for x in range(8)],
#             [Pawn(1) for x in range(8)],
#             [Rook(1), Knight(1), Bishop(1), Queen(1), King(1), Empty(), Empty(), Rook(1)]
#         ]
# print(b.show())
# moves = b.get_moves(*str2coord('c2'), 1)
# print(b.show(moves))
# b.perform_move(moves[0])
# App.change_pawn()
# print(b.show())