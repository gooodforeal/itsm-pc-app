import tkinter
from tkinter import ttk

import customtkinter
import customtkinter as ctk

from client.forms import build_form, login_from
from client.api_requests.funcs import api_all_builds, api_build, api_all_inc, api_inc

from client.forms import create_build_form, create_inc_form, inc_form


FONT_BOLD = ("Segoe UI", 10, "bold")


class MainForm(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.token = None
        self.style = ttk.Style()
        self.tab_control = None

        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()
        WIDTH = WIDTH // 2
        HEIGHT = HEIGHT // 2
        WIDTH = WIDTH - 200
        HEIGHT = HEIGHT - 200
        self.geometry(f'1200x700+{WIDTH}+{HEIGHT}')

        self.resizable(False, False)

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        login = login_from.LoginForm(parent=self)
        self.withdraw()
        login.deiconify()

    def set_style(self):
        self.style.theme_use("default")
        self.style.configure(
            "Treeview.Heading",
            background="dodgerblue1",
            foreground="white",
            font=('Segoe UI', 12)
        )
        self.style.configure(
            "Treeview",
            fieldbackground="grey20",
            foreground="white",
            background="transparent",
        )
        self.style.map(
            "Treeview",
            background=[("selected", "disabled", "grey"), ("selected", "white")],
            foreground=[("selected", "disabled", "black"), ("selected", "black")]

        )
        self.style.configure('Treeview', rowheight=40)
        self.style.theme_use("default")
        self.style.configure(
            "TNotebook",
            background="grey20",
            tabposition="nw"
        )
        self.style.configure(
            "TNotebook.Tab",
            background="dodgerblue1",
            foreground="white",
            font=('Arial', 10)
        )
        self.style.map(
            "TNotebook",
            background=[("selected", "blue")]
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", "white")],
            foreground=[("selected", "black")]
        )

    def draw_widgets(self):
        # Setting styles
        self.set_style()
        # Tabs Settings
        if self.tab_control is not None:
            self.tab_control.destroy()

        self.tab_control = ttk.Notebook(self)

        tab_builds = ctk.CTkFrame(self.tab_control)
        tab_inc = ctk.CTkFrame(self.tab_control)

        self.tab_control.add(tab_builds, text="Сборки")
        self.tab_control.add(tab_inc, text="Инциденты")

        self.tab_control.pack(expand=1, fill="both")

        builds = api_all_builds(self.token)

        i = 0
        if builds["status"] == "ok":
            x_scroll = ttk.Scrollbar(tab_builds)
            x_scroll.pack(fill="y", side="right")

            columns = ('id', 'Дата', 'Сотрудник', 'Клиент')

            self.table = ttk.Treeview(tab_builds, xscrollcommand=x_scroll, columns=columns, show="headings")

            for col in columns:
                self.table.column(col, anchor="center")
                self.table.heading(col, text=col)

            for build in builds["data"]:
                date = build["created_at"].split(".")[0].replace("T", " ")[:-3]
                self.table.insert(
                    parent='',
                    index='end',
                    iid=i,
                    text='',
                    values=(build["id"],
                            date,
                            build["user"]["fio"],
                            build["client"]["fio"]
                            )
                )
                i += 1
            self.table.pack(fill=tkinter.BOTH, expand=1)

            footer_row = ctk.CTkFrame(tab_builds)
            footer_row.pack(fill="both")

            open_button = ctk.CTkButton(
                footer_row,
                text="Открыть",
                command=self.open_build
            )
            open_button.grid(row=0, column=0, padx=8, pady=5)
            refresh_button = ctk.CTkButton(
                footer_row,
                text="Обновить",
                command=self.draw_widgets
            )
            refresh_button.grid(row=0, column=1, padx=8, pady=5)
            create_button = ctk.CTkButton(
                footer_row,
                text="Создать",
                command=self.create_build
            )
            create_button.grid(row=0, column=2, padx=8, pady=5)
        else:
            error_label = ctk.CTkLabel(
                tab_builds,
                text=builds["message"]
            )
            error_label.pack()

        incs = api_all_inc()

        i = 0
        if incs["status"] == "ok":
            x_scroll1 = ttk.Scrollbar(tab_inc)
            x_scroll1.pack(fill="y", side="right")

            columns1 = ('id', 'Дата', 'Сотрудник', 'Статус', 'Тема')

            self.table1 = ttk.Treeview(tab_inc, xscrollcommand=x_scroll1, columns=columns1, show="headings")

            for col in columns1:
                self.table1.column(col, anchor="center")
                self.table1.heading(col, text=col)

            for inc in incs["data"]:
                date = inc["created_at"].split(".")[0].replace("T", " ")[:-3]
                self.table1.insert(
                    parent='',
                    index='end',
                    iid=i,
                    text='',
                    values=(inc["id"],
                            date,
                            inc["user"]["fio"],
                            inc["status"],
                            inc["topic"]
                    )
                )
                i += 1
            self.table1.pack(fill=tkinter.BOTH, expand=1)

            footer_row1 = ctk.CTkFrame(tab_inc)
            footer_row1.pack(fill="both")

            open_button1 = ctk.CTkButton(
                footer_row1,
                text="Открыть",
                command=self.open_inc
            )
            open_button1.grid(row=0, column=0, padx=8, pady=5)
            refresh_button1 = ctk.CTkButton(
                footer_row1,
                text="Обновить",
                command=self.draw_widgets
            )
            refresh_button1.grid(row=0, column=1, padx=8, pady=5)
            create_button1 = ctk.CTkButton(
                footer_row1,
                text="Создать",
                command=self.create_inc
            )
            create_button1.grid(row=0, column=2, padx=8, pady=5)
        else:
            error_label1 = ctk.CTkLabel(
                tab_inc,
                text=incs["message"]
            )
            error_label1.pack()

    def create_build(self):
        create_form = create_build_form.CreateBuildForm(parent=self)

    def open_build(self):
        current_item = self.table.focus()
        build_id = int(self.table.item(current_item)["values"][0])

        build = api_build(token=self.token, build_id=build_id)

        new_build_form = build_form.BuildForm(parent=self, build=build)

    def create_inc(self):
        create_inc = create_inc_form.CreateIncForm(parent=self)

    def open_inc(self):
        current_item = self.table1.focus()
        inc_id = int(self.table1.item(current_item)["values"][0])

        inc = api_inc(inc_id=str(inc_id))

        new_inc_form = inc_form.IncForm(parent=self, inc=inc)

    def run_app(self) -> None:
        self.mainloop()
