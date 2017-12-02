"""
All values are in SI units unless their suffix specifies otherwise
"""
import numpy as np
from scipy.constants import k as k_B

BCS = 1.76
aluminum = {'v_Fermi': 2.03e6,  # m / s, Ashcroft & Mermin ToDo: verify
            'E_Fermi_eV': 11.63,  # eV, KozorezovPRB2000
            'E_Debye_eV': 36.9e-3,  # eV, KozorezovPRB2000
            'N0_per_eV_per_um3': 1.74e10  #
            }

niobium = {}

# Fiducial parameters
T_c = 1.3
Delta = BCS * k_B * T_c
T_bath = T_c / 10
f_mc = 3.0e9
f_1p = 0.1e9

# Multichroic 23-pixel nominal resonance frequencies
f_23_pixel = 1e6 * np.concatenate([np.linspace(2542, 2634, 23),
                                   np.linspace(2664, 2756, 23),
                                   np.linspace(2786, 2878, 23),
                                   np.linspace(2908, 3000, 23)])
