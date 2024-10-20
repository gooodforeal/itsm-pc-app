import customtkinter
import customtkinter as ctk

from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

from client.generate_documents import generate


FONT_BOLD = ("Segoe UI", 14, "bold")
FONT = ("Segoe UI", 14)


class BuildForm(ctk.CTkToplevel):
    def __init__(self, parent, build) -> None:
        super().__init__()
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()
        WIDTH = WIDTH // 2
        HEIGHT = HEIGHT // 2
        WIDTH = WIDTH - 200
        HEIGHT = HEIGHT - 200
        self.geometry(f'900x700+{WIDTH}+{HEIGHT}')

        self.parent = parent
        self.build = build

        self.total = None

        self.resizable(False, False)

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.draw_widgets()
        self.grab_focus()

    def draw_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=1, fill="both")

        if self.build["status"] == "ok":
            # Row build id
            row_header = ctk.CTkFrame(main_frame)
            build_id_label = ctk.CTkLabel(
                row_header,
                text="ID: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            build_id_label_text = ctk.CTkLabel(
                row_header,
                text=self.build["data"][0]["id"],
                justify="left",
                anchor="w",
                font=FONT

            )
            build_id_label.grid(row=0, column=0, sticky="w", padx=8, pady=8)
            build_id_label_text.grid(row=0, column=1, sticky="w", padx=8, pady=8)

            # Row build date
            date = self.build["data"][0]["created_at"].split(".")[0].replace("T", " ")[:-3]
            build_date_label = ctk.CTkLabel(
                row_header,
                text="Дата: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            build_date_label_text = ctk.CTkLabel(
                row_header,
                text=date,
                justify="left",
                anchor="w",
                font=FONT
            )
            build_date_label.grid(row=1, column=0, sticky="w", padx=8, pady=8)
            build_date_label_text.grid(row=1, column=1, sticky="w", padx=8, pady=8)

            # Row build user
            build_user_label = ctk.CTkLabel(
                row_header,
                text="Сотрудник: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            build_user_label_text = ctk.CTkLabel(
                row_header,
                text=self.build["data"][0]["user"]["fio"],
                justify="left",
                anchor="w",
                font=FONT
            )
            build_user_label.grid(row=2, column=0, sticky="w", padx=8, pady=8)
            build_user_label_text.grid(row=2, column=1, sticky="w", padx=8, pady=8)

            # Row build client
            build_client_label = ctk.CTkLabel(
                row_header,
                text="Клиент: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            build_client_label_text = ctk.CTkLabel(
                row_header,
                text=self.build["data"][0]["client"]["fio"],
                justify="left",
                anchor="w",
                font=FONT
            )
            build_client_label.grid(row=3, column=0, sticky="w", padx=8, pady=8)
            build_client_label_text.grid(row=3, column=1, sticky="w", padx=8, pady=8)

            # Components
            build_components_label = ctk.CTkLabel(
                row_header,
                text="Компоненты: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            build_components_label.grid(row=4, column=0, sticky="w", padx=8, pady=8)
            row_header.pack(expand=1, fill="both", anchor="n")

            x_scroll = ttk.Scrollbar(main_frame)
            x_scroll.pack(fill="y", side="right")

            columns = ('Номер', 'Название', 'Тип', 'Цена')

            self.table = ttk.Treeview(main_frame, xscrollcommand=x_scroll, columns=columns, show="headings")

            for col in columns:
                self.table.column(col, anchor="center")
                self.table.heading(col, text=col)

            i = 1
            for comp in self.build["data"][0]["components_replied"]:
                self.table.insert(
                    parent='',
                    index='end',
                    iid=i,
                    text='',
                    values=(str(i),
                            comp["name"],
                            comp["type"],
                            comp["price"]
                    )
                )
                i += 1
            self.table.pack(fill="both", expand=1)

            # Footer
            self.total = sum([comp["price"] for comp in self.build["data"][0]["components_replied"]])

            footer_frame = ctk.CTkFrame(main_frame)
            footer_frame.pack(fill="both")

            total_label = ctk.CTkLabel(
                footer_frame,
                text="Итого: ",
                font=FONT_BOLD
            )
            total_label.grid(row=0, column=0, padx=8, pady=5)
            total_label_text = ctk.CTkLabel(
                footer_frame,
                text=str(self.total) + " Руб",
                font=FONT
            )
            total_label_text.grid(row=0, column=1, padx=8, pady=5)

            make_document_btn = ctk.CTkButton(
                footer_frame,
                text="Создать накладную",
                command=self.make_document
            )
            make_document_btn.grid(row=0, column=3, padx=8, pady=5)
        else:
            error_label = ctk.CTkLabel(
                main_frame,
                text=self.build["message"]
            )
            error_label.pack()

    def make_document(self):
        result = generate.generate(self.build, self.total)
        if result["status"] == "ok":
            showinfo(title="Success", message=f'{result["message"]} {result["data"]}')
        else:
            showerror(title="Success", message=result["message"])

    def grab_focus(self) -> None:
        self.grab_set()
        self.parent.wait_window(self)

    def run_app(self) -> None:
        self.mainloop()


