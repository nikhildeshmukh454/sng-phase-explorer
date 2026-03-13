import numpy as np
import matplotlib.pyplot as plt
from thermopack.cubic import cubic
from thermopack.pcsaft import pcsaft

class SNGPhaseEnvelope2:
    def __init__(self):
        self.components = "N2,CO2,C1,C2,C3,IC4,NC4,IC5,NC5,NC6,NC7,NC8,NC10"

    def solve(self, z, save_path="custom_plot.png"):
        """
        z: list of mole fractions (length 13) summing to 1.
        save_path: where to save the generated plot.
        """
        n = len(z)

        # =====================
        # PR EOS
        # =====================
        pr = cubic(self.components, "PR")
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                pr.set_kij(i, j, 0.0)

        T_pr, P_pr = pr.get_envelope_twophase(1e5, z)
        T_pr = np.array(T_pr)
        P_pr = np.array(P_pr) / 1e6

        # =====================
        # PC-SAFT EOS
        # =====================
        pc = pcsaft(self.components)
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                pc.set_kij(i, j, 0.0)

        T_pc, P_pc = pc.get_envelope_twophase(1e5, z)
        T_pc = np.array(T_pc)
        P_pc = np.array(P_pc) / 1e6

        # =====================
        # Plot
        # =====================
        plt.figure(figsize=(7, 5))
        plt.plot(T_pr, P_pr, 'k-', label="Peng-Robinson EOS")
        plt.plot(T_pc, P_pc, 'k--', label="PC-SAFT EOS")

        # Optionally add critical points
        try:
            crit_pr = pr.critical(z)
            plt.scatter(crit_pr[0], crit_pr[-1]/1e6,
                        marker='s', s=80, facecolors='none',
                        edgecolors='black', label="PR Critical")
        except:
            pass

        try:
            crit_pc = pc.critical(z)
            plt.scatter(crit_pc[0], crit_pc[-1]/1e6,
                        marker='s', s=80, color='black',
                        label="PC-SAFT Critical")
        except:
            pass

        plt.xlabel("Temperature (K)")
        plt.ylabel("Pressure (MPa)")
        plt.title("Custom Mixture Phase Envelope")
        plt.xlim(190, None)
        plt.legend()
        plt.grid()
        plt.savefig(save_path)
        plt.close()

        return save_path

import pickle
engine = SNGPhaseEnvelope2()

with open("SNGPhaseEnvelope2.pkl","wb") as f:
    pickle.dump(engine,f)

print("SNGPhaseEnvelope2.pkl created successfully")