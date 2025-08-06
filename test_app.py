import streamlit as st
from math_solver import MathSolver
from solution_formatter import SolutionFormatter

st.title("Math Solver Test")

# Simple form
equation = st.text_input("Enter equation:", "x + 5 = 10")
if st.button("Solve"):
    solver = MathSolver()
    formatter = SolutionFormatter()
    
    result = solver.solve_problem(equation)
    st.write("Raw result:", result)
    
    if result and "error" not in result:
        formatted = formatter.format_solution(result)
        st.success(f"Answer: {formatted['answer']}")
        
        st.write("Steps:")
        for step in formatted['steps']:
            st.write(f"- {step}")
    else:
        st.error("Failed to solve")