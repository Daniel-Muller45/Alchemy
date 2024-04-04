from reactors.pfr.molar_expansion import pfr_expansion_factor, pfr_conversion
from scipy.optimize import fsolve
#
# # def pfr_expansion_volume_conversion(v_0, T, P_0, c_A0, c_B0, k, X):
# #     """
# #     Find the reactor volume needed to achieve a target conversion of A.
# #
# #     Parameters:
# #     - X: Desired conversion of A (0 to 1)
# #     - v_0: Initial volumetric flow rate
# #     - T: Temperature
# #     - P_0: Initial Pressure
# #     - c_A0: Initial Concentration of A
# #     - c_B0: Initial Concentration of B
# #     - k: Rate Constant
# #
# #     Returns:
# #     - V: Reactor volume that achieves the target conversion
# #     """
# #     def objective(V):
# #         conv_calc, _ = pfr_expansion_factor(v_0, T, P_0, c_A0, c_B0, k, V)
# #         return conv_calc - X
# #
# #     # Initial guess for the reactor volume
# #     V_guess = 1  # This value might need to be adjusted based on the system
# #     v_solve = fsolve(objective, V_guess)[0]
# #
# #     # Dictionary to store the results
# #     plug_flow_conversion_dict = {
# #         "initial_volumetric_flowrate": v_0,
# #         "temperature": T,
# #         "initial_pressure": P_0,
# #         "initial_concentration_of_A": c_A0,
# #         "initial_concentration_of_B": c_B0,
# #         "rate_constant": k,
# #         "reactor_volume": v_solve,
# #         "conversion": X,
# #     }
# #
# #     return json.dumps(plug_flow_conversion_dict)
#
# v_0 = 0.01
# T = 350
# P_0 = 1
# c_A0 = 10
# c_B0 = 10
# k = 0.0302
#
# print(pfr_conversion(v_0, T, P_0, c_A0, c_B0, k, 1.2))

def pfr_expansion_volume_conversion(v_0, T, P_0, c_A0, c_B0, k, X):
    """
    Find the reactor volume needed to achieve a target conversion of A.

    Parameters:
    - X: Desired conversion of A (0 to 1)
    - v_0: Initial volumetric flow rate
    - T: Temperature
    - P_0: Initial Pressure
    - c_A0: Initial Concentration of A
    - c_B0: Initial Concentration of B
    - k: Rate Constant
    - V_max: Maximum reactor volume to consider

    Returns:
    - V: Reactor volume that achieves the target conversion
    """
    def objective(V):
        conv_calc, prod_calc = pfr_expansion_factor(v_0, T, P_0, c_A0, c_B0, k, V)
        return conv_calc - X

    v_solve = fsolve(objective, 1)[0]
    # plug_flow_conversion_dict = {
    #     "initial_volumetric_flowrate": v_0,
    #     "temperature": T,
    #     "initial_pressure": P_0,
    #     "initial_concentration_of_A": c_A0,
    #     "initial_concentration_of_B": c_B0,
    #     "rate_constant": k,
    #     "reactor_volume": v_solve,
    #     "conversion": X,
    # }
    return v_solve

print(pfr_expansion_volume_conversion(0.01, 350, 1, 10, 10, 0.0302, 0.9))
"v_0, T, P_0, c_A0, c_B0, k, X"