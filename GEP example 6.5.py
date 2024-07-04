from pyomo.environ import *
from pyomo.opt import SolverFactory
import itertools

import pandas as pd

model = ConcreteModel()

# 5D Array
model.gen = Set(initialize=[1, 2])  # Generators
model.timePeriods = Set(initialize=[1, 2, 3])  # Time periods
model.demandScenario_1 = Set(initialize=[1, 2, 3, 4])  # Demand scenario for time period 1
model.demandScenario_2 = Set(initialize=[1, 2, 3, 4])  # Demand scenario for time period 2
model.demandScenario_3 = Set(initialize=[1, 2, 3, 4])  # Demand scenario for time period 3
model.A1 = Set(initialize=[1, 2, 3, 4])  # Availability scenarios for Generator 1
model.A2 = Set(initialize=[1, 2, 3, 4, 5])  # Availability scenarios for Generator 2

# Total Scenarios
model.totalScenarios = Set(dimen=5, initialize=lambda model: {(i, j, k, l, m) 
                                                         for i in model.demandScenario_1
                                                         for j in model.demandScenario_2 
                                                         for k in model.demandScenario_3 
                                                         for l in model.A1 
                                                         for m in model.A2})
file_path = 'cap_expan_data_7.xlsx'
sheet_name = 'DIC'  # Specify the sheet name or sheet number

# Load the data into a pandas DataFrame
df = pd.read_excel(file_path, sheet_name=sheet_name)
c = {}
for i in range(0,df.shape[0]):
    c[df['Generator'][i]] = df['Ammortized Fixed operating cost($)'][i]
model.c = Param(model.gen, initialize=c)  # Fixed cost per unit capacity of generator j

sheet_name = 'FIXOP'  # Specify the sheet name or sheet number

# Load the data into a pandas DataFrame
df = pd.read_excel(file_path, sheet_name=sheet_name)
f = {}
for i in range(0,df.shape[0]):
    f[(df['Generator'][i],df['time'][i])] = df['FIXOP'][i]
model.f = Param(model.gen,model.timePeriods, initialize=f)  

sheet_name = 'Additional cost'  # Specify the sheet name or sheet number

df = pd.read_excel(file_path, sheet_name=sheet_name)
g = {}
for i in range(0,df.shape[0]):
    g[df['Time'][i]] = df['Cost'][i]
model.g = Param(model.timePeriods, initialize=g)


prob = {}
prob['Demand_time_1'] = {}
prob['Demand_time_2'] = {}
prob['Demand_time_3'] = {}
prob['A1'] = {}
prob['A2'] = {}

d = {}

sheet_name = 'Demand' 
df = pd.read_excel(file_path, sheet_name=sheet_name)
for i in range(0,df.shape[0]):
    if(df['Time'][i]==1):
       prob['Demand_time_1'][df['Scenario'][i]] = df['Probability'][i]
       for j in range(1,5):
            for k in range(1,5):
                for m in range(1,5):
                    for n in range(1,6):
                        d[df['Time'][i],(df['Scenario'][i],j,k,m,n)]= df['Demand (KWh)'][i]
                        
                
    elif(df['Time'][i]==2):
       prob['Demand_time_2'][df['Scenario'][i]] = df['Probability'][i]
       for j in range(1,5):
            for k in range(1,5):
                for m in range(1,5):
                    for n in range(1,6):
                        d[df['Time'][i],(j,df['Scenario'][i],k,m,n)]= df['Demand (KWh)'][i]
    else:
       prob['Demand_time_3'][df['Scenario'][i]] = df['Probability'][i]
       for j in range(1,5):
            for k in range(1,5):
                for m in range(1,5):
                    for n in range(1,6):
                        d[df['Time'][i],(j,k,df['Scenario'][i],m,n)]= df['Demand (KWh)'][i]
                    
model.d = Param(model.timePeriods,model.totalScenarios, initialize=d)  

                        
    
a = {}    
sheet_name = 'Gen1_availibility' 
df = pd.read_excel(file_path, sheet_name=sheet_name)
for i in range(0,df.shape[0]):
    prob['A1'][df['Scenario'][i]] =  df['Probability'][i]
    for j in range(1,5):
            for k in range(1,5):
                for m in range(1,5):
                    for n in range(1,6):
                        a[1,(j,k,m,df['Scenario'][i],n)]= df['Availibility'][i]
    
    
sheet_name = 'Gen2_availiability' 
df = pd.read_excel(file_path, sheet_name=sheet_name)
for i in range(0,df.shape[0]):
    prob['A2'][df['Scenario'][i]] =  df['Probability'][i]
    for j in range(1,5):
            for k in range(1,5):
                for m in range(1,5):
                    for n in range(1,5):
                        a[2,(j,k,m,n,df['Scenario'][i])]= df['Availibility'][i]
                        
model.a = Param(model.gen, model.totalScenarios, initialize=a) 

    

p  = {}
for i in prob['Demand_time_1'].keys():
    for j in prob['Demand_time_2'].keys():
        for k in prob['Demand_time_3'].keys():
            for m in prob['A1'].keys():
                for n in prob['A2'].keys():
                    p[i,j,k,m,n] = prob['Demand_time_1'][i]*prob['Demand_time_2'][j]*prob['Demand_time_3'][k]*prob['A1'][m]*prob['A2'][n]

model.p = Param(model.demandScenario_1,model.demandScenario_2,model.demandScenario_1,model.A1,model.A2, initialize=p)  # Fixed cost per unit capacity of generator j    
# Variables
model.x = Var(model.gen, domain=NonNegativeReals)  # Installed capacity of generator j
model.y = Var(model.totalScenarios, model.timePeriods, model.gen, domain=NonNegativeReals)  # Operating level of generator j
model.y_purchased = Var(model.totalScenarios, model.timePeriods, domain=NonNegativeReals)  # Additional capacity purchased
# Objective function
def objective_rule(model):
    fixed_cost = sum(model.c[j] * model.x[j] for j in model.gen)
    operating_cost = sum(model.p[a,b,c,d,e]*sum(sum(model.f[j,i] * model.y[(a, b, c, d, e), i, j] for j in model.gen) + model.g[i] * model.y_purchased[(a, b, c, d, e), i] for i in model.timePeriods) for (a, b, c, d, e) in model.totalScenarios )
    return fixed_cost + operating_cost

model.obj = Objective(rule=objective_rule, sense=minimize)

# Constraints

# Demand satisfaction constraints
def demand_satisfaction_rule(model, i, j, k, l, m, t):
    return sum(model.y[(i, j, k, l, m), t, gen] for gen in model.gen) + model.y_purchased[(i, j, k, l, m), t] >= model.d[t,(i, j, k, l, m)]
model.demand_satisfaction_constraint = Constraint(model.totalScenarios, model.timePeriods, rule=demand_satisfaction_rule)

# Availability constraints
def availability_rule(model, i, j, k, l, m, t, gen):
    return model.y[(i, j, k, l, m), t, gen] <= model.a[gen,(i, j, k, l, m)] * model.x[gen]
model.availability_constraint = Constraint(model.totalScenarios, model.timePeriods, model.gen, rule=availability_rule)

opt = SolverFactory('gurobi')
results = opt.solve(model, tee=True)


model.display()


file_path = 'model_pprint_TEST2.txt'      
with open(file_path, 'w') as file: 
    model.pprint(ostream=file)

#model.pprint()