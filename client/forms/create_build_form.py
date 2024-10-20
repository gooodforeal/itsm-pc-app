import customtkinter
import customtkinter as ctk

from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

from tkinter import StringVar

from client.api_requests.funcs import api_get_clients, api_get_components, api_create_build


FONT_BOLD = ("Segoe UI", 14, "bold")
FONT = ("Segoe UI", 14)


class CreateBuildForm(ctk.CTkToplevel):
    def __init__(self, parent) -> None:
        super().__init__()
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()
        WIDTH = WIDTH // 2
        HEIGHT = HEIGHT // 2
        WIDTH = WIDTH - 200
        HEIGHT = HEIGHT - 200
        self.geometry(f'900x700+{WIDTH}+{HEIGHT}')

        self.parent = parent

        self.total = None

        self.resizable(False, False)

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.client = StringVar()

        self.variables = {
            "Видеокарта": StringVar(),
            "Процессор": StringVar(),
            "Оперативная память": StringVar(),
            "Материнская плата": StringVar(),
            "Блок питания": StringVar(),
            "SSD": StringVar(),
            "HDD": StringVar(),
            "Кулер": StringVar(),
            "Системный блок": StringVar(),
        }

        self.draw_widgets()
        self.grab_focus()

    def draw_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=1, fill="both")

        components = api_get_components()
        clients = api_get_clients()

        if components["status"] == "ok" and clients["status"] == "ok":
            clients = [client["fio"] for client in clients["data"]]

            # Row build id
            row_header = ctk.CTkFrame(main_frame)
            row_header.pack(expand=1, fill="both", anchor="n")

            client_label = ctk.CTkLabel(
                row_header,
                text="Клиент: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            client_label_box = ctk.CTkComboBox(
                row_header,
                values=clients,
                justify="left",
                font=FONT,
                variable=self.client,
                width=300

            )
            client_label.grid(row=0, column=0, sticky="w", padx=8, pady=8)
            client_label_box.grid(row=0, column=1, sticky="w", padx=8, pady=8)

            i = 1
            for component in self.variables.keys():

                components_types = [comp["name"] for comp in components["data"] if comp["type"] == component]

                component_label = ctk.CTkLabel(
                    row_header,
                    text=f"{component}: ",
                    justify="left",
                    anchor="w",
                    font=FONT_BOLD
                )
                component_label_box = ctk.CTkComboBox(
                    row_header,
                    values=components_types,
                    justify="left",
                    font=FONT,
                    variable=self.variables[component],
                    width=300

                )
                component_label.grid(row=i, column=0, sticky="w", padx=8, pady=8)
                component_label_box.grid(row=i, column=1, sticky="w", padx=8, pady=8)
                i += 1

            # Footer
            footer_frame = ctk.CTkFrame(main_frame)
            footer_frame.pack(fill="both")

            create_btn = ctk.CTkButton(
                footer_frame,
                text="Создать",
                command=self.create_build
            )
            create_btn.grid(row=0, column=3, padx=8, pady=5)
        else:
            error_label = ctk.CTkLabel(
                main_frame,
                text=components["message"]
            )
            error_label.pack()

    def create_build(self):
        key = self.parent.token
        client = self.client.get()
        components = [el.get() for el in self.variables.values()]

        if len(client) <= 1 or any([len(comp) <= 1 for comp in components]):
            showerror(title="Error", message="Fill all fields!")

        response = api_create_build(key, client, components)

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


