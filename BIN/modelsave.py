import pickle
from chemical_graphs import ChemicalGraphs

engine = ChemicalGraphs()

with open("chemical_graphs.pkl", "wb") as f:
    pickle.dump(engine, f)

print("ChemicalGraphs saved as chemical_graphs.pkl")