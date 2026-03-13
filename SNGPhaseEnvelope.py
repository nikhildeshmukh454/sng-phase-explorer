import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server environments
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from thermopack.cubic import cubic
from thermopack.pcsaft import pcsaft


class SNGPhaseEnvelope:

    def __init__(self):

        self.components = "N2,CO2,C1,C2,C3,IC4,NC4,IC5,NC5,NC6,NC7,NC8,NC10"

        self.SNG_data = {

        1:[0,0,94.085,4.468,0,0,0,1.4470,0,0,0,0,0],
        2:[0,0,81.4,0,0,0,13.5,0,0,0,0,0,5.1],
        3:[0,0,60.0,0,0,0,31.0,0,0,0,0,0,9.0],
        4:[0,0,89.0,7.0,0,4.0,0,0,0,0,0,0,0],
        5:[1.559,25.908,69.114,2.620,0.423,0.105,0.104,0.034,0.023,0.110,0,0,0],
        6:[0.772,1.700,84.446,8.683,3.297,0.293,0.589,0.084,0.086,0.050,0,0,0],
        7:[0,0,93.505,2.972,1.008,1.050,1.465,0,0,0,0,0,0],
        8:[0,0,84.280,10.067,4.028,0.597,1.028,0,0,0,0,0,0],
        9:[0,0,96.611,0,0,1.527,1.475,0.385,0,0,0,0,0],
        10:[0,0,93.600,2.630,0,1.490,1.490,0.795,0,0,0,0,0],
        11:[0.618,0.187,98.9430,0.082,0.065,0.050,0,0.017,0,0.032,0.0027,0.0033,0],
        12:[0.313,0.202,90.4183,8.038,0.801,0.081,0.123,0.010,0.0079,0.0047,0.0011,0,0],
        13:[2.80,0.20,96.6159,0.18,0.1029,0.0499,0.0095,0.0166,0,0.0160,0.0054,0.0038,0],
        14:[6.90,0.51,88.1882,2.72,0.85,0.17,0.32,0.0850,0.0940,0.119,0.0258,0.018,0],
        15:[5.651,0.284,83.3482,7.526,2.009,0.305,0.520,0.120,0.144,0.068,0.0138,0.011,0],
        16:[0,0.67,89.9584,8.22,0.90,0.11,0.13,0.0084,0.0032,0,0,0,0],
        17:[0,0.48,88.7634,8.54,1.68,0.22,0.29,0.0182,0.0084,0,0,0,0],
        18:[0,0.862,86.4838,9.832,2.388,0.183,0.231,0.0139,0.0063,0,0,0,0],
        19:[0,0.410,96.4654,2.510,0.213,0.184,0.197,0.0096,0.0100,0.0010,0,0,0]

        }

        for k in self.SNG_data:
            z = np.array(self.SNG_data[k])
            self.SNG_data[k] = z/z.sum()


    def solve(self, num, save_path="plot.jpg"):

        if num not in self.SNG_data:
            raise ValueError("Choose number between 1–19")

        z = self.SNG_data[num]
        n = len(z)

        # =====================
        # PR EOS
        # =====================

        pr = cubic(self.components,"PR")

        for i in range(1,n+1):
            for j in range(i+1,n+1):
                pr.set_kij(i,j,0.0)

        T_pr,P_pr = pr.get_envelope_twophase(1e5,z)

        T_pr = np.array(T_pr)
        P_pr = np.array(P_pr)/1e6

        crit_pr = None

        try:
            crit = pr.critical(z)
            crit_pr = (crit[0],crit[-1]/1e6)
        except:
            pass


        # =====================
        # PC-SAFT EOS
        # =====================

        pc = pcsaft(self.components)

        for i in range(1,n+1):
            for j in range(i+1,n+1):
                pc.set_kij(i,j,0.0)

        T_pc,P_pc = pc.get_envelope_twophase(1e5,z)

        T_pc = np.array(T_pc)
        P_pc = np.array(P_pc)/1e6

        crit_pc = None

        try:
            crit = pc.critical(z)
            crit_pc = (crit[0],crit[-1]/1e6)
        except:
            pass


        # =====================
        # Plot
        # =====================

        plt.figure(figsize=(7,5))

        plt.plot(T_pr,P_pr,'k-',label="Peng-Robinson EOS")
        plt.plot(T_pc,P_pc,'k--',label="PC-SAFT EOS")

        if crit_pr:
            plt.scatter(*crit_pr,marker='s',s=80,
                        facecolors='none',
                        edgecolors='black',
                        label="PR Critical")

        if crit_pc:
            plt.scatter(*crit_pc,marker='s',s=80,
                        color='black',
                        label="PC-SAFT Critical")

        plt.xlabel("Temperature (K)")
        plt.ylabel("Pressure (MPa)")
        plt.title(f"SNG{num} Phase Envelope")

        plt.xlim(190,None)

        plt.legend()
        plt.grid()

        # Save with high quality
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        return save_path


# ==========================================
# Create Pickle
# ==========================================

if __name__ == "__main__":
    engine = SNGPhaseEnvelope()

    with open("SNGPhaseEnvelope.pkl","wb") as f:
        pickle.dump(engine, f)

    print("SNGPhaseEnvelope.pkl created successfully")