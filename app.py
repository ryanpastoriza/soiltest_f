import helper
from itertools import combinations
import data


def runAnalysis(recommended_levels):
	groups = {}

	for group in all_combinations:
		f_grades = {}
		for name in group:
			f_grades.update({ name : data.fertilizer_grades[name] })
		fertilizer, total_amount = helper.fertilizerRecommendation(recommended_levels, f_grades)
		groups.update({ group : { 'deficient' : fertilizer, 'required': total_amount } })
	
	return sorted(groups.items(), key=helper.custom_sort)[:2]


if __name__ == "__main__":

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

	print(f'Rating: {rating_n} - {rating_p} - {rating_k}')

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

	for season, varieties in all_crops.items():
		print(season)
		for variety in varieties:
			all_crops[season][variety].update(runAnalysis(recommended_levels[season][variety]))


	for season, varieties in all_crops.items():
		print(season)
		for variety in varieties:
			print(variety)
			print(all_crops[season][variety])
			print()
