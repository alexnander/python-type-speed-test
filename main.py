import tkinter as tk
import random as rand


def wordsList():
    # load words list
    with open("words.txt", "r") as file:
        words_list = file.readlines()

    # shuffle words list
    new_words_list = []
    while words_list:
        next_word = str(rand.choice(words_list))
        words_list.remove(next_word)
        new_words_list.append(next_word.strip())

    return new_words_list


word_list = wordsList()

window = tk.Tk()

window.geometry("300x300")

text = tk.Text(window)

window.mainloop()
