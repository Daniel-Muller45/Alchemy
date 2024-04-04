from scipy.integrate import solve_ivp
import numpy as np
from scipy.optimize import fsolve
import json


def pfr_expansion_factor(v_0, T, P_0, c_A0, c_B0, k, V):
    """
    Calculate the conversion and production in an isothermal Plug Flow Reactor with molar expansion given:
        - Volumetric Flow Rate
        - Temperature
        - Initial Pressure
        - Initial Concentration of A
        - Initial Concentration of B
        - Rate Constant
        - Reactor Volume
    """
    R = 8.206 * 10 ** (-5)
    delta = -1
    F_A0 = c_A0 * v_0
    F_B0 = c_B0 * v_0
    F_C0 = 0
    F_T0 = F_A0 + F_B0 + F_C0
    e = c_A0 * R * T / P_0 * delta
    initial_condition = [F_A0, F_B0, F_C0]
    v_bounds = [0, V]
    v_span = np.linspace(v_bounds[0], v_bounds[1], 101).flatten()

    def dFdV(Vspan, F):
        F_A = F[0]
        F_B = F[1]
        F_C = F[2]
        F_T = F_A + F_B + F_C
        X = 1 - F_A / F_A0
        v = v_0 * (1 + e * X)
        c_A = F_A / v
        c_B = F_B / v
        r_A = -k * c_A * c_B
        dFdV = [r_A, r_A, -r_A]
        return dFdV

    sol = solve_ivp(dFdV, v_bounds, initial_condition, t_eval=v_span, dense_output=True, method='Radau')
    F_A, F_B, F_C = sol.y
    conv = 1 - F_A[-1] / F_A0
    prod = c_A0 * v_0 * 3 * conv
    return conv, prod


def pfr_conversion(v_0, T, P_0, c_A0, c_B0, k, V):
    conv, prod = pfr_expansion_factor(v_0, T, P_0, c_A0, c_B0, k, V)
    plug_flow_conversion_dict = {
        "initial_volumetric_flowrate": v_0,
        "temperature": T,
        "initial_pressure": P_0,
        "initial_concentration_of_A": c_A0,
        "initial_concentration_of_B": c_B0,
        "rate_constant": k,
        "reactor_volume": V,
        "conversion": conv,
    }
    return json.dumps(plug_flow_conversion_dict)


def pfr_production(v_0, T, P_0, c_A0, c_B0, k, V):
    conv, prod = pfr_expansion_factor(v_0, T, P_0, c_A0, c_B0, k, V)
    plug_flow_conversion_dict = {
        "initial_volumetric_flowrate": v_0,
        "temperature": T,
        "initial_pressure": P_0,
        "initial_concentration_of_A": c_A0,
        "initial_concentration_of_B": c_B0,
        "rate_constant": k,
        "reactor_volume": V,
        "conversion": prod,
    }
    return json.dumps(plug_flow_conversion_dict)


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

    v_solve = fsolve(objective, 10)[0]
    plug_flow_conversion_dict = {
        "initial_volumetric_flowrate": v_0,
        "temperature": T,
        "initial_pressure": P_0,
        "initial_concentration_of_A": c_A0,
        "initial_concentration_of_B": c_B0,
        "rate_constant": k,
        "reactor_volume": v_solve,
        "conversion": X,
    }
    return json.dumps(plug_flow_conversion_dict)


def pfr_expansion_volume_production(v_0, T, P_0, c_A0, c_B0, k, prod):
    """
    Find the reactor volume needed to achieve a target production of C.

    Parameters:
    - production: Desired production of C
    - v_0: Initial volumetric flow rate
    - T: Temperature
    - P_0: Initial Pressure
    - c_A0: Initial Concentration of A
    - c_B0: Initial Concentration of B
    - k: Rate Constant

    Returns:
    - V: Reactor volume that achieves the target production
    """
    def objective(V):
        conv_calc, prod_calc = pfr_expansion_factor(v_0, T, P_0, c_A0, c_B0, k, V)
        return prod - prod_calc

    v_solve = fsolve(objective, 10)[0]
    plug_flow_conversion_dict = {
        "initial_volumetric_flowrate": v_0,
        "temperature": T,
        "initial_pressure": P_0,
        "initial_concentration_of_A": c_A0,
        "initial_concentration_of_B": c_B0,
        "rate_constant": k,
        "reactor_volume": v_solve,
        "production": prod,
    }
    return json.dumps(plug_flow_conversion_dict)


def pfr_expansion_temperature_conversion(v_0, P_0, c_A0, c_B0, k, V, X):
    """
    Find the reactor temperature needed to achieve a target conversion of A.

    Parameters:
    - X: Desired conversion of A (0 to 1)
    - v_0: Initial volumetric flow rate
    - P_0: Initial Pressure
    - c_A0: Initial Concentration of A
    - c_B0: Initial Concentration of B
    - k: Rate Constant
    - V: Reactor Volume

    Returns:
    - T: Reactor temperature that achieves the target conversion
    """
    def objective(T):
        conv_calc, prod_calc = pfr_expansion_factor(v_0, T, P_0, c_A0, c_B0, k, V)
        return conv_calc - X

    t_solve = fsolve(objective, 10)[0]
    plug_flow_conversion_dict = {
        "initial_volumetric_flowrate": v_0,
        "temperature": t_solve,
        "initial_pressure": P_0,
        "initial_concentration_of_A": c_A0,
        "initial_concentration_of_B": c_B0,
        "rate_constant": k,
        "reactor_volume": V,
        "conversion": X,
    }
    return json.dumps(plug_flow_conversion_dict)


def pfr_expansion_temperature_production(v_0, P_0, c_A0, c_B0, k, V, prod):
    """
    Find the reactor temperature needed to achieve a target production of C.

    Parameters:
    - production: Desired production of C
    - v_0: Initial volumetric flow rate
    - P_0: Initial Pressure
    - c_A0: Initial Concentration of A
    - c_B0: Initial Concentration of B
    - k: Rate Constant
    - V: Reactor volume

    Returns:
    - T: Reactor temperature that achieves the target production
    """
    def objective(T):
        conv_calc, prod_calc = pfr_expansion_factor(v_0, T, P_0, c_A0, c_B0, k, V)
        return prod - prod_calc

    t_solve = fsolve(objective, 10)[0]
    plug_flow_conversion_dict = {
        "initial_volumetric_flowrate": v_0,
        "temperature": t_solve,
        "initial_pressure": P_0,
        "initial_concentration_of_A": c_A0,
        "initial_concentration_of_B": c_B0,
        "rate_constant": k,
        "reactor_volume": V,
        "production": prod,
    }
    return json.dumps(plug_flow_conversion_dict)
