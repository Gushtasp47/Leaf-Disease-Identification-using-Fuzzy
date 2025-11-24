import numpy as np
from skfuzzy import control as ctrl
import skfuzzy as fuzz

# Mapping dictionaries (categorical → numeric centers)
# color_map = {
#     'brown_tips': 0.5, 'black': 1.5, 'brown': 2.5, 'dark_brown': 3.5,
#     'pale_green': 4.5, 'brownish': 5.5, 'yellowish': 6.0,
#     'yellow_veins': 6.5, 'mosaic_pattern': 7 , 'yellow_green': 7.5,
#     'gray': 8 , 'blackish': 1.7, 'reddish_orange': 2.8,
#     'blackish_brown': 3.2, 'grayish_brown': 3.8, 'pale_yellow': 6.8,
#     'whitish': 9 , 'yellow_brown': 4 
# }
# ordered the colors in a more logical sequence
color_map = {
    'pale_green': 0.5, 'yellow_green': 1, 'yellowish': 1.5, 'pale_yellow': 2,
    'yellow_veins': 2.5, 'mosaic_pattern': 3, 'whitish': 3.5, 'yellow_brown': 4,
    'brown_tips': 4.5, 'brownish': 5, 'brown': 5.5, 'reddish_orange': 6, 'blackish_brown':6.5, 'dark_brown': 7,
    'grayish_brown': 7.5, 'brown_tips': 8, 'blackish': 8.5, 'black': 9, 'gray': 9.5
}
shape_map = {
    'elongated': 1 , 'circular': 2 , 'irregular': 3 ,
    'angular': 4 , 'blister_like': 5 , 'small_raised': 6 
}

# texture_map = {
#     'dry': 1 , 'greasy': 2 , 'water_soaked': 3 ,
#     'smooth': 4 , 'rough': 5 , 'velvety': 6 ,
#     'powdery': 7 , 'downy': 8 , 'rough': 5 
# }
# rearranged texture map for a more natural order
texture_map = {
    'smooth': 1,  'velvety': 1.5, 'downy': 2, 'powdery': 2.5,
    'rough': 3, 'dry': 4, 'water_soaked':4, 'greasy':4.5
}

curl_map = {
    'none': 0.5, 'slight': 2 , 'mild': 4 ,
    'moderate': 6 , 'severe': 8 
}

necrosis_map = {'none': 0.5, 'low': 1.5, 'moderate': 2 , 'high': 3}
defoliation_map = {'low': 2.5, 'moderate': 5 , 'high': 7.5}
temp_map = {'cool': 1 , 'mild': 2 , 'warm': 2.5, 'hot': 3.5}
humidity_map = {'low': 1 , 'moderate': 2 , 'high': 3 }
sunlight_map = {'low': 1 , 'moderate': 2 , 'high': 3 }


# Declare fuzzy variables
univ = np.arange(0, 10.01, 0.01)
univ_out = np.arange(0, 101, 1)

color = ctrl.Antecedent(univ, "color")
shape = ctrl.Antecedent(univ, "shape")
texture = ctrl.Antecedent(univ, "texture")
curl = ctrl.Antecedent(univ, "curl")
necrosis = ctrl.Antecedent(univ, "necrosis")
defoliation = ctrl.Antecedent(univ, "defoliation")
temperature = ctrl.Antecedent(univ, "temperature")
humidity = ctrl.Antecedent(univ, "humidity")
sunlight = ctrl.Antecedent(univ, "sunlight")

diseases = ctrl.Consequent(univ_out, "disease")


#Create membership functions automatically
def add_label_mfs(antecedent, label_map, width=1.0):
    for label, center in label_map.items():
        c = float(center)
        left = max(0.0, c - width)
        right = min(10.0, c + width)
        antecedent[label] = fuzz.trimf(antecedent.universe, [left, c, right])


add_label_mfs(color, color_map, 1.0)
add_label_mfs(shape, shape_map, 0.5)
add_label_mfs(texture, texture_map, 0.8)
add_label_mfs(curl, curl_map, 1.0)
add_label_mfs(necrosis, necrosis_map, 1.2)
add_label_mfs(defoliation, defoliation_map, 1.2)
add_label_mfs(temperature, temp_map, 1.2)
add_label_mfs(humidity, humidity_map, 1.2)
add_label_mfs(sunlight, sunlight_map, 1.2)

#Create disease membership functions
disease_labels = [
    'Tip_Burn', 'Black_Spot', 'Shot_Hole', 'Helminthosporium_Blight', 'Blister_Blight',
    'Leaf_Scorch', 'Chlorosis', 'Yellow_Vein_Mosaic', 'Mosaic_Virus', 'Leaf_Curl_Virus',
    'Bacterial_Blight_Cotton', 'Angular_Leaf_Spot', 'Bacterial_Pustule',
    'Bacterial_Leaf_Spot', 'Bacterial_Leaf_Blight', 'Fusarium_Blight',
    'Septoria_Leaf_Spot', 'Botrytis_Blight', 'Sooty_Mold', 'Rust', 'Anthracnose',
    'Cercospora_Leaf_Spot', 'Leaf_Spot', 'Downy_Mildew', 'Powdery_Mildew'
]

centers = np.linspace(2, 98, len(disease_labels))
for lbl, c in zip(disease_labels, centers):
    diseases[lbl] = fuzz.trimf(diseases.universe, [c - 3, c, c + 3])

#Helper for building rules
label_lookup = {
    'color': color, 'shape': shape, 'texture': texture, 'curl': curl,
    'necrosis': necrosis, 'defoliation_severity': defoliation,
    'temperature': temperature, 'humidity': humidity, 'sunlight': sunlight
}


def A(var_name, label):
    """Return Antecedent[label], creating a fallback MF if needed."""
    if var_name == 'defoliation':
        var_name = 'defoliation_severity'

    # this was needed in the earlier testing
    # if var_name not in label_lookup:
    #     raise KeyError(f"Unknown antecedent: {var_name}")

    var = label_lookup[var_name]

    if label not in var.terms:
        # Fallback: create very narrow MF near neutral
        # var[label] = fuzz.trimf(var.universe, [4.9, 5.0, 5.1])
        raise KeyError("missing values")

    return var[label]


rules = []
def R(*conditions, disease_name):
    rules.append(ctrl.Rule(conditions[0] & conditions[1] & conditions[2] &
                           conditions[3] & conditions[4] & conditions[5] &
                           conditions[6] & (conditions[7] if len(conditions) > 7 else True),
                           diseases[disease_name]))

# Rule 1: Tip_Burn
rules.append(ctrl.Rule(
    A('color', 'brown_tips') & A('shape', 'elongated') & A('texture', 'dry') &
    A('necrosis', 'high') & A('defoliation_severity', 'low') &
    A('temperature', 'hot') & A('humidity', 'low') & A('sunlight', 'high'),
    diseases['Tip_Burn']
))

# Rule 2: Black_Spot
rules.append(ctrl.Rule(
    A('color', 'black') & A('shape', 'circular') & A('texture', 'dry') &
    A('necrosis', 'high') & A('defoliation_severity', 'high') &
    A('temperature', 'mild') & A('humidity', 'high') & A('sunlight', 'low'),
    diseases['Black_Spot']
))

# Rule 3: Shot_Hole
rules.append(ctrl.Rule(
    A('color', 'brown') & A('shape', 'circular') & A('texture', 'dry') &
    A('necrosis', 'high') & A('defoliation_severity', 'moderate') &
    A('temperature', 'mild') & A('humidity', 'moderate'),
    diseases['Shot_Hole']
))

# Rule 4: Helminthosporium_Blight
rules.append(ctrl.Rule(
    A('color', 'dark_brown') & A('shape', 'elongated') & A('texture', 'dry') &
    A('necrosis', 'high') & A('defoliation_severity', 'high') &
    A('temperature', 'warm') & A('humidity', 'high'),
    diseases['Helminthosporium_Blight']
))

# Rule 5: Blister_Blight
rules.append(ctrl.Rule(
    A('color', 'pale_green') & A('shape', 'blister_like') & A('texture', 'smooth') &
    A('necrosis', 'low') & A('humidity', 'high') & A('temperature', 'mild'),
    diseases['Blister_Blight']
))

# Rule 6: Leaf_Scorch
rules.append(ctrl.Rule(
    A('color', 'brown') & A('shape', 'irregular') & A('necrosis', 'high') &
    A('defoliation_severity', 'high') & A('temperature', 'hot') &
    A('sunlight', 'high') & A('humidity', 'low'),
    diseases['Leaf_Scorch']
))

# Rule 7: Chlorosis
rules.append(ctrl.Rule(
    A('color', 'yellowish') & A('texture', 'smooth') & A('necrosis', 'none') &
    A('defoliation_severity', 'low') & A('temperature', 'mild') &
    A('humidity', 'moderate'),
    diseases['Chlorosis']
))

# Rule 8: Yellow_Vein_Mosaic
rules.append(ctrl.Rule(
    A('color', 'yellow_veins') & A('texture', 'smooth') & A('curl', 'mild') &
    A('necrosis', 'low') & A('temperature', 'warm') & A('humidity', 'moderate') &
    A('sunlight', 'high'),
    diseases['Yellow_Vein_Mosaic']
))

# Rule 9: Mosaic_Virus
rules.append(ctrl.Rule(
    A('color', 'mosaic_pattern') & A('texture', 'smooth') & A('curl', 'mild') &
    A('necrosis', 'low') & A('temperature', 'warm') & A('humidity', 'moderate'),
    diseases['Mosaic_Virus']
))

# Rule 10: Leaf_Curl_Virus
rules.append(ctrl.Rule(
    A('color', 'yellow_green') & A('curl', 'severe') & A('necrosis', 'low') &
    A('defoliation_severity', 'low') & A('temperature', 'warm') &
    A('humidity', 'moderate') & A('sunlight', 'high'),
    diseases['Leaf_Curl_Virus']
))

# Rule 11: Bacterial_Blight_Cotton
rules.append(ctrl.Rule(
    A('color', 'dark_brown') & A('texture', 'greasy') & A('curl', 'moderate') &
    A('necrosis', 'high') & A('defoliation_severity', 'high') &
    A('temperature', 'warm') & A('humidity', 'high'),
    diseases['Bacterial_Blight_Cotton']
))

# Rule 12: Angular_Leaf_Spot
rules.append(ctrl.Rule(
    A('color', 'brown') & A('shape', 'angular') & A('texture', 'water_soaked') &
    A('necrosis', 'moderate') & A('defoliation_severity', 'moderate') &
    A('temperature', 'warm') & A('humidity', 'high') & A('sunlight', 'low'),
    diseases['Angular_Leaf_Spot']
))

# Rule 13: Bacterial_Pustule
rules.append(ctrl.Rule(
    A('color', 'pale_yellow') & A('shape', 'small_raised') & A('texture', 'rough') &
    A('necrosis', 'low') & A('defoliation_severity', 'low') &
    A('temperature', 'warm') & A('humidity', 'moderate'),
    diseases['Bacterial_Pustule']
))

# Rule 14: Bacterial_Leaf_Spot
rules.append(ctrl.Rule(
    A('color', 'yellow_brown') & A('shape', 'angular') & A('texture', 'greasy') &
    A('necrosis', 'moderate') & A('defoliation_severity', 'low') &
    A('temperature', 'warm') & A('humidity', 'high'),
    diseases['Bacterial_Leaf_Spot']
))

# Rule 15: Bacterial_Leaf_Blight
rules.append(ctrl.Rule(
    A('color', 'yellowish') & A('texture', 'water_soaked') & A('shape', 'irregular') &
    A('necrosis', 'moderate') & A('defoliation_severity', 'moderate') &
    A('temperature', 'warm') & A('humidity', 'high') & A('sunlight', 'moderate'),
    diseases['Bacterial_Leaf_Blight']
))

# Rule 16: Fusarium_Blight
rules.append(ctrl.Rule(
    A('color', 'brownish') & A('shape', 'irregular') & A('texture', 'dry') &
    A('necrosis', 'high') & A('defoliation_severity', 'high') &
    A('temperature', 'warm') & A('humidity', 'moderate') & A('sunlight', 'high'),
    diseases['Fusarium_Blight']
))

# Rule 17: Septoria_Leaf_Spot
rules.append(ctrl.Rule(
    A('color', 'dark_brown') & A('shape', 'angular') & A('texture', 'dry') &
    A('necrosis', 'high') & A('defoliation_severity', 'moderate') &
    A('temperature', 'mild') & A('humidity', 'high') & A('sunlight', 'low'),
    diseases['Septoria_Leaf_Spot']
))

# Rule 18: Botrytis_Blight
rules.append(ctrl.Rule(
    A('color', 'gray') & A('texture', 'velvety') & A('necrosis', 'moderate') &
    A('defoliation_severity', 'high') & A('temperature', 'cool') &
    A('humidity', 'high') & A('sunlight', 'low'),
    diseases['Botrytis_Blight']
))

# Rule 19: Sooty_Mold
rules.append(ctrl.Rule(
    A('color', 'blackish') & A('texture', 'greasy') & A('curl', 'none') &
    A('necrosis', 'low') & A('defoliation_severity', 'low') &
    A('humidity', 'high') & A('sunlight', 'low'),
    diseases['Sooty_Mold']
))

# Rule 20: Rust
rules.append(ctrl.Rule(
    A('color', 'reddish_orange') & A('texture', 'powdery') & A('shape', 'circular') &
    A('necrosis', 'moderate') & A('defoliation_severity', 'moderate') &
    A('temperature', 'mild') & A('humidity', 'moderate') & A('sunlight', 'high'),
    diseases['Rust']
))

# Rule 21: Anthracnose
rules.append(ctrl.Rule(
    A('color', 'blackish_brown') & A('shape', 'irregular') & A('texture', 'rough') &
    A('necrosis', 'high') & A('defoliation_severity', 'high') &
    A('temperature', 'warm') & A('humidity', 'high') & A('sunlight', 'moderate'),
    diseases['Anthracnose']
))

# Rule 22: Cercospora_Leaf_Spot
rules.append(ctrl.Rule(
    A('color', 'grayish_brown') & A('shape', 'circular') & A('texture', 'dry') &
    A('necrosis', 'moderate') & A('curl', 'none') & A('humidity', 'high') &
    A('temperature', 'mild') & A('sunlight', 'low'),
    diseases['Cercospora_Leaf_Spot']
))

# Rule 23: Leaf_Spot
rules.append(ctrl.Rule(
    A('color', 'dark_brown') & A('shape', 'circular') & A('texture', 'rough') &
    A('necrosis', 'moderate') & A('defoliation_severity', 'high') &
    A('temperature', 'mild') & A('humidity', 'high') & A('sunlight', 'moderate'),
    diseases['Leaf_Spot']
))

# Rule 24: Downy_Mildew
rules.append(ctrl.Rule(
    A('color', 'pale_yellow') & A('texture', 'downy') & A('curl', 'slight') &
    A('necrosis', 'moderate') & A('defoliation_severity', 'low') &
    A('temperature', 'mild') & A('humidity', 'high') & A('sunlight', 'low'),
    diseases['Downy_Mildew']
))

# Rule 25: Powdery_Mildew
rules.append(ctrl.Rule(
    A('color', 'whitish') & A('texture', 'powdery') & A('curl', 'mild') &
    A('necrosis', 'low') & A('defoliation_severity', 'moderate') &
    A('temperature', 'mild') & A('humidity', 'moderate') & A('sunlight', 'low'),
    diseases['Powdery_Mildew']
))

#Control system
system = ctrl.ControlSystem(rules)

def diagnose(inputs):
    # Check if all inputs are missing or invalid
    all_none = True
    for var, mapping in [
        ('color', color_map),
        ('shape', shape_map),
        ('texture', texture_map),
        ('curl', curl_map),
        ('necrosis', necrosis_map),
        ('defoliation_severity', defoliation_map),
        ('temperature', temp_map),
        ('humidity', humidity_map),
        ('sunlight', sunlight_map)
    ]:
        val = inputs.get(var)
        if val in mapping:
            all_none = False
            break
    # also for the testing phase
    # if all_none:
    #     return "Unknown", {lbl: 0 for lbl in disease_labels}

    # fuzzy computation
    sim = ctrl.ControlSystemSimulation(system)

    def set_if(varname, mapping, simvar):
        val = inputs.get(varname, None)
        # if val in mapping:
        #     sim.input[simvar] = mapping[val]
        # else:
        #     sim.input[simvar] = 5.0  # neutral
        """do not need this with drop down type input"""
        sim.input[simvar] = mapping[val]

    set_if('color', color_map, 'color')
    set_if('shape', shape_map, 'shape')
    set_if('texture', texture_map, 'texture')
    set_if('curl', curl_map, 'curl')
    set_if('necrosis', necrosis_map, 'necrosis')
    set_if('defoliation_severity', defoliation_map, 'defoliation')
    set_if('temperature', temp_map, 'temperature')
    set_if('humidity', humidity_map, 'humidity')
    set_if('sunlight', sunlight_map, 'sunlight')

    sim.compute()

    if 'disease' not in sim.output:
        return "Unknown", {lbl: 0 for lbl in disease_labels}

    crisp = float(sim.output['disease'])

    # Compute membership score for each disease MF
    scores = {
        lbl: float(fuzz.interp_membership(diseases.universe,
                                          diseases.terms[lbl].mf,
                                          crisp))
        for lbl in disease_labels
    }

    # Check if all scores are near zero (no match)
    if max(scores.values()) < 0.01:
        return "Unknown", scores

    best = max(scores, key=scores.get)

    return best, scores

# import matplotlib.pyplot as plt
# defoliation.view()
# plt.show()
# texture.view()
# plt.show()
# necrosis.view()
# plt.show()