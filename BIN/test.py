import random
from chemical_graphs import ChemicalGraphs

# Create engine object
engine = ChemicalGraphs()

# -------- Generate RANDOM but REALISTIC inputs --------
Tc = random.uniform(150, 600)        # K (typical critical temp range)
Pc = random.uniform(3e6, 8e6)        # Pa (30–80 bar)
omega = random.uniform(0.0, 0.35)    # acentric factor
T = random.uniform(0.6*Tc, 1.2*Tc)   # around critical temperature

print("Testing with inputs:")
print(f"T  = {T:.2f} K")
print(f"Tc = {Tc:.2f} K")
print(f"Pc = {Pc:.2e} Pa")
print(f"ω  = {omega:.3f}")

# -------- Call your function --------
result = engine.generate_peng_robinson_pv_image(
    T=T,
    Tc=Tc,
    Pc=Pc,
    omega=omega
)

print("\nGraph generated!")
print("Saved at:", result["image_path"])
print("Equation:", result["equation"])
print("Parameters:", result["parameters"])
