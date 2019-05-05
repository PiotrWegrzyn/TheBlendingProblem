from pulp import *
import re

class BlendingProblem():
    def __init__(self):
        self.problem = pulp.LpProblem("The Blending Problem", pulp.LpMinimize)
        self.var_names = []
        self.variables = []
        self.objective_function = 0

    def set_vars_to_optimize(self):
        self.get_var_to_optimize_names()
        self.create_vars_to_optimize()

    def get_var_to_optimize_names(self):
        var_names = "s1,s2,s3"    # self.get_var_names_from_user()
        self.var_names = var_names.split(",")

    def get_var_names_from_user(self):
        return input("Input optimized variable names")

    def create_vars_to_optimize(self):
        for name in self.var_names:
            self.variables.append(pulp.LpVariable(name, lowBound=0))

    def get_obj_fun_from_user(self):
        return input("Objective function:")

    def set_objective_function(self, obj_fun_string):
        self.objective_function = self.string_to_function(obj_fun_string)
        self.problem += self.objective_function

    def string_to_function(self, function_string):
        fun = 0
        expressions = self.get_expressions(function_string)
        for expr in expressions:
            fun = self.add_expression(fun, expr)
        return fun

    def get_expressions(self, obj_fun_string):
        expression_strings = obj_fun_string.replace(" ", "").split("+")
        expressions = [(e.split("*")) for e in expression_strings]
        return expressions

    def add_expression(self, fun, expression):
        if len(expression) > 1:
            factor = float(expression[0])
            var_name = expression[1]
            try:
                variable = self.get_var_by_name(var_name)
                fun += factor * variable
            except NameError:
                print("No variable named: " + var_name + " found.")
        if len(expression) is 1:
            try:
                factor = float(expression[0])
                fun += factor
            except ValueError:
                try:
                    var_name = expression[0]
                    variable = self.get_var_by_name(var_name)
                    fun += 1 * variable
                except NameError:
                    print("No variable named: " + expression[0] + " found.")
        return fun

    def get_var_by_name(self, name):
        for var in self.variables:
            var_name = pulp.LpVariable.getName(var)
            if var_name == name:
                return var
        raise NameError

    def get_constraint_from_user(self):
        return input("Enter constraint")

    def add_constraint(self, constraint_string):
        constraint = self.transform_string_to_constraint(constraint_string)
        self.problem += constraint

    def transform_string_to_constraint(self, constraint_string):
        equality_symbol = self.get_equality_symbol(constraint_string)

        left_side_string = constraint_string.split(equality_symbol)[0]
        left_side = self.string_to_function(left_side_string)

        right_side_string = constraint_string.split(equality_symbol)[1]
        right_side = self.string_to_function(right_side_string)

        constraint = self.construct_constraint(left_side,equality_symbol,right_side)
        return constraint

    def get_equality_symbol(self, constraint_string):
        return re.findall(r"<=|==|>=|!=", constraint_string)[0]

    def construct_constraint(self, left_side, equality_symbol, right_side):
        if equality_symbol == "<=":
            return left_side <= right_side
        if equality_symbol == "==":
            return left_side == right_side
        if equality_symbol == ">=":
            return left_side >= right_side
        if equality_symbol == "!=":
            return left_side != right_side


if __name__ == "__main__":
    bp = BlendingProblem()
    bp.set_vars_to_optimize()
    objective_fun = "5*s1 + 3*s2 + 4*s3"  # runner.get_obj_fun_from_user()
    bp.set_objective_function(objective_fun)
    bp.add_constraint(" 0.026*s1 + 0.021*s2 + 0.021*s3 >= 10.2")
    bp.add_constraint("0.004*s1 + 0.009*s2 + 0.006*s3 >= 2.4")
    bp.add_constraint("0.006*s1 + 0.002*s2 + 0.006*s3 >= 2.7")
    bp.add_constraint("0.006*s1 + 0.002*s2 + 0.006*s3 <= 4")
    bp.add_constraint("2*s1 == s3")
    bp.problem.solve()
    print("Optimal Result:")
    for var in bp.problem.variables():
        print(var.name, "=", var.varValue)
    print("Total min cost:")
    print(value(bp.problem.objective))

