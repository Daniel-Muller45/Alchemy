from scipy.integrate import solve_ivp
import numpy as np
from molar_expansion import pfr_expansion_factor
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
import json


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
    description = """Useful for when you need to calculate the conversion or production from a plug flow reactor, given the volumetric flow rate, Temperature, Initial Pressure,
    Initial Concentration of A, Initial Concentration of B, Rate Constant, and Reactor Volume. Remember that volumetric flow rate is given in units of cubic meters per minute,
    temperature is in kelvin, initial pressure is in atm, initial concentration of A is in mol per cubic meter, initial concentration of B in mol per cubic meter, rate constant 
    in cubic meters per moles per min, and reactor volume is in cubic meters."""

    def _run(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, volume: float):
        return pfr_expansion_factor(volumetric, temperature, pressure, concentrationOfA, concentrationOfB, rateConstant, volume)

    def _arun(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, volume: float):
        return NotImplementedError("This tool does not support async")

    args_schema: Type[BaseModel] = PlugFlowConversionCheckInput
