from reactors.pfr.molar_expansion import (
    pfr_conversion, pfr_production, pfr_expansion_volume_conversion, pfr_expansion_volume_production,
    pfr_expansion_temperature_conversion, pfr_expansion_temperature_production
)

from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type


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
    name = "Pfr-conversion"
    description = """Useful for when you need to calculate the conversion from a plug flow reactor, given the volumetric flow rate, Temperature, Initial Pressure,
    Initial Concentration of A, Initial Concentration of B, Rate Constant, and Reactor Volume. Remember that volumetric flow rate is given in units of cubic meters per minute,
    temperature is in kelvin, initial pressure is in atm, initial concentration of A is in mol per cubic meter, initial concentration of B in mol per cubic meter, rate constant 
    in cubic meters per moles per min, and reactor volume is in cubic meters."""

    def _run(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, volume: float):
        return pfr_conversion(volumetric, temperature, pressure, concentrationOfA, concentrationOfB, rateConstant, volume)

    def _arun(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, volume: float):
        return NotImplementedError("This tool does not support async")

    args_schema: Type[BaseModel] = PlugFlowConversionCheckInput


class PlugFlowProductionCheckInput(BaseModel):
    """Input schema for PlugFLowProductionInput"""

    volumetric: float = Field(..., decsription="The volumetric flow rate of the feed in cubic meters per minute")
    temperature: float = Field(..., description="The temperature of the reactor in kelvin")
    pressure: float = Field(..., description="The pressure of the reactor in atm")
    concentrationOfA: float = Field(..., description="The concentration of A in moles per cubic meters")
    concentrationOfB: float = Field(..., description="The concentration of B in moles per cubic meters")
    rateConstant: float = Field(..., description="The rate constant of the reaction in cubic meters per mole per minute")
    volume: float = Field(..., description="The volume of the reactor in cubic meters")


class PlugFlowProductionTool(BaseTool):
    name = "Pfr-production"
    description = """Useful for when you need to calculate the conversion from a plug flow reactor, given the volumetric flow rate, Temperature, Initial Pressure,
    Initial Concentration of A, Initial Concentration of B, Rate Constant, and Reactor Volume. Remember that volumetric flow rate is given in units of cubic meters per minute,
    temperature is in kelvin, initial pressure is in atm, initial concentration of A is in mol per cubic meter, initial concentration of B in mol per cubic meter, rate constant 
    in cubic meters per moles per min, and reactor volume is in cubic meters."""

    def _run(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, volume: float):
        return pfr_production(volumetric, temperature, pressure, concentrationOfA, concentrationOfB, rateConstant, volume)

    def _arun(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, volume: float):
        return NotImplementedError("This tool does not support async")

    args_schema: Type[BaseModel] = PlugFlowProductionCheckInput


class PlugFlowVolumeConversionCheckInput(BaseModel):
    """Input schema for PlugFLowVolumeConversionInput"""

    volumetric: float = Field(..., decsription="The volumetric flow rate of the feed in cubic meters per minute")
    temperature: float = Field(..., description="The temperature of the reactor in kelvin")
    pressure: float = Field(..., description="The pressure of the reactor in atm")
    concentrationOfA: float = Field(..., description="The concentration of A in moles per cubic meters")
    concentrationOfB: float = Field(..., description="The concentration of B in moles per cubic meters")
    rateConstant: float = Field(..., description="The rate constant of the reaction in cubic meters per mole per minute")
    conversion: float = Field(..., description="The conversion of the limiting reactant")


class PlugFlowVolumeConversionTool(BaseTool):
    name = "Pfr-volume-conversion"
    description = """Useful for when you need to calculate the volume of a plug flow reactor, given the volumetric flow rate, Temperature, Initial Pressure,
    Initial Concentration of A, Initial Concentration of B, Rate Constant, and conversion. Remember that volumetric flow rate is given in units of cubic meters per minute,
    temperature is in kelvin, initial pressure is in atm, initial concentration of A is in mol per cubic meter, initial concentration of B in mol per cubic meter, and rate constant 
    in cubic meters per moles per min."""

    def _run(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, conversion: float):
        return pfr_expansion_volume_conversion(volumetric, temperature, pressure, concentrationOfA, concentrationOfB, rateConstant, conversion)

    def _arun(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, conversion: float):
        return NotImplementedError("This tool does not support async")

    args_schema: Type[BaseModel] = PlugFlowVolumeConversionCheckInput


class PlugFlowVolumeProductionCheckInput(BaseModel):
    """Input schema for PlugFLowVolumeProductionInput"""

    volumetric: float = Field(..., decsription="The volumetric flow rate of the feed in cubic meters per minute")
    temperature: float = Field(..., description="The temperature of the reactor in kelvin")
    pressure: float = Field(..., description="The pressure of the reactor in atm")
    concentrationOfA: float = Field(..., description="The concentration of A in moles per cubic meters")
    concentrationOfB: float = Field(..., description="The concentration of B in moles per cubic meters")
    rateConstant: float = Field(..., description="The rate constant of the reaction in cubic meters per mole per minute")
    production: float = Field(..., description="The production of the product in moles per min")


class PlugFlowVolumeProductionTool(BaseTool):
    name = "Pfr-volume-production"
    description = """Useful for when you need to calculate the volume of a plug flow reactor, given the volumetric flow rate, Temperature, Initial Pressure,
    Initial Concentration of A, Initial Concentration of B, Rate Constant, and production rate of the product. Remember that volumetric flow rate is given in units of cubic meters per minute,
    temperature is in kelvin, initial pressure is in atm, initial concentration of A is in mol per cubic meter, initial concentration of B in mol per cubic meter, rate constant 
    in cubic meters per moles per minute, and production rate is in moles per minute."""

    def _run(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, production: float):
        return pfr_expansion_volume_production(volumetric, temperature, pressure, concentrationOfA, concentrationOfB, rateConstant, production)

    def _arun(self, volumetric: float, temperature: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, production: float):
        return NotImplementedError("This tool does not support async")

    args_schema: Type[BaseModel] = PlugFlowVolumeProductionCheckInput


class PlugFlowTemperatureConversionCheckInput(BaseModel):
    """Input schema for PlugFLowConversionProductionInput"""

    volumetric: float = Field(..., decsription="The volumetric flow rate of the feed in cubic meters per minute")
    volume: float = Field(..., description="The volume of the reactor in cubic meters")
    pressure: float = Field(..., description="The pressure of the reactor in atm")
    concentrationOfA: float = Field(..., description="The concentration of A in moles per cubic meters")
    concentrationOfB: float = Field(..., description="The concentration of B in moles per cubic meters")
    rateConstant: float = Field(..., description="The rate constant of the reaction in cubic meters per mole per minute")
    conversion: float = Field(..., description="The conversion of the limiting reactant")


class PlugFlowTemperatureConversionTool(BaseTool):
    name = "Pfr-temperature-conversion"
    description = """Useful for when you need to calculate the temperature of a plug flow reactor, given the volumetric flow rate, Temperature, Initial Pressure,
    Initial Concentration of A, Initial Concentration of B, Rate Constant, and conversion of the limiting reactant. Remember that volumetric flow rate is given in units of cubic meters per minute,
    temperature is in kelvin, initial pressure is in atm, initial concentration of A is in mol per cubic meter, initial concentration of B in mol per cubic meter, and rate constant 
    in cubic meters per moles per minute."""

    def _run(self, volumetric: float, volume: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, conversion: float):
        return pfr_expansion_temperature_conversion(volumetric, volume, pressure, concentrationOfA, concentrationOfB, rateConstant, conversion)

    def _arun(self, volumetric: float, volume: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, conversion: float):
        return NotImplementedError("This tool does not support async")

    args_schema: Type[BaseModel] = PlugFlowTemperatureConversionCheckInput


class PlugFlowTemperatureProductionCheckInput(BaseModel):
    """Input schema for PlugFLowTemperatureProductionInput"""

    volumetric: float = Field(..., decsription="The volumetric flow rate of the feed in cubic meters per minute")
    volume: float = Field(..., description="The volume of the reactor in cubic meters")
    pressure: float = Field(..., description="The pressure of the reactor in atm")
    concentrationOfA: float = Field(..., description="The concentration of A in moles per cubic meters")
    concentrationOfB: float = Field(..., description="The concentration of B in moles per cubic meters")
    rateConstant: float = Field(..., description="The rate constant of the reaction in cubic meters per mole per minute")
    production: float = Field(..., description="The production of the product in moles per min")


class PlugFlowTemperatureProductionTool(BaseTool):
    name = "Pfr-temperature-production"
    description = """Useful for when you need to calculate the temperature of a plug flow reactor, given the volumetric flow rate, Temperature, Initial Pressure,
    Initial Concentration of A, Initial Concentration of B, Rate Constant, and production rate of the product. Remember that volumetric flow rate is given in units of cubic meters per minute,
    temperature is in kelvin, initial pressure is in atm, initial concentration of A is in mol per cubic meter, initial concentration of B in mol per cubic meter, rate constant 
    in cubic meters per moles per minute, and production rate is in moles per minute."""

    def _run(self, volumetric: float, volume: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, production: float):
        return pfr_expansion_temperature_production(volumetric, volume, pressure, concentrationOfA, concentrationOfB, rateConstant, production)

    def _arun(self, volumetric: float, volume: float, pressure: float, concentrationOfA: float, concentrationOfB: float, rateConstant: float, production: float):
        return NotImplementedError("This tool does not support async")

    args_schema: Type[BaseModel] = PlugFlowTemperatureProductionCheckInput
