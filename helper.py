def deficiency(actual, desired, area):

	required = {}

	for nutrient, value in actual.items():
		# Convert mg/kg to kg/kg - kg/kg to kg/ha 		
		converted = toKilogramPerHectare(toKilogram(value), area)
		# Compute deficiency actual - desired
		deficient = desired[nutrient] - converted
		required.update({ nutrient : round(deficient, 2) })
	
	return required;

def formatNumber(val):
	return '{:.10f}'.format(val).rstrip('0').rstrip('.')

# conver mg/kg to kg/kg
def toKilogram(milligram):
	return (milligram/1000000)

def toKilogramPerHectare(kilogram, area):
	return (kilogram * area)

def fertilizerRecommendation(recommended_levels, fertilizer_grades):

	nutrient_amounts_per_grade = {grade: {nutrient: 0 for nutrient in recommended_levels} for grade in fertilizer_grades}
	total_kg_per_grade = {grade: 0 for grade in fertilizer_grades}

		# Step 1: Calculate amounts from each fertilizer grade
	for grade, percentages in fertilizer_grades.items():
	    for nutrient in recommended_levels:
	        amount_needed = max(0, recommended_levels[nutrient] - nutrient_amounts_per_grade[grade][nutrient])
	        nutrient_amounts_per_grade[grade][nutrient] += min(amount_needed, (percentages[nutrient] / 100) * sum(recommended_levels.values()))
	    # Calculate total kg/ha for the current fertilizer grade
	    total_kg_per_grade[grade] = sum(nutrient_amounts_per_grade[grade].values())

	# Output the total kg/ha for each fertilizer grade and the resulting nutrient amounts
	# print("Total kg/ha for Each Fertilizer Grade:")
	# for grade, total_kg in total_kg_per_grade.items():
	#     print(f"{grade}: {total_kg} kg/ha")
	#     print("Nutrient Amounts (kg/ha):")
	#     for nutrient, amount in nutrient_amounts_per_grade[grade].items():
	#         print(f"  {nutrient}: {amount}")

	deficit = calculateDeficit(recommended_levels, fertilizer_grades, nutrient_amounts_per_grade)
	# print (deficit)

	for grade, percentages in fertilizer_grades.items():
	    for nutrient in recommended_levels:
	        amount_needed = max(0, recommended_levels[nutrient] - nutrient_amounts_per_grade[grade][nutrient])
	        nutrient_amounts_per_grade[grade][nutrient] += min(amount_needed, (percentages[nutrient] / 100) * sum(recommended_levels.values()))
	    # Calculate total kg/ha for the current fertilizer grade
	    total_kg_per_grade[grade] = sum(nutrient_amounts_per_grade[grade].values())

	# Output the total kg/ha for each fertilizer grade and the resulting nutrient amounts
	# print("Total kg/ha for Each Fertilizer Grade:")
	# for grade, total_kg in total_kg_per_grade.items():
	#     print(f"{grade}: {total_kg} kg/ha")
	#     print("Nutrient Amounts (kg/ha):")
	#     for nutrient, amount in nutrient_amounts_per_grade[grade].items():
	#         print(f"  {nutrient}: {amount}")


	deficit = calculateDeficit(recommended_levels, fertilizer_grades, nutrient_amounts_per_grade)
	# print (deficit)
	return deficit, total_kg_per_grade

def calculateDeficit(recommended_levels, fertilizer_grades, nutrient_amounts_per_grade):

	deficiency = {};
	# print("\nDeficit for Each Nutrient:")
	for nutrient in recommended_levels:
	    deficit = recommended_levels[nutrient] - sum(nutrient_amounts_per_grade[grade][nutrient] for grade in fertilizer_grades)
	    deficiency.update({ nutrient: deficit })
	    # print(f"{nutrient}: {deficit} kg/ha")

	return deficiency

def calculateScore(npk):
	score = abs(npk['n']) + abs(npk['p']) + abs(npk['k'])
	return score

# def sortResults(fertilizers):
# 	sorted_npks = sorted(fertilizers.items(), key=lambda x: calculateScore(x[1]))
# 	return sorted_npks

# Define a custom sorting function based on the deficiency values
def custom_sort(item):
    deficiency_values = item[1]['deficient']
    # Return the sum of deficiency values as the sorting key
    return calculateScore(deficiency_values)

def fertility_rating_n(nutrient):

	if nutrient < 2:
		return 'l'

	if nutrient >= 2.1 and nutrient <= 3.5:
		return 'ml'

	if nutrient >= 3.6 and nutrient <= 4.5:
		return 'mh'

	if nutrient >= 4.6 and nutrient <= 5.0:
		return 'h'

	return False

def fertility_rating_p(nutrient):

	if nutrient < 2:
		return 'l'

	if nutrient >= 2.1 and nutrient <= 6.0:
		return 'ml'

	if nutrient >= 6.1 and nutrient <= 10:
		return 'mh'

	if nutrient >= 10.1 and nutrient <= 15.0:
		return 'h'

	return False

def fertility_rating_k(nutrient):
	
	if nutrient < 35:
		return 'l'

	if nutrient >= 36 and nutrient <= 55:
		return 'ml'

	if nutrient >= 56 and nutrient <= 75:
		return 'mh'

	if nutrient >= 76 and nutrient <= 100:
		return 'h'

	return False
