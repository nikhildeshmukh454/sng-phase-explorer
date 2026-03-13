import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from flask import Flask, render_template, request, jsonify
import pickle

# Import the two engine classes
from SNGPhaseEnvelope import SNGPhaseEnvelope      # for preset mixtures
from SNGPhaseEnvelope2 import SNGPhaseEnvelope2    # for custom mixtures

app = Flask(__name__)

# -------------------------------------------------------------------
# Load the pre‑trained engine for preset SNG mixtures (from pickle)
# -------------------------------------------------------------------
PRESET_ENGINE = None
if os.path.exists("SNGPhaseEnvelope.pkl"):
    with open("SNGPhaseEnvelope.pkl", "rb") as f:
        PRESET_ENGINE = pickle.load(f)
else:
    # Fallback: create a new instance if pickle is missing
    PRESET_ENGINE = SNGPhaseEnvelope()

# -------------------------------------------------------------------
# Instantiate the engine for custom compositions
# -------------------------------------------------------------------
CUSTOM_ENGINE = SNGPhaseEnvelope2()

# Ensure the plot directories exist
os.makedirs("static/plots", exist_ok=True)
os.makedirs("static", exist_ok=True)

# -------------------------------------------------------------------
# Main route – serves the page and handles preset SNG form submission
# -------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    # Default values when page first loads
    image_path = "plots/plot.png"  # Always show the same plot
    composition = None
    mixture_name = None

    if request.method == "POST":
        # Retrieve the selected SNG number from the form
        sng_number = int(request.form["sng_number"])
        mixture_name = f"SNG {sng_number}"

        # Generate the phase diagram using the preset engine
        plot_path = os.path.join("static", "plots", "plot.png")
        PRESET_ENGINE.solve(num=sng_number, save_path=plot_path)

        # Retrieve composition data from the engine
        z = PRESET_ENGINE.SNG_data[sng_number]
        comps = PRESET_ENGINE.components.split(",")
        composition = {
            comp: round(val * 100, 2)
            for comp, val in zip(comps, z)
            if val > 0
        }

    return render_template(
        "index.html",
        image_path=image_path,  # Always "plots/plot.png"
        composition=composition,
        mixture_name=mixture_name
    )

# -------------------------------------------------------------------
# Custom composition endpoint – called via AJAX from the browser
# -------------------------------------------------------------------
@app.route("/custom", methods=["POST"])
def custom():
    # Parse the JSON data sent from the front end
    data = request.get_json()
    # data["composition"] is expected to be a list of floats (mole fractions)
    composition = list(map(float, data["composition"]))

    # Define the output plot path
    plot_path = "static/custom_plot.png"

    # Generate the phase diagram using the custom engine
    CUSTOM_ENGINE.solve(composition, plot_path)

    # Return the plot URL so the front end can display it
    return jsonify({"plot": "/" + plot_path})

# -------------------------------------------------------------------
# Run the application
# -------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)