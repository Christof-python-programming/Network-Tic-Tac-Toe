"""
    Description: Simple Network tictactoe game
"""
import tkinter as tk
import threading
import tic_lib
import socket

root = tk.Tk()
root.title('TicTacToe')
root.resizable(0, 0)

lib = tic_lib.PlayGame(root, 399, 'white', 'white')


# erst im nachhinein erstellen -> zuerst zu den Buttons

def destroy_buttons():
    """

    : to destroy the buttons
    """
    button_create_game.destroy()
    button_join_game.destroy()


def create_sever():
    """

    : to create a sever socket and start the game
    """
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)  # to get your local ip address
    print('Your IP is:', local_ip)
    threading.Thread(target=lib.create_sever_socket).start()  # wait for connection and start the game
    tk.Label(root, text='Your IP: ' + str(local_ip), font=('Sans', 12), bg='white').pack(fill='x')
    destroy_buttons()
    # create the game field
    lib.game_canvas.pack()


def create_client():
    """

    : client a client socket and wait for connection to the sever
    """

    # write this function after creating the conntinue button
    def continue_button_f():
        """

        : function for continue button
        """
        ip = ent.get()
        lib.create_client_socket(ip)  # wait for connection and start the game
        # create the game field
        label.config(text='Connected IP:' + str(ip))
        ent.destroy()
        continue_button.destroy()

    destroy_buttons()
    label = tk.Label(root, text='Type the sever IP in', font=('Sans', 12), bg='white')
    label.pack(fill='x')
    ent = tk.Entry(root, font=('Sans', 12))
    ent.pack(fill='x')
    continue_button = tk.Button(root, text='Join', font=('Sans', 12), bg='green', command=continue_button_f)
    continue_button.pack(fill='x')

    lib.game_canvas.pack()


# create this buttons first
button_create_game = tk.Button(root, text='Create Game', font=('Sans', 12), bg='red', width=30,
                               command=create_sever)
button_create_game.pack(fill='x')

button_join_game = tk.Button(root, text='Join Game', font=('Sans', 12), bg='green', width=30,
                             command=create_client)
button_join_game.pack(fill='x')
root.mainloop()
