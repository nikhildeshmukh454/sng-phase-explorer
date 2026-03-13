# import os
# # Prevent OpenMP and Intel MKL thread collisions (Windows stability)
# os.environ["OMP_NUM_THREADS"] = "1"
# os.environ["MKL_NUM_THREADS"] = "1"

# import numpy as np
# import matplotlib.pyplot as plt
# import warnings

# warnings.filterwarnings("ignore")

# try:
#     from thermopack.cubic import cubic
#     from thermopack.pcsaft import pcsaft
#     THERMO_OK = True
#     print("✅ Thermopack loaded successfully (PR + PC-SAFT)")
# except ImportError:
#     print("❌ Install thermopack: pip install thermopack")
#     THERMO_OK = False

# # ==========================================
# # 1. EXACT PAPER COMPOSITIONS (% molar normalized)
# # ==========================================
# comps6 = "N2,CO2,C1,C2,C3,IC4,NC4,IC5,NC5,NC6"
# z6 = np.array([0.772, 1.700, 84.446, 8.683, 3.297, 0.293, 0.589, 0.084, 0.086, 0.050])
# z6 = z6 / z6.sum()

# comps14 = "N2,CO2,C1,C2,C3,IC4,NC4,IC5,NC5,NC6,NC7,NC8"
# z14 = np.array([6.90, 0.51, 88.1882, 2.72, 0.85, 0.17, 0.32, 0.085, 0.094, 0.119, 0.0258, 0.018])
# z14 = z14 / z14.sum()

# # ==========================================
# # 2. HIGH-FIDELITY DIGITIZED EXPERIMENTAL DATA
# # ==========================================
# exp6_T = np.array([218.0, 219.5, 222.5, 228.0, 232.0, 236.0, 239.0, 241.0, 242.5, 244.5, 
#                    246.5, 247.5, 249.5, 250.5, 252.0, 253.0, 254.0, 255.0, 256.5, 257.5, 
#                    258.0, 258.5, 259.0, 260.0, 260.0, 259.0, 258.0, 257.0, 256.0, 254.5, 
#                    254.0, 251.5, 250.5, 249.5, 247.5, 245.5, 244.5, 243.5, 242.5, 241.5, 
#                    239.5, 238.5, 236.5, 235.0, 234.0])
# exp6_P = np.array([0.10, 0.12, 0.20, 0.30, 0.40, 0.50, 0.65, 0.75, 0.85, 1.00, 1.15, 1.25, 
#                    1.45, 1.55, 1.80, 1.95, 2.20, 2.55, 3.05, 3.40, 3.75, 4.15, 4.50, 5.10, 
#                    5.60, 6.20, 6.70, 7.00, 7.40, 7.60, 7.65, 7.80, 7.95, 8.05, 8.10, 8.15, 
#                    8.15, 8.15, 8.15, 8.15, 8.10, 8.10, 8.00, 7.95, 7.95])
                   

# exp14_T = np.array([248.0, 252.0, 257.0, 261.0, 265.0, 268.0, 271.5, 274.0, 275.5, 276.0, 
#                     276.5, 276.5, 276.0, 275.5, 275.0, 274.5, 273.5, 272.0, 271.0, 269.0, 
#                     267.0, 265.5, 263.0, 260.5, 256.0, 250.5, 246.5, 243.5, 240.5, 236.0, 
#                     231.5, 229.0, 226.0, 222.5, 220.5, 217.5, 214.5, 211.5])
# exp14_P = np.array([0.15, 0.25, 0.35, 0.50, 0.70, 1.00, 1.45, 1.95, 2.50, 2.95, 3.50, 4.00, 
#                     4.50, 5.00, 5.45, 5.95, 6.50, 7.00, 7.50, 8.10, 8.50, 8.80, 9.15, 9.50, 
#                     10.00, 10.50, 10.60, 10.60, 10.60, 10.20, 9.90, 9.50, 9.00, 8.55, 8.30, 
#                     7.85, 7.40, 6.80])

# # ==========================================
# # 3. EOS ENVELOPE CALCULATORS + LIVE CRITICAL POINTS
# # ==========================================
# def compute_pr_envelope(comps, z):
#     eos = cubic(comps, "PR")
#     ncomp = len(z)
#     for i in range(1, ncomp + 1):
#         for j in range(i + 1, ncomp + 1):
#             eos.set_kij(i, j, 0.0)
    
#     env_T, env_P = eos.get_envelope_twophase(1e5, z)
#     env_T, env_P = np.array(env_T), np.array(env_P) / 1e6
    
#     # CORRECT UNPACKING: critical(z) returns (Temperature, Specific Volume, Pressure)
#     crit = eos.critical(z)
#     crit_T = crit[0]
#     crit_P = crit[-1] / 1e6 # [-1] safely grabs the pressure regardless of tuple size
    
#     return env_T, env_P, (crit_T, crit_P)

# def compute_pcsaft_envelope(comps, z):
#     eos = pcsaft(comps)
#     ncomp = len(z)
#     for i in range(1, ncomp + 1):
#         for j in range(i + 1, ncomp + 1):
#             eos.set_kij(i, j, 0.0)
            
#     env_T, env_P = eos.get_envelope_twophase(1e5, z)
#     env_T, env_P = np.array(env_T), np.array(env_P) / 1e6
    
#     # CORRECT UNPACKING
#     crit = eos.critical(z)
#     crit_T = crit[0]
#     crit_P = crit[-1] / 1e6
    
#     return env_T, env_P, (crit_T, crit_P)

# # ==========================================
# # 4. MAIN EXECUTION - SHOW PLOT!
# # ==========================================
# def plot_paper_figures():
#     print("🎯 Computing rigorous EOS envelopes and critical points (kij=0)...")

#     if THERMO_OK:
#         T_pr6, P_pr6, crit_pr_6 = compute_pr_envelope(comps6, z6)
#         T_pc6, P_pc6, crit_pc_6 = compute_pcsaft_envelope(comps6, z6)
#         T_pr14, P_pr14, crit_pr_14 = compute_pr_envelope(comps14, z14)
#         T_pc14, P_pc14, crit_pc_14 = compute_pcsaft_envelope(comps14, z14)
#         print("✅ Critical points rigorously calculated via Heidemann & Khalil matrix!")
#     else:
#         return

#     # Paper-exact 1x2 plot
#     fig, (ax6, ax14) = plt.subplots(1, 2, figsize=(11, 5.2))

#     # === FIGURE 6: SNG6 ===
#     ax6.plot(T_pr6, P_pr6, '-', color='black', lw=1.8, label='Peng-Robinson EOS (—)')
#     ax6.plot(T_pc6, P_pc6, '--', color='black', lw=1.8, label='PC-SAFT EOS (−−)')
#     ax6.scatter(exp6_T, exp6_P, c='black', s=30, marker='o', zorder=10, label='Experimental (•)')
    
#     ax6.scatter(*crit_pr_6, marker='s', s=80, facecolors='none', edgecolors='black', lw=1.5, label='PR critical (□)', zorder=11)
#     ax6.scatter(*crit_pc_6, marker='s', s=80, c='black', zorder=11, label='PC-SAFT critical (■)')
    
#     ax6.set_xlim(210, 270); ax6.set_ylim(0, 10)
#     ax6.set_xlabel('Temperature (K)', fontsize=11)
#     ax6.set_ylabel('Pressure (MPa)', fontsize=11)
#     ax6.set_title('Figure 6\nSNG6.', loc='left', pad=10, fontsize=12)
#     ax6.legend(loc='upper left', frameon=False, fontsize=9)
#     ax6.tick_params(direction='in', top=True, right=True, labelsize=10)

#     # === FIGURE 14: SNG14 ===
#     ax14.plot(T_pr14, P_pr14, '-', color='black', lw=1.8, label='Peng-Robinson EOS (—)')
#     ax14.plot(T_pc14, P_pc14, '--', color='black', lw=1.8, label='PC-SAFT EOS (−−)')
#     ax14.scatter(exp14_T, exp14_P, c='black', s=30, marker='o', zorder=10, label='Experimental (•)')
    
#     ax14.scatter(*crit_pr_14, marker='s', s=80, facecolors='none', edgecolors='black', lw=1.5, label='PR critical (□)', zorder=11)
#     ax14.scatter(*crit_pc_14, marker='s', s=80, c='black', zorder=11, label='PC-SAFT critical (■)')
    
#     ax14.set_xlim(190, 280); ax14.set_ylim(0, 12)
#     ax14.set_xlabel('Temperature (K)', fontsize=11)
#     ax14.set_ylabel('Pressure (MPa)', fontsize=11)
#     ax14.set_title('Figure 14\nSNG14.', loc='left', pad=10, fontsize=12)
#     ax14.legend(loc='upper left', frameon=False, fontsize=9)
#     ax14.tick_params(direction='in', top=True, right=True, labelsize=10)

#     plt.tight_layout()
    
#     print("\n🎉 SUCCESS! PERFECT MATCH ACHIEVED:")
#     print(f"   SNG6 - PR crit: ({crit_pr_6[0]:.1f}K, {crit_pr_6[1]:.2f}MPa)")
#     print(f"   SNG6 - PC-SAFT crit: ({crit_pc_6[0]:.1f}K, {crit_pc_6[1]:.2f}MPa)")
#     print(f"   SNG14 - PR crit: ({crit_pr_14[0]:.1f}K, {crit_pr_14[1]:.2f}MPa)")
#     print(f"   SNG14 - PC-SAFT crit: ({crit_pc_14[0]:.1f}K, {crit_pc_14[1]:.2f}MPa)")
    
#     plt.show()

# if __name__ == "__main__":
#     plot_paper_figures()


import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

try:
    from thermopack.cubic import cubic
    from thermopack.pcsaft import pcsaft
    THERMO_OK = True
    print("✅ Thermopack loaded successfully (PR + PC-SAFT)")
except ImportError:
    print("❌ Install thermopack: pip install thermopack")
    THERMO_OK = False


# =====================================================
# COMPONENT LIST
# =====================================================

components = "N2,CO2,C1,C2,C3,IC4,NC4,IC5,NC5,NC6,NC7,NC8,NC10"


# =====================================================
# SNG MIXTURE COMPOSITIONS
# =====================================================

SNG_data = {

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

# Normalize compositions
for key in SNG_data:
    z = np.array(SNG_data[key])
    SNG_data[key] = z / z.sum()


# =====================================================
# EOS FUNCTIONS
# =====================================================

def compute_pr_envelope(comps, z):

    eos = cubic(comps, "PR")
    ncomp = len(z)

    for i in range(1, ncomp + 1):
        for j in range(i + 1, ncomp + 1):
            eos.set_kij(i, j, 0.0)

    env_T, env_P = eos.get_envelope_twophase(1e5, z)

    env_T = np.array(env_T)
    env_P = np.array(env_P) / 1e6

    crit_point = None
    try:
        crit = eos.critical(z)
        crit_point = (crit[0], crit[-1] / 1e6)
    except:
        print("⚠ PR critical calculation failed")

    return env_T, env_P, crit_point


def compute_pcsaft_envelope(comps, z):

    eos = pcsaft(comps)
    ncomp = len(z)

    for i in range(1, ncomp + 1):
        for j in range(i + 1, ncomp + 1):
            eos.set_kij(i, j, 0.0)

    env_T, env_P = eos.get_envelope_twophase(1e5, z)

    env_T = np.array(env_T)
    env_P = np.array(env_P) / 1e6

    crit_point = None
    try:
        crit = eos.critical(z)
        crit_point = (crit[0], crit[-1] / 1e6)
    except:
        print("⚠ PC-SAFT critical calculation failed")

    return env_T, env_P, crit_point


# =====================================================
# PLOT FUNCTION
# =====================================================

def plot_sng(num):

    if num not in SNG_data:
        print("❌ Choose number between 1–19")
        return

    z = SNG_data[num]

    print(f"\nRunning SNG{num}")

    T_pr, P_pr, crit_pr = compute_pr_envelope(components, z)
    T_pc, P_pc, crit_pc = compute_pcsaft_envelope(components, z)

    plt.figure(figsize=(7,5))

    plt.plot(T_pr, P_pr, '-', color='black', lw=2, label="PR EOS")
    plt.plot(T_pc, P_pc, '--', color='black', lw=2, label="PC-SAFT EOS")

    if crit_pr is not None:
        plt.scatter(*crit_pr, marker='s', s=80,
                    facecolors='none', edgecolors='black',
                    label="PR Critical")

    if crit_pc is not None:
        plt.scatter(*crit_pc, marker='s', s=80,
                    color='black', label="PC-SAFT Critical")

    plt.xlabel("Temperature (K)")
    plt.ylabel("Pressure (MPa)")
    plt.title(f"SNG{num} Phase Envelope")
    plt.xlim(190, None)
    plt.legend()
    plt.grid(True)

    plt.show()

    print("\nCritical Points:")

    if crit_pr is not None:
        print(f"PR: {crit_pr[0]:.2f} K , {crit_pr[1]:.2f} MPa")

    if crit_pc is not None:
        print(f"PC-SAFT: {crit_pc[0]:.2f} K , {crit_pc[1]:.2f} MPa")


# =====================================================
# MAIN PROGRAM
# =====================================================

if __name__ == "__main__":

    if not THERMO_OK:
        exit()

    print("\nAvailable mixtures: 1 → 19")

    num = int(input("Enter SNG number: "))

    plot_sng(num)