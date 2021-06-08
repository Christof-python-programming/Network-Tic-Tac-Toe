"""
    Description: A simple library to create a network tictactoe
"""

import tkinter as tk
import threading
import socket


class PlayGame:
    def __init__(self, master, width_height=399, game_canvas_bg='white', button_color='white'):
        """

        :param master: interface (root)
        :param width_height: height and width of the game field
        :param game_canvas_bg: background of the game field
        :param button_color: color of the buttons on the game field
        """
        self.master = master
        self.button_color = button_color
        self.sever_socket = None
        self.client_socket = None
        self.player_x = True
        self.win = False
        self.wait_for_player_status = False
        self.check_list = ['-', '-', '-',
                           '-', '-', '-',
                           '-', '-', '-']

        self.width_height = width_height
        self.button_list = list()
        self.win_list = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.game_canvas = tk.Canvas(master, width=self.width_height, height=self.width_height, bg=game_canvas_bg)
        self.port = 12345

    def create_sever_socket(self):
        """

        : Create a sever socket which waits for a connection to the client
        """
        self.sever_socket = socket.socket()
        self.sever_socket.bind(('', self.port))
        self.sever_socket.listen(1)
        # Establish connection with client.
        self.client_socket, addr = self.sever_socket.accept()
        self._create_game_field()  # create the lines and the buttons on the game canvas

    def create_client_socket(self, ip_address):
        """

        :param ip_address: ip address of the sever socket
        : start the game when connecting was successful
        """
        self.client_socket = socket.socket()
        self.client_socket.connect((ip_address, self.port))
        self._create_game_field()  # create the lines and the buttons on the game canvas

        threading.Thread(target=self.wait_for_player).start()

    def _create_game_field(self):
        """

        : Create the lines and the buttons on the game field
        """
        # for the lines
        line_points = [[0, int(self.width_height / 3), self.width_height, int(self.width_height / 3)],
                       [0, int((self.width_height / 3) * 2), self.width_height, int((self.width_height / 3) * 2)],
                       [int(self.width_height / 3), 0, int(self.width_height / 3), self.width_height],
                       [int((self.width_height / 3) * 2), 0, int((self.width_height / 3) * 2), self.width_height]]

        button_y_points = [5, int(self.width_height / 3) + 5, int((self.width_height / 3) * 2) + 5]

        for x1, y1, x2, y2 in line_points:
            self.game_canvas.create_line((x1, y1), (x2, y2), fill='black', width=4)

        # for the buttons
        button_counter = 0
        for button_row in range(3):
            for button_in_row in range(3):
                button = tk.Button(self.game_canvas, text='-', font=('Sans', 12),
                                   height=int((self.width_height / 30) / 2),
                                   width=int((self.width_height / 30)), bg=self.button_color,
                                   command=lambda index=button_counter: self._button_is_hit(index))
                self.button_list.append(button)
                button.place(x=(self.width_height / 3) * button_in_row + 4, y=button_y_points[button_row])

                button_counter += 1

    def _button_is_hit(self, index):
        """

        :param index: index of the button which is hit (0-8)
        : change the text of the button and send the index to the other player
        """
        if self.wait_for_player_status is False:
            status = self._change_button_status(index)
            if status is False:
                # Example: x want to place on a button which o has already choose
                return  # this is when a player want to place his sign on a field which is already placed
            self.client_socket.send(bytes(str(index), 'utf8'))
            threading.Thread(target=self.wait_for_player).start()

    def _change_button_status(self, button_index):
        """

        :param button_index: index of the button (0-8)
        : change the text of the button
        """
        if self.check_list[button_index] == '-':
            if self.player_x is True:
                self.button_list[button_index].config(text='x')
                self.check_list[button_index] = 'x'
                self.player_x = False
            else:
                self.button_list[button_index].config(text='o')
                self.check_list[button_index] = 'o'
                self.player_x = True
        else:
            return False

        if self.win is False:
            self._check_for_win()

        return True

    def _check_for_win(self):
        """

        : look for all winning cases and put a label on the interface when win is True
        """
        for index1, index2, index3 in self.win_list:
            if self.check_list[index1] == self.check_list[index2] == self.check_list[index3] == 'x':
                tk.Label(self.game_canvas, text='x hat gewonnen', font=('Sans', 20), bg='green',
                         width=int(self.width_height / 15)).place(x=0, y=int(self.width_height / 2))
                self.win = True
            if self.check_list[index1] == self.check_list[index2] == self.check_list[index3] == 'o':
                tk.Label(self.game_canvas, text='o hat gewonnen', font=('Sans', 20), bg='green',
                         width=int(self.width_height / 15)).place(x=0, y=int(self.width_height / 2))
                self.win = True

    def wait_for_player(self):
        """

        : Wait until a other player has chosen a button
        """
        self.wait_for_player_status = True
        received = self.client_socket.recv(1024)
        button_index = int(str(received, 'utf8'))
        self.wait_for_player_status = False
        self._change_button_status(button_index)
