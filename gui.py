import tkinter
import tkinter.messagebox
import customtkinter
import helper
from itertools import combinations
import data


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Soil Test")
        self.geometry(f"{576}x{360}")
        # self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)
        self.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="NPK Data", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # sidebar start npk reading button
        self.start_reading_btn = customtkinter.CTkButton(self.sidebar_frame, text="Start Reading")
        self.start_reading_btn.grid(row=1, column=0, padx=20, pady=10)
        # sidebar npk label and values
        self.nitrogen_lbl = customtkinter.CTkLabel(self.sidebar_frame, text="Nitrogen:")
        self.nitrogen_lbl.grid(row=2, column=0, padx=0, pady=0, sticky="n")
        self.nitrogen_value_lbl = customtkinter.CTkLabel(self.sidebar_frame, text="0", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.nitrogen_value_lbl.grid(row=3, column=0, padx=0, pady=0, sticky="n")
        self.phosphorus_lbl = customtkinter.CTkLabel(self.sidebar_frame, text="Phosphorus:")
        self.phosphorus_lbl.grid(row=4, column=0, padx=0, pady=0, sticky="n")
        self.phosphorus_value_lbl = customtkinter.CTkLabel(self.sidebar_frame, text="0", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.phosphorus_value_lbl.grid(row=5, column=0, padx=0, pady=0, sticky="n")
        self.potassium_lbl = customtkinter.CTkLabel(self.sidebar_frame, text="Potassium:")
        self.potassium_lbl.grid(row=6, column=0, padx=0, pady=0, sticky="n")
        self.potassium_value_lbl = customtkinter.CTkLabel(self.sidebar_frame, text="0", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.potassium_value_lbl.grid(row=7, column=0, padx=10, pady=0, sticky="n")

        self.send_btn = customtkinter.CTkButton(self, fg_color="transparent", command=self.send, border_width=2, text_color=("gray10", "#DCE4EE"), text="Send")
        self.send_btn.grid(row=3, column=1, padx=(10, 10), pady=(10, 10), sticky="nw")

        # create textbox
        self.rating_lbl = customtkinter.CTkLabel(self, text="Fertility Rating:")
        self.rating_lbl.grid(row=0, column=1, padx=10, pady=0, sticky="nw")

        self.rating_value = customtkinter.CTkLabel(self, text="XX - XX - XX", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.rating_value.grid(row=1, column=1, padx=10, pady=0, sticky="nw")

        self.textbox = customtkinter.CTkTextbox(self, width=380, height=180)
        self.textbox.grid(row=2, column=1, padx=(10, 10), pady=(10, 10))
        self.textbox.insert("0.0", "Recommendation\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

    def sensor_reading():

        # self.start_reading_btn.configure(state="disabled")
        # rating_n = helper.fertility_rating_n(3)
        # rating_p = helper.fertility_rating_p(7)
        # rating_k = helper.fertility_rating_k(32)

        # rating = "%s - %s - %s" %(rating_n, rating_p, rating_k)

        # self.rating_value.configure(text=rating.upper())
        print("Initialize sensor")

    def send(self):
        self.send_btn.configure(state="disabled", text="Sending")
        print('send')


if __name__ == "__main__":

    app = App()
    app.mainloop()