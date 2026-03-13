import numpy as np
import matplotlib.pyplot as plt
import os

class ChemicalGraphs:
    """
    Chemical graph engine (CO2 only for now)
    Supports:
    - P–V (Peng–Robinson EOS)
    - P–T (Saturation curve)
    """

    R = 8.314  # J/mol-K

    def __init__(self):
        # ---- CO2 properties ----
        self.CO2 = {
            "name": "Carbon Dioxide",
            "Tc": 304.2,      # K
            "Pc": 7.38e6,     # Pa
            "omega": 0.225
        }

    # ==================================================
    # MAIN ENTRY POINT
    # ==================================================
    def generate_graph(
        self,
        graph_type,        # "PV" or "PT"
        user_inputs,
        image_path="static/plots/current_plot.png"
    ):
        """
        Decides which graph to generate based on graph_type
        """

        graph_type = graph_type.upper()

        if graph_type == "PV":
            return self.p_v(
                T=user_inputs["T"],
                image_path=image_path
            )

        elif graph_type == "PT":
            return self.p_t(
                T_min=user_inputs["T_min"],
                T_max=user_inputs["T_max"],
                image_path=image_path
            )

        else:
            raise ValueError("Graph type must be 'PV' or 'PT'")

    # ==================================================
    # P–V GRAPH (Peng–Robinson EOS)
    # ==================================================
    def p_v(self, T, image_path):
        """
        Generates P–V diagram for CO2 using PR EOS
        """

        Tc = self.CO2["Tc"]
        Pc = self.CO2["Pc"]
        omega = self.CO2["omega"]

        # ---- PR EOS parameters ----
        a_c = 0.45724 * self.R**2 * Tc**2 / Pc
        b = 0.07780 * self.R * Tc / Pc

        kappa = 0.37464 + 1.54226*omega - 0.26992*omega**2
        alpha = (1 + kappa*(1 - np.sqrt(T/Tc)))**2
        a = a_c * alpha

        # ---- Data ----
        V = np.linspace(0.0005, 0.01, 300)
        P = (self.R*T)/(V - b) - a/(V*(V + b) + b*(V - b))

        # ---- Plot ----
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        plt.figure(figsize=(7, 5))
        plt.plot(V, P, linewidth=2)
        plt.xlabel("Molar Volume (m³/mol)")
        plt.ylabel("Pressure (Pa)")
        plt.title("CO₂ P–V Curve (Peng–Robinson EOS)")
        plt.grid(True)
        plt.savefig(image_path, dpi=200, bbox_inches="tight")
        plt.close()

        return {
            "graph_type": "P–V",
            "substance": "CO₂",
            "equation": "Peng–Robinson EOS",
            "parameters": {
                "T": T,
                "Tc": Tc,
                "Pc": Pc,
                "omega": omega
            },
            "image_path": image_path
        }

    # ==================================================
    # P–T GRAPH (SATURATION CURVE)
    # ==================================================
    def p_t(self, T_min, T_max, image_path):
        """
        Generates P–T saturation curve for CO2
        using vapor pressure correlation
        """

        # Antoine constants for CO2
        A = 6.81228
        B = 1301.679
        C = -3.494

        T = np.linspace(T_min, T_max, 200)

        log10_P = A - (B / (T + C))      # P in bar
        P_bar = 10 ** log10_P
        P = P_bar * 1e5                 # bar → Pa

        # ---- Plot ----
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        plt.figure(figsize=(7, 5))
        plt.plot(T, P, linewidth=2)
        plt.xlabel("Temperature (K)")
        plt.ylabel("Pressure (Pa)")
        plt.title("CO₂ P–T Saturation Curve")
        plt.grid(True)
        plt.savefig(image_path, dpi=200, bbox_inches="tight")
        plt.close()

        return {
            "graph_type": "P–T",
            "substance": "CO₂",
            "equation": "Saturation Pressure Correlation",
            "parameters": {
                "T_min": T_min,
                "T_max": T_max
            },
            "image_path": image_path
        }

