import sympy as sp
import matplotlib.pyplot as plt
import re
from math_solver import MathSolver

class SolutionFormatter:
    def __init__(self):
        """Initialize the solution formatter"""
        self.solver = MathSolver()
    
    def format_solution(self, solution_data):
        """Format the solution data for display"""
        if not solution_data or "error" in solution_data:
            return {
                "steps": ["Error: Could not solve the problem"],
                "answer": "No solution found",
                "error": solution_data.get("error", "Unknown error") if solution_data else "No solution data"
            }
        
        formatted_result = {
            "steps": [self._format_math_symbols(step) for step in solution_data.get("steps", [])],
            "answer": self._format_math_symbols(solution_data.get("answer", "")),
            "info": [],
            "plot": None
        }
        
        # Add type-specific formatting
        problem_type = solution_data.get("type", "general")
        
        if problem_type == "algebraic":
            formatted_result = self._format_algebraic_solution(solution_data, formatted_result)
        elif problem_type == "equation":
            formatted_result = self._format_equation_solution(solution_data, formatted_result)
        elif problem_type == "derivative":
            formatted_result = self._format_derivative_solution(solution_data, formatted_result)
        elif problem_type == "integral":
            formatted_result = self._format_integral_solution(solution_data, formatted_result)
        elif problem_type == "system_of_equations":
            formatted_result = self._format_system_solution(solution_data, formatted_result)
        elif problem_type == "general":
            formatted_result = self._format_general_solution(solution_data, formatted_result)
        
        return formatted_result
    
    def _format_algebraic_solution(self, solution_data, formatted_result):
        """Format algebraic problem solutions"""
        solutions = solution_data.get("solutions", [])
        
        if solutions:
            # Add solution verification
            formatted_result["info"].append(f"Found {len(solutions)} solution(s)")
            
            # Add solution types
            for i, sol in enumerate(solutions):
                if sol.is_real:
                    formatted_result["info"].append(f"Solution {i+1}: {sol} (Real number)")
                else:
                    formatted_result["info"].append(f"Solution {i+1}: {sol} (Complex number)")
        
        return formatted_result
    
    def _format_equation_solution(self, solution_data, formatted_result):
        """Format equation solutions"""
        solutions = solution_data.get("solutions", {})
        
        if solutions:
            for var, sols in solutions.items():
                formatted_result["info"].append(f"Variable '{var}' has {len(sols)} solution(s)")
                
                # Check for special solution types
                for sol in sols:
                    if sol == 0:
                        formatted_result["info"].append(f"'{var} = 0' is a trivial solution")
                    elif sol.is_rational:
                        formatted_result["info"].append(f"'{var} = {sol}' is a rational solution")
        
        return formatted_result
    
    def _format_derivative_solution(self, solution_data, formatted_result):
        """Format calculus derivative solutions"""
        derivative = solution_data.get("derivative")
        original_function = solution_data.get("original_function")
        
        if derivative and original_function:
            # Add derivative rules used
            formatted_result["info"].append("Derivative calculated using standard differentiation rules")
            
            # Check for critical points
            try:
                critical_points = sp.solve(derivative, sp.symbols('x'))
                if critical_points:
                    formatted_result["info"].append(f"Critical points (where f'(x) = 0): {critical_points}")
            except:
                pass
            
            # Try to create a plot
            try:
                plot_fig = self.solver.create_plot(original_function)
                if plot_fig:
                    formatted_result["plot"] = plot_fig
            except:
                pass
        
        return formatted_result
    
    def _format_integral_solution(self, solution_data, formatted_result):
        """Format calculus integral solutions"""
        integral = solution_data.get("integral")
        original_function = solution_data.get("original_function")
        
        if integral and original_function:
            # Add integration information
            formatted_result["info"].append("Integral calculated using standard integration rules")
            formatted_result["info"].append("Don't forget the constant of integration (+C)")
            
            # Check if it's a definite integral
            if hasattr(integral, 'free_symbols') and not integral.free_symbols:
                formatted_result["info"].append("This appears to be a definite integral (numerical result)")
            
            # Try to create a plot of the original function
            try:
                plot_fig = self.solver.create_plot(original_function)
                if plot_fig:
                    formatted_result["plot"] = plot_fig
            except:
                pass
        
        return formatted_result
    
    def _format_general_solution(self, solution_data, formatted_result):
        """Format general expression solutions"""
        simplified = solution_data.get("simplified")
        factored = solution_data.get("factored")
        expanded = solution_data.get("expanded")
        
        # Add information about different forms
        if factored and factored != simplified:
            formatted_result["info"].append(self._format_math_symbols("Factored form available - useful for finding zeros"))
        
        if expanded and expanded != simplified:
            formatted_result["info"].append(self._format_math_symbols("Expanded form available - useful for polynomial operations"))
        
        # If expression has variables, try to create a plot
        if simplified and hasattr(simplified, 'free_symbols'):
            free_symbols = simplified.free_symbols
            if len(free_symbols) == 1:
                try:
                    plot_fig = self.solver.create_plot(simplified)
                    if plot_fig:
                        formatted_result["plot"] = plot_fig
                except:
                    pass
        
        return formatted_result
    
    def _format_math_symbols(self, text):
        """Convert mathematical expressions to use proper symbols"""
        if isinstance(text, str):
            # Replace sqrt with √ symbol
            text = re.sub(r'sqrt\(([^)]+)\)', r'√(\1)', text)
            
            # Replace other common mathematical symbols (token-aware)
            text = re.sub(r'(?<!\w)pi(?!\w)', 'π', text)
            text = re.sub(r'(?<!\w)infinity(?!\w)', '∞', text)
            text = re.sub(r'(?<!\w)oo(?!\w)', '∞', text)
            text = text.replace('**', '^')  # Power notation
            
            # Handle negative square roots
            text = re.sub(r'-√\(([^)]+)\)', r'-√(\1)', text)
            
        return text
    
    def _latex_format(self, expression):
        """Convert sympy expression to LaTeX format (for future enhancement)"""
        try:
            return sp.latex(expression)
        except:
            return str(expression)
    
    def add_step_explanations(self, steps, problem_type):
        """Add detailed explanations to solution steps"""
        explained_steps = []
        
        for step in steps:
            explained_step = step
            
            # Add explanations based on problem type
            if problem_type == "derivative":
                if "power rule" in step.lower():
                    explained_step += " (Power Rule: d/dx[x^n] = n*x^(n-1))"
                elif "chain rule" in step.lower():
                    explained_step += " (Chain Rule: d/dx[f(g(x))] = f'(g(x))*g'(x))"
            
            elif problem_type == "integral":
                if "power rule" in step.lower():
                    explained_step += " (Power Rule for Integration: ∫x^n dx = x^(n+1)/(n+1) + C)"
            
            explained_steps.append(explained_step)
        
        return explained_steps
    
    def _format_system_solution(self, solution_data, formatted_result):
        """Format system of equations solutions"""
        formatted_result['info'].append("📊 This is a system of equations with multiple variables")
        
        # Check if we have solutions for boat/current or similar problems
        answer = solution_data.get('answer', '')
        if 'b =' in answer and 'c =' in answer:
            formatted_result['info'].append("🚤 b = speed of boat in still water, c = speed of current")
        elif 'p =' in answer and 'w =' in answer:
            formatted_result['info'].append("✈️ p = speed of plane in still air, w = wind speed")
        
        return formatted_result
