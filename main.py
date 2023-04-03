import tkinter as tk
import random as rand
import datetime as dt


class typingTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.running = False
        self.words_total = 0
        self.correct = 0
        self.incorrect = 0

        self.__word_list = []
        self.__completed_words = []
        self.__text_box = None
        self.__text_input = None
        self.__label_wpm = None
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
        self.words_total += 1
        # check if typed entry is correct
        user_text = self.__text_input.get().strip()
        cur = self.__current_word
        self.__completed_words.append(user_text)  # save user input word for later use
        self.__text_input.delete(0, tk.END)  # clear entry text
        if user_text == self.__word_list[cur]:
            tag = "correct"
            self.correct += 1
        else:
            tag = "incorrect"
            self.incorrect += 1
        self.__highlight_cur_word(tag=tag)
        self.__char_offset += len(self.__word_list[self.__current_word]) + 1
        self.__current_word += 1
        self.__highlight_cur_word()

        # display WPM
        self.__show_wpm()

    def __show_wpm(self):
        time_diff = dt.datetime.now() - self.start_time

        self.__label_wpm.config(text=f"WPM: {(self.correct / time_diff.seconds) * 60 :.0f}")
        print(time_diff.seconds)

    def __highlight_cur_word(self, tag="start"):
        cur = self.__current_word
        self.__text_box.focus()
        self.__text_box.tag_add(tk.SEL, f"1.{self.__char_offset}",
                                f"1.{self.__char_offset + len(self.__word_list[cur])}")
        self.__text_box.see(f"1.{self.__char_offset}")
        self.__text_box.tag_add(tag, f"1.{self.__char_offset}", f"1.{self.__char_offset + len(self.__word_list[cur])}")
        self.__text_input.focus()

    def __initWindow(self):
        # setup window
        window = tk.Tk()
        window.title("Typing Speed Test")
        window.geometry("300x300")
        window.config(padx=20, pady=20)

        # setup speed typing text
        self.__text_box = tk.Text(window, wrap=tk.WORD, height=8, width=32)
        for word in self.__word_list:
            self.__text_box.insert(tk.INSERT, word + " ")  # insert text with spaces
        self.__text_box.config(state=tk.DISABLED)
        self.__text_box.grid(row=0, column=0, rowspan=4)

        # select first word
        # self.__text_box.focus()
        # self.__text_box.tag_add(tk.SEL, "1.0", f"1.{len(self.__word_list[0])}")

        # set tags for highlight, correct, and incorrect
        self.__text_box.tag_config("start", foreground="white", background="black")
        self.__text_box.tag_config("correct", foreground="green", background="white")
        self.__text_box.tag_config("incorrect", foreground="red", background="white")

        # setup text entry
        self.__text_input = tk.Entry(window)
        self.__text_input.bind('<Button-1>', self.__start)
        self.__text_input.bind('<space>', self.__next_word)
        self.__text_input.bind('<Return>', self.__next_word)
        self.__text_input.grid(row=4, column=0, pady=10)

        self.__label_wpm = tk.Label(text="WPM: 0", relief=tk.RAISED)
        self.__label_wpm.grid(row=5, column=0, pady=10)

        button_reset = tk.Button(window, text="Reset", command=self.__reset)
        button_reset.grid(row=6)

        self.__highlight_cur_word()
        self.__text_box.focus()  # bugfix (user needs to click into entry to start timer)

        window.mainloop()

    def __initWordList(self):
        self.__word_list = []
        # load words list
        with open("words.txt", "r") as file:
            self.__word_list = file.readlines()

        # strip newline from all words
        self.__word_list = [word.strip() for word in self.__word_list]

        self.__shuffle_wordlist()

    def __shuffle_wordlist(self):
        # shuffle words list
        old_wordlist = self.__word_list
        new_wordlist = []
        while old_wordlist:
            next_word = str(rand.choice(old_wordlist))
            old_wordlist.remove(next_word)
            new_wordlist.append(next_word)

        self.__word_list = new_wordlist

    def __reset(self):
        # reset all attributes to default
        self.start_time = None
        self.end_time = None
        self.running = False
        self.words_total = 0
        self.correct = 0
        self.incorrect = 0
        self.__completed_words = []
        self.__char_offset = 0
        self.__current_word = 0

        # clear and reset text_box
        self.__text_box.config(state=tk.NORMAL)
        self.__text_box.delete("1.0", "end")

        # shuffle loaded words list
        self.__shuffle_wordlist()

        # fill text box with re-shuffled word list
        for word in self.__word_list:
            self.__text_box.insert(tk.INSERT, word + " ")  # insert text with spaces
        self.__text_box.config(state=tk.DISABLED)

        # highlight first word
        self.__highlight_cur_word()

        self.__text_box.focus()  # bugfix (user needs to click into entry to start timer)

        # set WPM label to 0
        self.__label_wpm.config(text="WPM: 0")


tt = typingTimer()
