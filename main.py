class Department:
    def __init__(self, name, manager):
        self.name = name
        self.manager = manager
        self.subdepartments = []
    

def find_managers(root: Department, dept_name: str):
    def dfs(node: Department):
        if node.name == dept_name:
            return [node.manager]

        for subdept in node.subdepartments:
            result = dfs(subdept)
            if result:
                return result + [node.manager]
            
        return None

    result = dfs(root)
    return result if result else []

# Create the company hierarchy
ceo = Department("CEO", "Alice")
engineering = Department("Engineering", "Bob")
sales = Department("Sales", "Charlie")
backend = Department("Backend", "David")
frontend = Department("Frontend", "Eve")
domestic = Department("Domestic", "Fay")


ceo.subdepartments = [engineering, sales]
engineering.subdepartments = [backend, frontend]
sales.subdepartments = [domestic]

print(find_managers(ceo, "Engineering"))