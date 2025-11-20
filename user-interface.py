from flask import Flask, render_template_string, request
from main import diagnose, color_map, shape_map, texture_map, curl_map, necrosis_map, defoliation_map, temp_map
from main import humidity_map, sunlight_map, disease_labels

app = Flask(__name__)

# Options for each input
options = {
    "color": ["None"] + list(color_map.keys()),
    "shape": ["None"] + list(shape_map.keys()),
    "texture": ["None"] + list(texture_map.keys()),
    "curl": list(curl_map.keys()),
    "necrosis": list(necrosis_map.keys()),
    "defoliation_severity": ["None"] + list(defoliation_map.keys()),
    "temperature": ["None"] + list(temp_map.keys()),
    "humidity": ["None"] + list(humidity_map.keys()),
    "sunlight": ["None"] + list(sunlight_map.keys())
}

# Group inputs into 3 sections
sections = {
    "Leaf Appearance": ["color", "shape", "texture", "curl"],
    "Leaf Health": ["necrosis", "defoliation_severity"],
    "Environment": ["temperature", "humidity", "sunlight"]
}

template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🌿 Plant Disease Detection System 🌿</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #121212;
            color: #e0e0e0;
            margin: 0;
            padding: 0;
        }
        h1 {
            text-align: center;
            padding: 25px 0;
            margin: 0;
            font-size: 2.2em;
            color: #4caf50;
            text-shadow: 1px 1px 3px #000;
        }
        form {
            max-width: 1000px;
            margin: 30px auto;
            padding: 25px;
            background: #1e1e1e;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.7);
        }
        .flex-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        .section {
            flex: 1;
            min-width: 300px;
            padding: 20px;
            border-radius: 15px;
            background: #2a2a2a;
            box-shadow: 4px 4px 10px rgba(0,0,0,0.6), -4px -4px 10px rgba(60,60,60,0.3);
        }
        .section h2 {
            margin-top: 0;
            color: #ff9800;
            border-bottom: 1px solid #444;
            padding-bottom: 8px;
        }
        .label {
            font-weight: bold;
            display: block;
            margin-bottom: 10px;
            color: #4caf50;
        }
        select {
            padding: 8px 12px;
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #555;
            width: 100%;
            background: #3c3c3c;
            color: #e0e0e0;
            box-shadow: inset 2px 2px 5px rgba(0,0,0,0.3);
        }
        input[type="submit"] {
            padding: 12px 25px;
            font-size: 16px;
            font-weight: bold;
            color: #fff;
            background: linear-gradient(to right, #4caf50, #66bb6a);
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            margin-top: 20px;
        }
        input[type="submit"]:hover {
            background: linear-gradient(to right, #43a047, #57b05d);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        }
        .result-box {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 500px;
            max-width: 90%;
            padding: 25px;
            background: #1e1e1e;
            border-radius: 20px;
            box-shadow: 0 15px 30px rgba(0,0,0,0.8);
            border: 1px solid #444;
            display: none;
            z-index: 1000;
            animation: fadeIn 0.4s ease;
            color: #e0e0e0;
        }
        .result-box h2 {
            color: #ff9800;
            margin-top: 0;
        }
        .result-box ul {
            list-style: none;
            padding-left: 0;
        }
        .result-box ul li {
            padding: 5px 0;
            border-bottom: 1px dashed #555;
        }
        .close-btn {
            display: block;
            text-align: right;
            margin-bottom: 10px;
            cursor: pointer;
            color: #f44336;
            font-weight: bold;
        }
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        @media (max-width: 700px) {
            .flex-container {
                flex-direction: column;
            }
        }
    </style>
    <script>
        function showResult() {
            document.getElementById('resultBox').style.display = 'block';
        }
        function closeResult() {
            document.getElementById('resultBox').style.display = 'none';
        }
    </script>
</head>
<body>
    <h1>🌿 Plant Disease Detection System 🌿</h1>
    <form method="POST">
        <div class="flex-container">
            {% for section_name, vars in sections.items() %}
                {% if loop.index <= 2 %}
                <div class="section">
                    <h2>{{ section_name }}</h2>
                    {% for var in vars %}
                        <label class="label">{{ var.replace('_', ' ').title() }}:</label>
                        <select name="{{ var }}">
                            {% for opt in options[var] %}
                                <option value="{{ opt }}">{{ opt.replace('_', ' ').title() }}</option>
                            {% endfor %}
                        </select>
                    {% endfor %}
                </div>
                {% endif %}
            {% endfor %}
        </div>
        {% for section_name, vars in sections.items() %}
            {% if loop.index == 3 %}
            <div class="section">
                <h2>{{ section_name }}</h2>
                {% for var in vars %}
                    <label class="label">{{ var.replace('_', ' ').title() }}:</label>
                    <select name="{{ var }}">
                        {% for opt in options[var] %}
                            <option value="{{ opt }}">{{ opt.replace('_', ' ').title() }}</option>
                        {% endfor %}
                    </select>
                {% endfor %}
            </div>
            {% endif %}
        {% endfor %}
        <input type="submit" value="Diagnose" {% if result %}onclick="showResult()" {% endif %}>
    </form>

    {% if result %}
    <div class="result-box" id="resultBox">
        <span class="close-btn" onclick="closeResult()">✖ Close</span>
        {% if result.best == "Unknown" %}
            <h2>No match found / Invalid input</h2>
        {% else %}
            <h2>Top 3 Disease Predictions</h2>
            <ul>
                {% for disease, score in result.top3 %}
                <li>{{ disease }} → {{ "%.4f"|format(score) }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
    <script>showResult();</script>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        # Collect input values
        inputs = {var: None if request.form.get(var) == "None" else request.form.get(var) for var in options}
        best, scores = diagnose(inputs)

        # Sort scores descending and pick top 3
        top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

        result = {"best": best, "scores": scores, "top3": top3}

    return render_template_string(template, options=options, sections=sections, result=result)


if __name__ == "__main__":
    app.run(debug=True)
