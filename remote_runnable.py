from langserve import RemoteRunnable

question = "The elementary gas phase reaction A+B → C is carried out in a 1.2 m^3 PFR at 1 atm and 350 K. The inlet is at 1 atm and a temperature of 350 K. The stream consists of A and B with equal concentrations of 10 mol/m^3 at a volumetric flowrate of 0.01 m^3/min. The rate constant is 0.0302 m^3/(mol.min). What is the conversion of reactant A?"

remote_chain = RemoteRunnable("http://localhost:8000")
print(remote_chain.invoke({
    "input": question,
    "chat_history": []
}))