import customtkinter
import customtkinter as ctk

from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

from tkinter import StringVar

from client.api_requests.funcs import api_create_inc


FONT_BOLD = ("Segoe UI", 14, "bold")
FONT = ("Segoe UI", 14)


class CreateIncForm(ctk.CTkToplevel):
    def __init__(self, parent) -> None:
        super().__init__()
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()
        WIDTH = WIDTH // 2
        HEIGHT = HEIGHT // 2
        WIDTH = WIDTH - 200
        HEIGHT = HEIGHT - 200
        self.geometry(f'900x500+{WIDTH}+{HEIGHT}')

        self.parent = parent

        self.resizable(False, False)

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.client = StringVar()

        self.status = StringVar()
        self.topic = StringVar()

        self.topic_label_box =None

        self.draw_widgets()
        self.grab_focus()

    def draw_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=1, fill="both")

        # Row build id
        row_header = ctk.CTkFrame(main_frame)
        row_header.pack(expand=1, fill="both", anchor="n")

        status_label = ctk.CTkLabel(
            row_header,
            text="Статус: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        status_label_box = ctk.CTkComboBox(
            row_header,
            values=["Открыт", "В работе", "Решен"],
            justify="left",
            font=FONT,
            variable=self.status,
        )
        status_label.grid(row=0, column=0, sticky="w", padx=8, pady=8)
        status_label_box.grid(row=0, column=1, sticky="w", padx=8, pady=8)

        title_label = ctk.CTkLabel(
            row_header,
            text="Тема: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        title_label_entry = ctk.CTkEntry(
            row_header,
            justify="left",
            font=FONT,
            textvariable=self.topic,
        )
        title_label.grid(row=1, column=0, sticky="w", padx=8, pady=8)
        title_label_entry.grid(row=1, column=1, sticky="w", padx=8, pady=8)

        topic_label = ctk.CTkLabel(
            row_header,
            text="Описание: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        self.topic_label_box = ctk.CTkTextbox(
            row_header,
            font=FONT,
            width=400,
            height=100
        )
        topic_label.grid(row=2, column=0, sticky="w", padx=8, pady=8)
        self.topic_label_box.grid(row=2, column=1, sticky="w", padx=8, pady=8)

        # Footer
        footer_frame = ctk.CTkFrame(main_frame)
        footer_frame.pack(fill="both")

        create_btn = ctk.CTkButton(
            footer_frame,
            text="Создать",
            command=self.create_inc
        )
        create_btn.grid(row=0, column=3, padx=8, pady=5)

    def create_inc(self):
        key = self.parent.token
        status = self.status.get()
        topic = self.topic.get()
        description = self.topic_label_box.get("0.0", "end")

        if len(status) < 1 or len(topic) < 1 or len(description) < 1:
            showerror(title="Error", message="Fill all fields!")
        else:
            response = api_create_inc(
                token=key,
                status=status,
                topic=topic,
                description=description
            )

            if response["status"] == "ok":
                showinfo(title="Ok", message=response["message"])
                self.parent.grab_set()
                self.withdraw()
                self.parent.deiconify()
            else:
                showerror(title="Error", message=response["message"])

    def grab_focus(self) -> None:
        self.grab_set()
        self.parent.wait_window(self)

    def run_app(self) -> None:
        self.mainloop()


