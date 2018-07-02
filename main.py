import tkinter as tk
from editor import Editor


def main():
    root = tk.Tk()
    app = Editor(root)
    root.title("Longclaw")
    root.minsize(951,540)
    root.configure()

    root.mainloop()


if __name__ == '__main__':
    main()
