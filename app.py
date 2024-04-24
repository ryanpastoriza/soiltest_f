import helper
from itertools import combinations
import data
import gui
import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def runAnalysis(recommended_levels, all_combinations):
	groups = {}

	for group in all_combinations:
		f_grades = {}
		for name in group:
			f_grades.update({ name : data.fertilizer_grades[name] })
		fertilizer, total_amount = helper.fertilizerRecommendation(recommended_levels, f_grades)
		groups.update({ group : { 'deficient' : fertilizer, 'required': total_amount } })
	
	return sorted(groups.items(), key=helper.custom_sort)[:1]

def npk_sensor():
	rating_n = helper.fertility_rating_n(3)
	rating_p = helper.fertility_rating_p(7)
	rating_k = helper.fertility_rating_k(32)

	soil_test = { 'n': rating_n, 'p': rating_p , 'k': rating_k }

	recommended_levels = { 
		'wet': {
			'hybrid': { 'n': 0, 'p': 0 , 'k': 0 },
			'inbred': { 'n': 0, 'p': 0 , 'k': 0 },
			'upland': { 'n': 0, 'p': 0 , 'k': 0 },
		},
		'dry': {
			'hybrid': { 'n': 0, 'p': 0 , 'k': 0 },
			'inbred': { 'n': 0, 'p': 0 , 'k': 0 },
			'upland': { 'n': 0, 'p': 0 , 'k': 0 },
		}
	}

	fertility_rating = "%s - %s - %s" %(rating_n, rating_p, rating_k)

	for season, rice_type in data.nutrient_requirements.items():
		for rice, nutrients in rice_type.items():
			for nutrient, rating in nutrients.items():
				for key, val in rating.items():
					if nutrient == 'n':
						if key == soil_test[nutrient]:
							recommended_levels[season][rice][nutrient] = val
					if nutrient == 'p':
						if key == soil_test[nutrient]:
							recommended_levels[season][rice][nutrient] = val
					if nutrient == 'k':
						if key == soil_test[nutrient]:
							recommended_levels[season][rice][nutrient] = val

	all_combinations = []
	for r in range(1, min(4, len(data.fertilizer_grades) + 1)):
	    all_combinations.extend(combinations(data.fertilizer_grades.keys(), r))

	all_crops = {
		'wet': {
			'hybrid': {},
			'inbred': {},
			'upland': {}
		},
		'dry': {
			'hybrid': {},
			'inbred': {},
			'upland': {}
		}
	}

	# Fertilizer Distribution
	for season, varieties in all_crops.items():
		for variety in varieties:
			all_crops[season][variety].update(runAnalysis(recommended_levels[season][variety], all_combinations))

	result = ''
	for season, varieties in all_crops.items():
		result = result + f'-{season.title()} Season-\n'
		for variety in varieties:
			result = result + f'{variety.title()}\nNutrient Requirements\n'
			n = recommended_levels[season][variety]['n']
			p = recommended_levels[season][variety]['p']
			k = recommended_levels[season][variety]['k']
			result = result + f'N:{n} | P:{p} | K:{k} \n'
			for group in all_crops[season][variety].items():
				result = result + f'Fertilizer Recommendation\n'
				# print(group[0])
				# print(group[1]['deficient'])
				# print(group[1]['required'])
				for f, v in group[1]['required'].items():
					bag = v/50
					result = result + f'{f}: {v} = {bag} bag/ha \n'
		result = result + '\n'


	return fertility_rating, result


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
        self.start_reading_btn = customtkinter.CTkButton(self.sidebar_frame, command=self.sensor_reading, text="Start Reading")
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
        # self.textbox.insert("0.0", "Recommendation\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

    def sensor_reading(self):
    	fertility_rating, result = npk_sensor()

    	self.rating_value.configure(text=fertility_rating.upper())
    	self.textbox.insert("0.0", '')
    	self.textbox.insert("0.0", result)

    def send(self):
        self.send_btn.configure(state="disabled", text="Sending")
        print('send')


if __name__ == "__main__":

    app = App()
    app.mainloop()