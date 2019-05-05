import kivy
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

kivy.require('1.8.0')
from kivy.app import App
from BlendingProblem import BlendingProblem


class BlendingProblemApp(App):

    def __init__(self):
        super(BlendingProblemApp, self).__init__()
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (800, 500)
        self.initial = True
        self.blending_problem = BlendingProblem()

    def build(self):
        self.root = GridLayout(cols=2)
        self.main_box = BoxLayout(orientation="vertical")
        self.constraints_box = BoxLayout(orientation="vertical")
        self.root.add_widget(self.main_box)
        self.root.add_widget(self.constraints_box)
        self.show_variables_input()
        self.show_function_input()

        return self.root

    def show_variables_input(self):
        # self.variables_input = TextInput(text='Enter variables', multiline=False)
        self.variables_input = TextInput(size_hint=(1, 0.2), hint_text='s1,s2,s3', multiline=False)
        self.variables_input.bind(on_text_validate=self.on_enter_variables_input)
        self.main_box.add_widget(self.variables_input)

    def on_enter_variables_input(self, instance):
        print('variables:', instance.text)
        variables = instance.text
        self.blending_problem.set_variables(variables)

    def show_function_input(self):
        # self.function_input = TextInput(text='Enter Object Function', multiline=False)
        self.function_input = TextInput(size_hint=(1, 0.2), hint_text='s1*5 + 3*s2 + 4*s3', multiline=False)
        self.function_input.bind(on_text_validate=self.on_enter_function_input)
        self.main_box.add_widget(self.function_input)

    def on_enter_function_input(self, instance):
        print('Object Function:', instance.text)
        # objective_fun = "s1*5 + 3*s2 + 4*s3"
        objective_fun = instance.text
        self.blending_problem.set_objective_function(objective_fun)
        if self.initial is True:
            self.show_constraint_input()
            self.show_solve_button()
            self.show_clear_button()
            self.initial = False

    def show_constraint_input(self):
        # self.constraint_input = TextInput(text='Enter constraint', multiline=False)
        self.constraint_input = TextInput(size_hint=(1, 0.2), hint_text=' 0.026*s1 + 0.021*s2 + 0.021*s3 >= 10.2', multiline=False)
        self.constraint_input.bind(on_text_validate=self.on_enter_constraint_input)
        self.constraints_box.add_widget(self.constraint_input)

    def on_enter_constraint_input(self, instance):
        print('constraint:', instance.text)
        constraint = instance.text
        self.blending_problem.add_constraint(constraint)
        self.show_constraint_input()

    def show_solve_button(self):
        self.solve_button = Button(size_hint=(1, 0.2),text='Solve')
        self.solve_button.bind(on_press=self.solve_button_callback)
        self.main_box.add_widget(self.solve_button)

    def solve_button_callback(self, btn_instance):
        self.blending_problem.solve()
        self.blending_problem.print_results()

    def show_clear_button(self):
        self.clear_button = Button(size_hint=(1, 0.2), text='Clear')
        self.clear_button.bind(on_press=self.clear_button_callback)
        self.main_box.add_widget(self.clear_button)

    def clear_button_callback(self, btn_instance):
        self.blending_problem = BlendingProblem()
        self.main_box.clear_widgets()
        self.constraints_box.clear_widgets()
        self.show_variables_input()
        self.show_function_input()
        self.initial = True


if __name__ == '__main__':
    BlendingProblemApp().run()