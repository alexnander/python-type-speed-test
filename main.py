import tkinter as tk
import random as rand
import datetime as dt


class typingTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.running = False
        self.words_total = 0

        self.__word_list = []
        self.__completed_words = []
        self.__text_box = None
        self.__text_input = None
        self.__char_offset = 0
        self.__current_word = 0

        # init words list
        # show window
        self.__initWordList()
        self.__initWindow()

    def __start(self, event):
        if not self.running:
            self.running = True
            self.start_time = dt.datetime.now()

        print(self.start_time)

    def __next_word(self, event):
        self.__highlight_cur_word(undo=True)
        self.__char_offset += len(self.__word_list[self.__current_word]) + 1
        self.__current_word += 1
        self.__highlight_cur_word()
        print(self.__char_offset)

    def __highlight_cur_word(self, undo=False):
        cur = self.__current_word
        self.__text_box.focus()
        self.__text_box.tag_add(tk.SEL, f"1.{self.__char_offset}", f"1.{self.__char_offset + len(self.__word_list[cur])}")
        if undo:
            tag = "undo"
        else:
            tag = "start"
        self.__text_box.see(f"1.{self.__char_offset}")
        self.__text_box.tag_add(tag, f"1.{self.__char_offset}", f"1.{self.__char_offset + len(self.__word_list[cur])}")
        self.__text_input.focus()

    def __initWindow(self):
        # setup window
        window = tk.Tk()
        window.geometry("300x300")
        window.config(padx=20, pady=20)

        # setup speed typing text
        self.__text_box = tk.Text(window, wrap=tk.WORD, height=8, width=32)
        for word in self.__word_list:
            self.__text_box.insert(tk.INSERT, word + " ")  # insert text with spaces
        self.__text_box.config(state=tk.DISABLED)
        self.__text_box.grid(row=0, column=0, rowspan=4)

        # select first word
        self.__text_box.focus()
        self.__text_box.tag_add(tk.SEL, "1.0", f"1.{len(self.__word_list[0])}")
        self.__text_box.tag_config("start", foreground="white", background="black")
        self.__text_box.tag_config("undo", foreground="black", background="white")

        # setup text entry
        self.__text_input = tk.Entry(window)
        self.__text_input.bind('<Button-1>', self.__start)
        self.__text_input.bind('<space>', self.__next_word)
        self.__text_input.bind('<Return>', self.__next_word)
        self.__text_input.grid(row=4, column=0, pady=10)

        self.__highlight_cur_word()

        window.mainloop()

    def __initWordList(self):
        self.__word_list = []
        # load words list
        with open("words.txt", "r") as file:
            new_words_list = file.readlines()

        # shuffle words list
        while new_words_list:
            next_word = str(rand.choice(new_words_list))
            new_words_list.remove(next_word)
            self.__word_list.append(next_word.strip())


tt = typingTimer()
