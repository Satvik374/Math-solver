import sympy as sp
import numpy as np
from sympy import symbols, solve, diff, integrate, simplify, expand, factor, limit, series
from sympy.parsing.sympy_parser import parse_expr
from sympy.plotting import plot
import matplotlib.pyplot as plt
import re

class MathSolver:
    def __init__(self):
        """Initialize the math solver"""
        pass
        
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
            
            # Check if this is a simple calculation (not an equation to solve)
            if self._is_simple_calculation(cleaned_problem):
                return self._evaluate_expression(cleaned_problem)
            
            # Route to appropriate solver based on problem type
            if problem_type == "Algebra" or "solve" in cleaned_problem.lower():
                return self._solve_algebraic(cleaned_problem)
            elif problem_type == "Calculus" or any(keyword in cleaned_problem.lower() for keyword in ["derivative", "differentiate", "d/dx"]):
                return self._solve_calculus_derivative(cleaned_problem)
            elif problem_type == "Calculus" or any(keyword in cleaned_problem.lower() for keyword in ["integrate", "integral", "∫"]):
                return self._solve_calculus_integral(cleaned_problem)
            elif self._is_system_of_equations(cleaned_problem):
                return self._solve_system_of_equations(cleaned_problem)
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
        # Convert to string and strip whitespace
        text = str(text).strip()
        
        # Remove any non-printable characters
        text = ''.join(char for char in text if char.isprintable() or char.isspace())
        
        # Handle command words that precede expressions
        text = re.sub(r'^calculate\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^what is\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^find\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^solve\s+', '', text, flags=re.IGNORECASE)
        
        # Replace common mathematical notations
        text = text.replace("^", "**")  # Convert power notation
        text = text.replace("÷", "/")   # Division symbol
        text = text.replace("×", "*")   # Multiplication symbol
        text = text.replace("π", "pi")  # Pi symbol
        text = text.replace("∞", "oo")  # Infinity symbol
        text = re.sub(r'√\(([^)]+)\)', r'sqrt(\1)', text)  # Convert √ to sqrt for parsing
        
        # Handle common input formats
        text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)  # Add multiplication: 2x -> 2*x
        text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)  # Add multiplication: x2 -> x*2
        text = re.sub(r'\)\(', ')*(', text)  # Add multiplication between parentheses
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        return text
    
    def _is_simple_calculation(self, problem_text):
        """Check if this is a simple calculation rather than an equation to solve"""
        # If no equals sign and no variables, it's likely a calculation
        if "=" not in problem_text and not re.search(r'\b[a-zA-Z]\b', problem_text):
            # Check if it contains only numbers and operators
            if re.match(r'^[\d\+\-\*/\(\)\.\s]+$', problem_text):
                return True
        return False
    
    def _evaluate_expression(self, expression_text):
        """Evaluate a simple mathematical expression"""
        try:
            expr = parse_expr(expression_text)
            result = float(expr.evalf())
            
            steps = [
                f"Evaluating: {expression_text}",
                f"Result: {result}"
            ]
            
            return {
                "steps": steps,
                "answer": str(result),
                "type": "calculation"
            }
            
        except Exception as e:
            return {"error": f"Could not evaluate expression: {str(e)}"}
    
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
            equation_str = problem_text.strip()
            var_str = 'x'
            
            # Handle "solve ... for variable" pattern
            for_match = re.search(r'\s+for\s+(\w+)$', problem_text.lower())
            if for_match:
                var_str = for_match.group(1)
                # Remove the "for variable" part from the equation
                equation_str = re.sub(r'\s+for\s+\w+$', '', problem_text, flags=re.IGNORECASE).strip()
            
            # Remove "solve" from the beginning if present
            equation_str = re.sub(r'^solve\s+', '', equation_str, flags=re.IGNORECASE).strip()
            
            # Validate that we have something to work with
            if not equation_str:
                return {"error": "No equation provided to solve. Please enter a mathematical equation."}
            
            # Clean up the equation string
            equation_str = equation_str.replace('^', '**')
            
            # Parse the expression
            if '=' in equation_str:
                left, right = equation_str.split('=', 1)
                try:
                    left_expr = parse_expr(left.strip())
                    right_expr = parse_expr(right.strip())
                    equation = left_expr - right_expr
                except Exception as parse_error:
                    return {"error": f"Failed to parse equation '{equation_str}': {str(parse_error)}. Please check your equation format."}
            else:
                try:
                    equation = parse_expr(equation_str)
                except Exception as parse_error:
                    return {"error": f"Failed to parse expression '{equation_str}': {str(parse_error)}. Please check your equation format."}
            
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
            # Handle "for variable" pattern like in _solve_algebraic
            equation_str = equation_text.strip()
            var_str = 'x'
            
            # Handle "solve ... for variable" pattern
            for_match = re.search(r'\s+for\s+(\w+)$', equation_text.lower())
            if for_match:
                var_str = for_match.group(1)
                # Remove the "for variable" part from the equation
                equation_str = re.sub(r'\s+for\s+\w+$', '', equation_text, flags=re.IGNORECASE).strip()
            
            if '=' not in equation_str:
                return {"error": "No equation found (missing '=' sign)"}
            
            left, right = equation_str.split('=', 1)
            try:
                left_expr = parse_expr(left.strip())
                right_expr = parse_expr(right.strip())
            except Exception as parse_error:
                return {"error": f"Failed to parse equation '{equation_str}': {str(parse_error)}. Please check your equation format."}
            
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
                f"Original equation: {equation_str}",
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
    
    def _is_system_of_equations(self, problem_text):
        """Check if the problem contains a system of equations"""
        # Look for multiple equations separated by commas or "and"
        if ',' in problem_text and '=' in problem_text:
            equations = problem_text.split(',')
            equation_count = sum(1 for eq in equations if '=' in eq.strip())
            return equation_count >= 2
        return False
    
    def _solve_system_of_equations(self, problem_text):
        """Solve a system of equations"""
        try:
            # Split equations by comma
            equation_strings = [eq.strip() for eq in problem_text.split(',')]
            equations = []
            variables = set()
            
            steps = ["System of equations:"]
            
            # Parse each equation
            for i, eq_str in enumerate(equation_strings, 1):
                if '=' not in eq_str:
                    continue
                    
                left, right = eq_str.split('=', 1)
                try:
                    left_expr = parse_expr(left.strip())
                    right_expr = parse_expr(right.strip())
                    equation = left_expr - right_expr
                    equations.append(equation)
                    variables.update(equation.free_symbols)
                    steps.append(f"Equation {i}: {eq_str}")
                except Exception as parse_error:
                    return {"error": f"Failed to parse equation '{eq_str}': {str(parse_error)}"}
            
            if not equations:
                return {"error": "No valid equations found in the system"}
            
            if not variables:
                return {"error": "No variables found in the system"}
            
            # Solve the system
            try:
                solutions = solve(equations, list(variables))
                steps.append(f"Solving for variables: {', '.join(str(v) for v in variables)}")
                
                if not solutions:
                    return {
                        "steps": steps + ["No solution exists for this system"],
                        "answer": "No solution",
                        "type": "system_of_equations"
                    }
                
                # Format the solution
                if isinstance(solutions, dict):
                    # Single solution
                    answer_parts = []
                    for var, value in solutions.items():
                        answer_parts.append(f"{var} = {value}")
                        steps.append(f"{var} = {value}")
                    
                    answer = ", ".join(answer_parts)
                    
                elif isinstance(solutions, list):
                    # Multiple solutions
                    answer_parts = []
                    for i, sol in enumerate(solutions):
                        if isinstance(sol, dict):
                            sol_str = ", ".join(f"{var} = {value}" for var, value in sol.items())
                        else:
                            sol_str = str(sol)
                        answer_parts.append(f"Solution {i+1}: {sol_str}")
                        steps.append(f"Solution {i+1}: {sol_str}")
                    
                    answer = "; ".join(answer_parts)
                
                else:
                    answer = str(solutions)
                    steps.append(f"Solution: {answer}")
                
                return {
                    "steps": steps,
                    "answer": answer,
                    "type": "system_of_equations"
                }
                
            except Exception as solve_error:
                return {
                    "error": f"Failed to solve system: {str(solve_error)}",
                    "steps": steps + [f"Error: {str(solve_error)}"],
                    "type": "system_of_equations"
                }
                
        except Exception as e:
            return {"error": f"System solving error: {str(e)}"}
