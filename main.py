from pulp import *
S1 = pulp.LpVariable("s1", lowBound=0)
S2 = pulp.LpVariable("s2", lowBound=0)
S3 = pulp.LpVariable("s3", lowBound=0)
problem = pulp.LpProblem("The Blending Problem", pulp.LpMinimize)
problem += 5*S1 + 3*S2 + 4*S3, "The objective function"
problem += 0.026*S1 + 0.021*S2 + 0.021*S3 >= 10.2, "SI"
problem += 0.004*S1 + 0.009*S2 + 0.006*S3 >= 2.4, "MN"
problem += 0.006*S1 + 0.002*S2 + 0.006*S3 >= 2.7, "Pmin"
problem += 0.006*S1 + 0.002*S2 + 0.006*S3 <= 4, "Pmax"
problem += S1*2 == S3, "3rd constraint"
problem.solve()
print ("Optimal Result:")
for variable in problem.variables():
    print (variable.name, "=", variable.varValue)
print("Total min cost:")
print(value(problem.objective))
