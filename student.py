class Student:
    def __init__(self, f_name, l_name, department):
        self.f_name = f_name
        self.l_name =  l_name
        self.department = department
        
    def __str__(self):
        return (f"{self.f_name} {self.l_name}")
