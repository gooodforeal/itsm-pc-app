import customtkinter
import customtkinter as ctk

from tkinter import ttk, StringVar
from tkinter.messagebox import showerror, showinfo

from client.api_requests.funcs import api_edit_inc


FONT_BOLD = ("Segoe UI", 14, "bold")
FONT = ("Segoe UI", 14)


class IncForm(ctk.CTkToplevel):
    def __init__(self, parent, inc) -> None:
        super().__init__()
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()
        WIDTH = WIDTH // 2
        HEIGHT = HEIGHT // 2
        WIDTH = WIDTH - 200
        HEIGHT = HEIGHT - 200
        self.geometry(f'900x700+{WIDTH}+{HEIGHT}')

        self.parent = parent
        self.inc = inc

        self.resizable(False, False)

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.status = StringVar()

        self.draw_widgets()
        self.grab_focus()

    def draw_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=1, fill="both")

        if self.inc["status"] == "ok":
            # Row build id
            row_header = ctk.CTkFrame(main_frame)
            row_header.pack(expand=1, fill="both", anchor="n")

            id_label = ctk.CTkLabel(
                row_header,
                text="ID: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            id_label_text = ctk.CTkLabel(
                row_header,
                text=self.inc["data"]["id"],
                justify="left",
                anchor="w",
                font=FONT

            )
            id_label.grid(row=0, column=0, sticky="w", padx=8, pady=8)
            id_label_text.grid(row=0, column=1, sticky="w", padx=8, pady=8)

            date_label = ctk.CTkLabel(
                row_header,
                text="Дата: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            date_label_text = ctk.CTkLabel(
                row_header,
                text=self.inc["data"]["created_at"].split(".")[0].replace("T", " ")[:-3],
                justify="left",
                anchor="w",
                font=FONT
            )
            date_label.grid(row=1, column=0, sticky="w", padx=8, pady=8)
            date_label_text.grid(row=1, column=1, sticky="w", padx=8, pady=8)

            status_label = ctk.CTkLabel(
                row_header,
                text="Статус: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            self.status.set(self.inc["data"]["status"])
            status_label_text = ctk.CTkComboBox(
                row_header,
                values=["Открыт", "В работе", "Решен"],
                font=FONT,
                variable=self.status
            )
            status_label.grid(row=2, column=0, sticky="w", padx=8, pady=8)
            status_label_text.grid(row=2, column=1, sticky="w", padx=8, pady=8)

            topic_label = ctk.CTkLabel(
                row_header,
                text="Тема: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            topic_label_text = ctk.CTkLabel(
                row_header,
                text=self.inc["data"]["topic"],
                justify="left",
                anchor="w",
                font=FONT

            )
            topic_label.grid(row=3, column=0, sticky="w", padx=8, pady=8)
            topic_label_text.grid(row=3, column=1, sticky="w", padx=8, pady=8)

            desc_label = ctk.CTkLabel(
                row_header,
                text="Описание: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            desc_label_text = ctk.CTkLabel(
                row_header,
                text=self.inc["data"]["description"].strip(),
                justify="left",
                anchor="w",
                font=FONT

            )
            desc_label.grid(row=4, column=0, sticky="w", padx=8, pady=8)
            desc_label_text.grid(row=4, column=1, sticky="w", padx=8, pady=8)

            user_label = ctk.CTkLabel(
                row_header,
                text="Сотрудник: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            user_label_text = ctk.CTkLabel(
                row_header,
                text=self.inc["data"]["user"]["fio"],
                justify="left",
                anchor="w",
                font=FONT

            )
            user_label.grid(row=5, column=0, sticky="w", padx=8, pady=8)
            user_label_text.grid(row=5, column=1, sticky="w", padx=8, pady=8)

            footer_frame = ctk.CTkFrame(main_frame)
            footer_frame.pack(fill="both")

            edit_btn = ctk.CTkButton(
                footer_frame,
                text="Ok",
                command=self.inc_edit
            )
            edit_btn.grid(row=0, column=0, padx=8, pady=5)
        else:
            error_label = ctk.CTkLabel(
                main_frame,
                text=self.inc["message"]
            )
            error_label.pack()

    def inc_edit(self):
        response = api_edit_inc(incident_id=int(self.inc["data"]["id"]), incident_status=self.status.get())
        if response["status"] == "ok":
            showinfo(title="Success", message=f'{response["message"]}')
            self.parent.grab_set()
            self.withdraw()
            self.parent.deiconify()
        else:
            showerror(title="Success", message=response["message"])

    def grab_focus(self) -> None:
        self.grab_set()
        self.parent.wait_window(self)

    def run_app(self) -> None:
        self.mainloop()


