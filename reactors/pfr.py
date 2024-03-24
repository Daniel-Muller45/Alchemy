from scipy.integrate import solve_ivp
import numpy as np
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
import json

"""
Calculate the conversion in an isothermal Plug Flow Reactor with molar expansion given:
    - Volumetric Flow Rate
    - Temperature
    - Initial Pressure
    - Initial Concentration of A
    - Initial Concentration of B
    - Rate Constant
    - Reactor Volume
"""


def pfr_conversion(v_0, T, P_0, c_A0, c_B0, k, V):
    R = 8.206 * 10 ** (-5)
    delta = -1
    F_A0 = c_A0 * v_0
    F_B0 = c_B0 * v_0
    F_C0 = 0
    F_T0 = F_A0 + F_B0 + F_C0
    e = c_A0 * R * T / P_0 * delta
    initial_condition = [F_A0, F_B0, F_C0]
    v_bounds = [0, V]
    v_span = np.linspace(v_bounds[0], v_bounds[1], 101)

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


class PlugFlowConversionCheckInput(BaseModel):
    """Input schema for PlugFLowConversionInput"""

    volumetric: float = Field(..., decsription="The volumetric flow rate of the feed in cubic meters per minute")
    temperature: float = Field(..., description="The temperature of the reactor in kelvin")
    pressure: float = Field(..., description="The pressure of the reactor in atm")
    concentrationOfA: float = Field(..., description="The concentration of A in moles per cubic meters")
    concentrationOfB: float = Field(..., description="The concentration of B in moles per cubic meters")
    rateConstant: float = Field(..., description="The rate constant of the reaction in cubic meters per mole per minute")
    volume: float = Field(..., description="The volume of the reactor in cubic meters")


class PlugFlowConversionTool(BaseTool):
    name = "Plug-flow-reactor"
    description = """Useful for when you need to calculate the conversion from a plug flow reactor, given the volumetric flow rate, Temperature, Initial Pressure,
    Initial Concentration of A, Initial Concentration of B, Rate Constant, and Reactor Volume. Remember that volumetric flow rate is given in units of cubic meters per minute,
    temperature is in kelvin, initial pressure is in atm, initial concentration of A is in mol per cubic meter, initial concentration of B in mol per cubic meter, rate constant 
    in cubic meters per moles per min, and reactor volume is in cubic meters."""

    def _run(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, volume: float):
        return pfr_conversion(volumetric, temperature, pressure, concentrationOfA, concentrationOfB, rateConstant, volume)

    def _arun(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, volume: float):
        return NotImplementedError("This tool does not support async")

    args_schema: Type[BaseModel] = PlugFlowConversionCheckInput
