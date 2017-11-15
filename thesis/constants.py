"""
All values are in SI units unless their suffix specifies otherwise
"""
from scipy.constants import k as k_B

BCS = 1.76
aluminum = {'v_Fermi': 2.03e6,  # m / s, Ashcroft & Mermin ToDo: verify
            'E_Fermi_eV': 11.63,  # eV, KozorezovPRB2000
            'E_Debye_eV': 36.9e-3,  # eV, KozorezovPRB2000
            'N0_per_eV_per_um3': 1.74e10  #
            }

# Fiducial parameters
T_c = 1.3
Delta = BCS * k_B * T_c
T_bath = T_c / 10
f_mc = 2.5e9
f_1p = 0.1e9
