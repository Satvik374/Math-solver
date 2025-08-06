import streamlit as st
import traceback
from math_solver import MathSolver
from nlp_processor import NLPProcessor
from solution_formatter import SolutionFormatter

# Initialize components
@st.cache_resource
def init_components():
    """Initialize the math solver and NLP processor"""
    solver = MathSolver()
    nlp = NLPProcessor()
    formatter = SolutionFormatter()
    return solver, nlp, formatter

def main():
    st.set_page_config(
        page_title="AI Math Problem Solver",
        page_icon="🧮",
        layout="wide"
    )
    
    st.title("🧮 AI Math Problem Solver")
    st.markdown("Enter your mathematical problem and get step-by-step solutions!")
    
    # Initialize components
    try:
        solver, nlp, formatter = init_components()
    except Exception as e:
        st.error(f"Failed to initialize components: {str(e)}")
        st.stop()
    
    # Sidebar for problem type selection
    st.sidebar.header("Problem Type")
    problem_type = st.sidebar.selectbox(
        "Select the type of problem:",
        ["Auto-detect", "Algebra", "Calculus", "Geometry", "Word Problem", "Direct Equation"]
    )
    
    st.sidebar.markdown("### Examples:")
    st.sidebar.markdown("- Solve x^2 + 5x + 6 = 0")
    st.sidebar.markdown("- Find the derivative of x^3 + 2x^2")
    st.sidebar.markdown("- Integrate sin(x) dx")
    st.sidebar.markdown("- A car travels 60 miles in 2 hours. What is its speed?")
    
    # Main input area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Enter Your Problem")
        problem_input = st.text_area(
            "Type your mathematical problem here:",
            height=150,
            placeholder="Example: Solve 2x + 5 = 15 for x"
        )
        
        solve_button = st.button("🔍 Solve Problem", type="primary", use_container_width=True)
    
    with col2:
        st.header("Quick Actions")
        if st.button("Clear Input", use_container_width=True):
            st.rerun()
        
        st.markdown("### Supported Operations:")
        st.markdown("- Equation solving")
        st.markdown("- Differentiation")
        st.markdown("- Integration")
        st.markdown("- Simplification")
        st.markdown("- Factoring")
        st.markdown("- Expansion")
    
    # Process the problem when button is clicked
    if solve_button and problem_input.strip():
        with st.spinner("Solving your problem..."):
            try:
                # Process the input
                if problem_type == "Word Problem" or (problem_type == "Auto-detect" and nlp.is_word_problem(problem_input)):
                    # Extract mathematical expression from word problem
                    extracted_problem = nlp.extract_math_from_text(problem_input)
                    if extracted_problem:
                        st.info(f"Extracted mathematical expression: {extracted_problem}")
                        problem_to_solve = extracted_problem
                    else:
                        problem_to_solve = problem_input
                else:
                    problem_to_solve = problem_input
                
                # Solve the problem
                solution = solver.solve_problem(problem_to_solve, problem_type)
                
                if solution:
                    # Display the solution
                    st.success("✅ Problem solved successfully!")
                    
                    # Format and display the solution
                    formatted_solution = formatter.format_solution(solution)
                    
                    st.header("📋 Solution")
                    
                    # Display original problem
                    st.subheader("Original Problem:")
                    st.code(problem_input, language="text")
                    
                    # Display solution steps
                    if formatted_solution.get("steps"):
                        st.subheader("Step-by-Step Solution:")
                        for i, step in enumerate(formatted_solution["steps"], 1):
                            st.markdown(f"**Step {i}:** {step}")
                    
                    # Display final answer
                    if formatted_solution.get("answer"):
                        st.subheader("Final Answer:")
                        st.success(formatted_solution["answer"])
                    
                    # Display plot if available
                    if formatted_solution.get("plot"):
                        st.subheader("Visualization:")
                        st.pyplot(formatted_solution["plot"])
                    
                    # Display additional info
                    if formatted_solution.get("info"):
                        st.subheader("Additional Information:")
                        for info in formatted_solution["info"]:
                            st.info(info)
                
                else:
                    st.error("❌ Could not solve the problem. Please check your input and try again.")
                    
            except Exception as e:
                st.error(f"❌ An error occurred while solving the problem: {str(e)}")
                st.error("Please check your input format and try again.")
                
                # Show detailed error in expander for debugging
                with st.expander("Show detailed error information"):
                    st.code(traceback.format_exc())
    
    elif solve_button and not problem_input.strip():
        st.warning("⚠️ Please enter a mathematical problem to solve.")
    
    # Footer
    st.markdown("---")
    st.markdown("### How to Use:")
    st.markdown("1. Enter your mathematical problem in the text area above")
    st.markdown("2. Select the problem type (or use Auto-detect)")
    st.markdown("3. Click 'Solve Problem' to get step-by-step solutions")
    st.markdown("4. View the detailed solution with explanations")

if __name__ == "__main__":
    main()
