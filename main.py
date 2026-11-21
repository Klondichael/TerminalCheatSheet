from tkinter import *
from pathlib import Path

root = Tk()

root.geometry("500x300")
root.title("Terminal Cheat Sheet")

CHEATS_FILE = Path("cheats.local.txt")
CHEATS_TEMPLATE = Path("cheats.txt")

cheats = []

class Cheat:
    def __init__(self, index, text=None):
        self.index = index
        self.text_box = Text(root, height=1, width=30)
        self.text_box.grid(row=index, column=0)
        self.copy_button = Button(
            root,
            text="Copy",
            command=self.copy_to_clipboard
        )
        self.copy_button.grid(row=index, column=1)
        self.delete_button = Button(
            root,
            text="Delete",
            command=self.delete_cheat
        )
        self.delete_button.grid(row=index, column=2)
        if text is not None:
            self.text_box.insert(END, text)

    def copy_to_clipboard(self):
        text_to_copy = self.text_box.get("1.0", "end-1c")
        if text_to_copy:
            root.clipboard_clear()  # Clear existing clipboard content
            root.clipboard_append(text_to_copy)  # Add new text
            root.update()  # Refresh clipboard

    def delete_cheat(self):
        with open(CHEATS_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()  # read all lines
        with open(CHEATS_FILE, "w", encoding="utf-8") as file:
            for row, line in enumerate(lines):
                if row != self.index:
                    file.write(line)
        cheats.remove(self)
        self.update_cheats()

    def update_cheats(self):
        for cheat in cheats:
            cheat.index = cheats.index(cheat)
            cheat.text_box.grid(row=cheat.index, column=0)
            cheat.copy_button.grid(row=cheat.index, column=1)
            cheat.delete_button.grid(row=cheat.index, column=2)

def save_cheats():
    lines = [
        cheat.text_box.get("1.0", "end-1c")
        for cheat in cheats
    ]

    with open(CHEATS_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

def add_cheat(text=None):
    global cheats
    global save_btn
    global add_btn
    cheats.append(Cheat(len(cheats), text))
    print(len(cheats))
    save_btn.grid(row=len(cheats), column=0)
    add_btn.grid(row=len(cheats), column=1)

def load_cheats():
    if not CHEATS_FILE.exists():
        CHEATS_FILE.write_text(
            CHEATS_TEMPLATE.read_text(encoding="utf-8"),
            encoding="utf-8"
        )

    with open(CHEATS_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                add_cheat(line.rstrip("\r\n"))

save_btn = Button(root, text="Save", command=save_cheats)
save_btn.grid(row=len(cheats), column=0)

add_btn = Button(root, text="Add New Cheat", command=add_cheat)
add_btn.grid(row=len(cheats), column=1)

load_cheats()

root.mainloop()