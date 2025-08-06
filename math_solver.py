import sympy as sp
import numpy as np
from sympy import symbols, solve, diff, integrate, simplify, expand, factor, limit, series
from sympy.parsing.sympy_parser import parse_expr
from sympy.plotting import plot
import matplotlib.pyplot as plt
import re

class MathSolver:
    def __init__(self):
        """Initialize the math solver with common symbols"""
        self.x, self.y, self.z = symbols('x y z')
        self.t = symbols('t')
        self.common_symbols = [self.x, self.y, self.z, self.t]
        
    def solve_problem(self, problem_text, problem_type="Auto-detect"):
        """
        Main method to solve mathematical problems
        """
        try:
            # Clean and preprocess the input
            cleaned_problem = self._preprocess_input(problem_text)
            
            # Determine the type of problem if auto-detect is selected
            if problem_type == "Auto-detect":
                problem_type = self._detect_problem_type(cleaned_problem)
            
            # Route to appropriate solver based on problem type
            if problem_type == "Algebra" or "solve" in cleaned_problem.lower():
                return self._solve_algebraic(cleaned_problem)
            elif problem_type == "Calculus" or any(keyword in cleaned_problem.lower() for keyword in ["derivative", "differentiate", "d/dx"]):
                return self._solve_calculus_derivative(cleaned_problem)
            elif problem_type == "Calculus" or any(keyword in cleaned_problem.lower() for keyword in ["integrate", "integral", "∫"]):
                return self._solve_calculus_integral(cleaned_problem)
            elif problem_type == "Direct Equation" or "=" in cleaned_problem:
                return self._solve_equation(cleaned_problem)
            else:
                # Try to parse as a general expression
                return self._solve_general_expression(cleaned_problem)
                
        except Exception as e:
            return {
                "error": str(e),
                "steps": [f"Error processing problem: {str(e)}"],
                "answer": "Could not solve the problem"
            }
    
    def _preprocess_input(self, text):
        """Clean and preprocess the input text"""
        # Replace common mathematical notations
        text = text.replace("^", "**")  # Convert power notation
        text = text.replace("÷", "/")   # Division symbol
        text = text.replace("×", "*")   # Multiplication symbol
        text = text.replace("π", "pi")  # Pi symbol
        text = text.replace("∞", "oo")  # Infinity symbol
        text = text.replace("**", "**") # Ensure power notation is consistent
        
        # Handle common input formats
        text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)  # Add multiplication: 2x -> 2*x
        text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)  # Add multiplication: x2 -> x*2
        text = re.sub(r'\)\(', ')*(', text)  # Add multiplication between parentheses
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        return text
    
    def _detect_problem_type(self, problem_text):
        """Detect the type of mathematical problem"""
        problem_lower = problem_text.lower()
        
        if any(keyword in problem_lower for keyword in ["derivative", "differentiate", "d/dx", "derive"]):
            return "Calculus"
        elif any(keyword in problem_lower for keyword in ["integrate", "integral", "∫", "antiderivative"]):
            return "Calculus"
        elif any(keyword in problem_lower for keyword in ["solve", "find x", "find y"]):
            return "Algebra"
        elif "=" in problem_text:
            return "Direct Equation"
        else:
            return "Algebra"
    
    def _solve_algebraic(self, problem_text):
        """Solve algebraic problems"""
        try:
            # Extract equation from text
            equation_match = re.search(r'solve\s+(.+?)(?:\s+for\s+(\w+))?$', problem_text.lower())
            if equation_match:
                equation_str = equation_match.group(1).strip()
                var_str = equation_match.group(2) if equation_match.group(2) else 'x'
            else:
                equation_str = problem_text.strip()
                var_str = 'x'
            
            # Clean up the equation string
            equation_str = equation_str.replace('^', '**')
            
            # Parse the expression
            if '=' in equation_str:
                left, right = equation_str.split('=', 1)
                left_expr = parse_expr(left.strip())
                right_expr = parse_expr(right.strip())
                equation = left_expr - right_expr
            else:
                equation = parse_expr(equation_str)
            
            # Get the variable to solve for
            var = symbols(var_str)
            
            # Solve the equation
            solutions = solve(equation, var)
            
            steps = [
                f"Original problem: {problem_text}",
                f"Equation to solve: {equation_str}",
                f"Rearranged as: {equation} = 0",
                f"Solving for {var_str}..."
            ]
            
            if solutions:
                steps.append(f"Solutions found: {solutions}")
                answer = f"{var_str} = {solutions}"
            else:
                steps.append("No real solutions found")
                answer = "No real solutions"
            
            return {
                "steps": steps,
                "answer": answer,
                "solutions": solutions,
                "type": "algebraic"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _solve_equation(self, equation_text):
        """Solve direct equations"""
        try:
            if '=' not in equation_text:
                return {"error": "No equation found (missing '=' sign)"}
            
            left, right = equation_text.split('=')
            left_expr = parse_expr(left.strip())
            right_expr = parse_expr(right.strip())
            
            equation = left_expr - right_expr
            
            # Find all symbols in the equation
            free_symbols = equation.free_symbols
            
            if not free_symbols:
                # No variables, just check if equation is true
                result = left_expr.equals(right_expr)
                return {
                    "steps": [f"Evaluating: {left.strip()} = {right.strip()}"],
                    "answer": f"The equation is {'True' if result else 'False'}",
                    "type": "evaluation"
                }
            
            # Solve for each variable
            solutions = {}
            for var in free_symbols:
                var_solutions = solve(equation, var)
                if var_solutions:
                    solutions[str(var)] = var_solutions
            
            steps = [
                f"Original equation: {equation_text}",
                f"Rearranged as: {equation} = 0"
            ]
            
            if solutions:
                for var, sols in solutions.items():
                    steps.append(f"Solutions for {var}: {sols}")
                answer = "; ".join([f"{var} = {sols}" for var, sols in solutions.items()])
            else:
                steps.append("No solutions found")
                answer = "No solutions"
            
            return {
                "steps": steps,
                "answer": answer,
                "solutions": solutions,
                "type": "equation"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _solve_calculus_derivative(self, problem_text):
        """Solve calculus derivative problems"""
        try:
            # Extract function from text
            func_match = re.search(r'(?:derivative of|differentiate|d/dx)\s*(.+?)(?:\s+with respect to\s+(\w+))?$', problem_text.lower())
            if func_match:
                func_str = func_match.group(1)
                var_str = func_match.group(2) if func_match.group(2) else 'x'
            else:
                func_str = problem_text
                var_str = 'x'
            
            # Parse the function
            func = parse_expr(func_str)
            var = symbols(var_str)
            
            # Calculate derivative
            derivative = diff(func, var)
            simplified_derivative = simplify(derivative)
            
            steps = [
                f"Find the derivative of: f({var_str}) = {func}",
                f"Using differentiation rules...",
                f"f'({var_str}) = {derivative}",
                f"Simplified: f'({var_str}) = {simplified_derivative}"
            ]
            
            return {
                "steps": steps,
                "answer": f"f'({var_str}) = {simplified_derivative}",
                "derivative": simplified_derivative,
                "original_function": func,
                "type": "derivative"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _solve_calculus_integral(self, problem_text):
        """Solve calculus integral problems"""
        try:
            # Extract function from text
            func_match = re.search(r'(?:integrate|integral of)\s*(.+?)(?:\s+d(\w+)|\s+with respect to\s+(\w+))?$', problem_text.lower())
            if func_match:
                func_str = func_match.group(1)
                var_str = func_match.group(2) or func_match.group(3) or 'x'
            else:
                func_str = problem_text.replace("∫", "").strip()
                var_str = 'x'
            
            # Parse the function
            func = parse_expr(func_str)
            var = symbols(var_str)
            
            # Calculate integral
            integral_result = integrate(func, var)
            
            steps = [
                f"Find the integral of: ∫ {func} d{var_str}",
                f"Using integration rules...",
                f"∫ {func} d{var_str} = {integral_result} + C"
            ]
            
            return {
                "steps": steps,
                "answer": f"∫ {func} d{var_str} = {integral_result} + C",
                "integral": integral_result,
                "original_function": func,
                "type": "integral"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _solve_general_expression(self, problem_text):
        """Solve general mathematical expressions"""
        try:
            expr = parse_expr(problem_text)
            
            # Try to simplify
            simplified = simplify(expr)
            
            # Try to factor
            try:
                factored = factor(expr)
            except:
                factored = None
            
            # Try to expand
            try:
                expanded = expand(expr)
            except:
                expanded = None
            
            steps = [f"Original expression: {expr}"]
            
            if simplified != expr:
                steps.append(f"Simplified: {simplified}")
            
            if factored and factored != expr:
                steps.append(f"Factored: {factored}")
            
            if expanded and expanded != expr:
                steps.append(f"Expanded: {expanded}")
            
            # Evaluate if expression has no variables
            if not expr.free_symbols:
                try:
                    numeric_value = float(expr.evalf())
                    steps.append(f"Numerical value: {numeric_value}")
                    answer = f"{numeric_value}"
                except:
                    answer = f"{simplified}"
            else:
                answer = f"{simplified}"
            
            return {
                "steps": steps,
                "answer": answer,
                "simplified": simplified,
                "factored": factored,
                "expanded": expanded,
                "type": "general"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def create_plot(self, expression, variable='x', x_range=(-10, 10)):
        """Create a plot for mathematical expressions"""
        try:
            var = symbols(variable)
            expr = parse_expr(str(expression))
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Generate x values
            x_vals = np.linspace(x_range[0], x_range[1], 1000)
            
            # Convert sympy expression to numpy function
            func = sp.lambdify(var, expr, 'numpy')
            y_vals = func(x_vals)
            
            # Plot
            ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'y = {expr}')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            ax.set_xlabel(variable)
            ax.set_ylabel('y')
            ax.set_title(f'Graph of y = {expr}')
            ax.legend()
            
            return fig
            
        except Exception as e:
            return None
