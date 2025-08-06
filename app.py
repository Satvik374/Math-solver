import streamlit as st
import traceback
from math_solver import MathSolver
from nlp_processor import NLPProcessor
from solution_formatter import SolutionFormatter

# Initialize components
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
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for dark theme styling
    st.markdown("""
    <style>
    /* Dark theme overrides */
    .stApp {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    .main {
        background-color: #1a1a1a !important;
    }
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #4a5bc7 0%, #5a67d8 100%);
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        color: white;
    }
    .main-header h1 {
        color: white !important;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header p {
        color: #f0f0f0 !important;
        font-size: 1.2rem !important;
        margin: 0 !important;
    }
    .stTextArea > div > div > textarea {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border-radius: 15px;
        border: 2px solid #444444;
        padding: 1rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #4a5bc7;
        box-shadow: 0 0 15px rgba(74, 91, 199, 0.3);
        background-color: #333333 !important;
    }
    .stButton > button {
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .solution-container {
        background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        border: 1px solid #444444;
        color: #ffffff !important;
    }
    .step-card {
        background: #2d2d2d;
        color: #ffffff !important;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #4a5bc7;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .answer-highlight {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    .sidebar-content {
        background: #2d2d2d;
        color: #ffffff !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #444444;
    }
    .feature-card {
        background: #2d2d2d;
        color: #ffffff !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #444444;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .feature-card h3, .feature-card h4 {
        color: #6c7ce7 !important;
    }
    .feature-card p, .feature-card div, .feature-card li {
        color: #ffffff !important;
    }
    .math-symbol {
        color: #6c7ce7 !important;
        font-weight: bold;
    }
    .white-bg-text {
        color: #ffffff !important;
    }
    .dark-text {
        color: #ffffff !important;
    }
    /* Dark theme for Streamlit elements */
    .stMarkdown, .stText, .stDataFrame {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    .stSelectbox label, .stTextArea label, .stButton label {
        color: #ffffff !important;
    }
    .stSelectbox > div > div {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
    }
    /* Dark theme for markdown containers */
    div[data-testid="stMarkdownContainer"] p, 
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stMarkdownContainer"] span {
        color: #ffffff !important;
    }
    /* Dark theme for sidebar */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] > div {
        background-color: #1a1a1a !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced header
    st.markdown("""
    <div class="main-header">
        <h1>🧮 AI Math Problem Solver</h1>
        <p>✨ Enter your mathematical problem and get step-by-step solutions with beautiful formatting!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize components
    try:
        solver, nlp, formatter = init_components()
    except Exception as e:
        st.error(f"Failed to initialize components: {str(e)}")
        st.stop()
    
    # Enhanced sidebar for problem type selection
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-content">
            <h2 style="color: #6c7ce7; text-align: center; margin-bottom: 1rem;">🎯 Problem Type</h2>
        </div>
        """, unsafe_allow_html=True)
        
        problem_type = st.selectbox(
            "🔍 Select the type of problem:",
            ["🤖 Auto-detect", "🔢 Algebra", "📈 Calculus", "📐 Geometry", "📝 Word Problem", "⚖️ Direct Equation"],
            format_func=lambda x: x
        )
        
        st.markdown("""
        <div class="sidebar-content">
            <h3 style="color: #6c7ce7;">💡 Examples:</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced examples with better formatting
        examples = [
            ("🔢", "Solve x² + 5x + 6 = 0", "Quadratic equation"),
            ("📊", "Find derivative of x³ + 2x²", "Calculus differentiation"),
            ("∫", "Integrate sin(x) dx", "Calculus integration"),
            ("🚗", "Car travels 60 miles in 2 hours. Speed?", "Word problem")
        ]
        
        for icon, example, description in examples:
            st.markdown(f"""
            <div class="feature-card">
                <strong style="color: #ffffff !important;">{icon} {example}</strong><br>
                <small style="color: #cccccc !important;">{description}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Add helpful tips
        st.markdown("""
        <div class="sidebar-content">
            <h3 style="color: #6c7ce7 !important;">💡 Tips:</h3>
            <ul style="color: #cccccc !important; font-size: 0.9rem;">
                <li style="color: #cccccc !important;">Use <span class="math-symbol">√</span> for square roots</li>
                <li style="color: #cccccc !important;">Use <span class="math-symbol">^</span> for exponents</li>
                <li style="color: #cccccc !important;">Use <span class="math-symbol">π</span> for pi</li>
                <li style="color: #cccccc !important;">Natural language is supported!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced main input area
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div style="background: #2d2d2d; padding: 1.5rem; border-radius: 15px; border: 1px solid #444444; margin-bottom: 1rem;">
            <h2 style="color: #6c7ce7 !important; margin-bottom: 1rem;">📝 Enter Your Problem</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Get the random input value if it exists
        default_value = st.session_state.get('random_input', '')
        
        problem_input = st.text_area(
            "🔤 Type your mathematical problem here:",
            value=default_value,
            height=180,
            placeholder="✨ Example: Solve 2x + 5 = 15 for x\n📐 Try: Find derivative of x³ + 2x²\n∫ Or: Integrate sin(x) dx",
            help="You can use natural language or mathematical notation. The AI will understand both!"
        )
        
        # Clear the random input after it's been used
        if 'random_input' in st.session_state:
            del st.session_state.random_input
        
        # Enhanced solve button with animation effect
        solve_button = st.button(
            "🚀 Solve Problem", 
            type="primary", 
            use_container_width=True,
            help="Click to solve your mathematical problem with step-by-step explanation"
        )
    
    with col2:
        st.markdown("""
        <div style="background: #2d2d2d; padding: 1.5rem; border-radius: 15px; border: 1px solid #444444; margin-bottom: 1rem;">
            <h2 style="color: #6c7ce7 !important; margin-bottom: 1rem;">⚡ Quick Actions</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            if st.button("🗑️ Clear", use_container_width=True, help="Clear the input field"):
                # Clear any existing random input
                if 'random_input' in st.session_state:
                    del st.session_state.random_input
                st.rerun()
        with col2_2:
            if st.button("🎲 Random", use_container_width=True, help="Try a random example"):
                import random
                examples = [
                    # Algebraic equations
                    "solve x² + 4x - 5 = 0",
                    "solve 2x + 10 = 0",
                    "factor x² - 9",
                    "solve √(x + 1) = 3",
                    "simplify (x + 2)(x - 3)",
                    
                    # Calculus problems
                    "find derivative of x³ + 2x²",
                    "integrate x² dx",
                    "find derivative of sin(x)",
                    "integrate cos(x) dx",
                    
                    # Word problems - Speed/Distance/Time
                    "A car travels 120 miles in 3 hours. What is its speed?",
                    "If a train travels at 60 mph for 2.5 hours, how far does it go?",
                    
                    # Word problems - Money
                    "Sarah buys 3 books for $15 each and 2 pens for $2 each. What is the total cost?",
                    "A shirt costs $25. If there's a 20% discount, what is the final price?",
                    
                    # Word problems - Age
                    "John is 5 years older than Mary. If Mary is 20 years old, how old is John?",
                    
                    # Word problems - Geometry
                    "What is the area of a rectangle with length 8 feet and width 5 feet?",
                    "Find the perimeter of a square with side length 7 meters",
                    
                    # Word problems - Percentage
                    "What is 25% of 80?",
                    "A population of 1000 increases by 15%. What is the new population?",
                    
                    # Word problems - General
                    "If 12 apples cost $6, how much do 8 apples cost?",
                    
                    # Complex word problems - Systems of equations
                    "A boat travels 24 km downstream in 3 hours and the same distance upstream in 4 hours. Find the speed of the boat in still water and the speed of the current.",
                    "Two numbers sum to 50 and their difference is 10. Find the numbers."
                ]
                st.session_state.random_input = random.choice(examples)
        
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #6c7ce7 !important; margin-bottom: 1rem;">🛠️ Supported Operations:</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.9rem; color: #ffffff !important;">
                <div style="color: #ffffff !important;">📈 Equation solving</div>
                <div style="color: #ffffff !important;">🔍 Differentiation</div>
                <div style="color: #ffffff !important;">∫ Integration</div>
                <div style="color: #ffffff !important;">🔧 Simplification</div>
                <div style="color: #ffffff !important;">📊 Factoring</div>
                <div style="color: #ffffff !important;">📐 Expansion</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Math symbols quick reference
        st.markdown("""
        <div class="feature-card">
            <h4 style="color: #6c7ce7 !important;">🔤 Quick Symbols:</h4>
            <div style="font-size: 0.9rem; line-height: 1.6; color: #ffffff !important;">
                <span class="math-symbol">√</span> <span style="color: #ffffff !important;">Square root</span> &nbsp;&nbsp;
                <span class="math-symbol">π</span> <span style="color: #ffffff !important;">Pi</span> &nbsp;&nbsp;
                <span class="math-symbol">∞</span> <span style="color: #ffffff !important;">Infinity</span><br>
                <span class="math-symbol">^</span> <span style="color: #ffffff !important;">Power</span> &nbsp;&nbsp;
                <span class="math-symbol">∫</span> <span style="color: #ffffff !important;">Integral</span> &nbsp;&nbsp;
                <span class="math-symbol">≠</span> <span style="color: #ffffff !important;">Not equal</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    

    
    # Process the problem when button is clicked
    if solve_button and problem_input.strip():
        with st.spinner("Solving your problem..."):
            try:
                # Map display names back to internal names
                type_mapping = {
                    "🤖 Auto-detect": "Auto-detect",
                    "🔢 Algebra": "Algebra", 
                    "📈 Calculus": "Calculus",
                    "📐 Geometry": "Geometry",
                    "📝 Word Problem": "Word Problem",
                    "⚖️ Direct Equation": "Direct Equation"
                }
                internal_problem_type = type_mapping.get(problem_type, problem_type)
                
                # Process the input
                if internal_problem_type == "Word Problem" or (internal_problem_type == "Auto-detect" and nlp.is_word_problem(problem_input)):
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
                solution = solver.solve_problem(problem_to_solve, internal_problem_type)
                
                if solution and "error" not in solution:
                    # Enhanced success message
                    st.balloons()
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                                color: white; padding: 1rem; border-radius: 15px; text-align: center; 
                                margin: 1rem 0; font-size: 1.1rem; font-weight: 600;">
                        🎉 Problem solved successfully! 🎉
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Format and display the solution
                    formatted_solution = formatter.format_solution(solution)
                    
                    # Solution container with enhanced styling
                    st.markdown('<div class="solution-container">', unsafe_allow_html=True)
                    
                    st.markdown("""
                    <h2 style="color: #6c7ce7; text-align: center; margin-bottom: 2rem;">
                        📋 Complete Solution
                    </h2>
                    """, unsafe_allow_html=True)
                    
                    # Display original problem in enhanced format
                    st.markdown("""
                    <div style="background: #3a3a3a; padding: 1rem; border-radius: 10px; border-left: 4px solid #6c7ce7; margin-bottom: 1.5rem;">
                        <h4 style="color: #6c7ce7 !important; margin-bottom: 0.5rem;">📝 Original Problem:</h4>
                        <div style="background: #2d2d2d; padding: 1rem; border-radius: 8px; font-family: monospace; font-size: 1.1rem; color: #ffffff !important;">
                    """ + problem_input + """
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced step-by-step solution
                    if formatted_solution.get("steps"):
                        st.markdown("""
                        <h3 style="color: #6c7ce7; margin: 1.5rem 0 1rem 0;">
                            🔢 Step-by-Step Solution:
                        </h3>
                        """, unsafe_allow_html=True)
                        
                        for i, step in enumerate(formatted_solution["steps"], 1):
                            st.markdown(f"""
                            <div class="step-card">
                                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                    <div style="background: #6c7ce7; color: white; border-radius: 50%; 
                                                width: 30px; height: 30px; display: flex; align-items: center; 
                                                justify-content: center; margin-right: 1rem; font-weight: bold;">
                                        {i}
                                    </div>
                                    <div style="font-size: 1.1rem; line-height: 1.4; color: #ffffff !important;">
                                        {step}
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Enhanced final answer display
                    if formatted_solution.get("answer"):
                        st.markdown("""
                        <h3 style="color: #6c7ce7; margin: 1.5rem 0 1rem 0;">
                            🎯 Final Answer:
                        </h3>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="answer-highlight">
                            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🏆</div>
                            <div style="font-size: 1.3rem;">{formatted_solution["answer"]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Enhanced plot display
                    if formatted_solution.get("plot"):
                        st.markdown("""
                        <h3 style="color: #6c7ce7; margin: 1.5rem 0 1rem 0;">
                            📊 Visualization:
                        </h3>
                        """, unsafe_allow_html=True)
                        
                        plot_col1, plot_col2, plot_col3 = st.columns([1, 3, 1])
                        with plot_col2:
                            st.pyplot(formatted_solution["plot"])
                    
                    # Enhanced additional info
                    if formatted_solution.get("info"):
                        st.markdown("""
                        <h3 style="color: #6c7ce7; margin: 1.5rem 0 1rem 0;">
                            💡 Additional Information:
                        </h3>
                        """, unsafe_allow_html=True)
                        
                        for info in formatted_solution["info"]:
                            st.markdown(f"""
                            <div style="background: #3a3a3a; padding: 1rem; border-radius: 10px; 
                                        border-left: 4px solid #6c7ce7; margin: 0.5rem 0; color: #ffffff;">
                                <strong style="color: #ffffff;">💡</strong> <span style="color: #ffffff;">{info}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                elif solution and "error" in solution:
                    # Enhanced error display
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%); 
                                color: white; padding: 1rem; border-radius: 15px; text-align: center; 
                                margin: 1rem 0; font-size: 1.1rem;">
                        🤔 Hmm, I encountered an issue...
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="background: #4a3a3a; padding: 1rem; border-radius: 10px; border-left: 4px solid #ff6b6b; margin: 1rem 0; color: #ffffff;">
                        <strong style="color: #ff6b6b;">❌ Error:</strong> <span style="color: #ffffff;">{solution['error']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced suggestions
                    st.markdown("""
                    <div style="background: #3a3a3a; padding: 1rem; border-radius: 10px; border-left: 4px solid #6c7ce7; margin: 1rem 0; color: #ffffff;">
                        <strong style="color: #6c7ce7;">💡 Try these suggestions:</strong><br>
                        <span style="color: #ffffff;">• Reformat your equation: <code style="background: #2d2d2d; color: #ffffff; padding: 2px 4px; border-radius: 3px;">x + 5 = 10</code><br>
                        • Use proper syntax: <code style="background: #2d2d2d; color: #ffffff; padding: 2px 4px; border-radius: 3px;">solve x^2 + 2x + 1 = 0</code><br>
                        • Check spelling and mathematical notation<br>
                        • Try the random example button for inspiration!</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show what was processed
                    st.markdown("""
                    <div style="background: #3a3a3a; padding: 1rem; border-radius: 10px; margin: 1rem 0; color: #ffffff;">
                        <strong style="color: #ffffff;">🔍 What was processed:</strong><br>
                        <code style="background: #2d2d2d; color: #ffffff; padding: 0.5rem; border-radius: 5px; display: block; margin-top: 0.5rem;">""" + problem_to_solve + """</code>
                    </div>
                    """, unsafe_allow_html=True)
                
                else:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%); 
                                color: white; padding: 1rem; border-radius: 15px; text-align: center; 
                                margin: 1rem 0; font-size: 1.1rem;">
                        😵 Oops! Something went wrong...
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div style="background: #4a3a3a; padding: 1rem; border-radius: 10px; border-left: 4px solid #ff6b6b; margin: 1rem 0; color: #ffffff;">
                        <strong style="color: #ff6b6b;">❌</strong> <span style="color: #ffffff;">Could not solve the problem. Please check your input and try again.</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%); 
                            color: white; padding: 1rem; border-radius: 15px; text-align: center; 
                            margin: 1rem 0; font-size: 1.1rem;">
                    🚨 Unexpected Error Occurred
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background: #4a3a3a; padding: 1rem; border-radius: 10px; border-left: 4px solid #ff6b6b; margin: 1rem 0; color: #ffffff;">
                    <strong style="color: #ff6b6b;">❌ Error:</strong> <span style="color: #ffffff;">{str(e)}</span><br>
                    <small style="color: #cccccc;">Please check your input format and try again.</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Show detailed error in expander for debugging
                with st.expander("🔧 Show detailed error information (for debugging)"):
                    st.code(traceback.format_exc())
    
    elif solve_button and not problem_input.strip():
        st.markdown("""
        <div style="background: #4a3a3a; padding: 1rem; border-radius: 10px; border-left: 4px solid #ffa726; margin: 1rem 0; text-align: center; color: #ffffff;">
            <strong style="color: #ffa726;">⚠️</strong> <span style="color: #ffffff;">Please enter a mathematical problem to solve.</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4a5bc7 0%, #5a67d8 100%); 
                color: white; padding: 2rem; border-radius: 20px; margin: 2rem 0; text-align: center;">
        <h2 style="color: white; margin-bottom: 1.5rem;">📚 How to Use AI Math Solver</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; text-align: left;">
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                <h4 style="color: #fff; margin-bottom: 0.5rem;">1️⃣ Enter Problem</h4>
                <p style="color: #f0f0f0; margin: 0; font-size: 0.9rem;">Type your mathematical problem using natural language or mathematical notation</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                <h4 style="color: #fff; margin-bottom: 0.5rem;">2️⃣ Select Type</h4>
                <p style="color: #f0f0f0; margin: 0; font-size: 0.9rem;">Choose problem type or let AI auto-detect it for you</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                <h4 style="color: #fff; margin-bottom: 0.5rem;">3️⃣ Solve</h4>
                <p style="color: #f0f0f0; margin: 0; font-size: 0.9rem;">Click 'Solve Problem' to get detailed step-by-step solutions</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                <h4 style="color: #fff; margin-bottom: 0.5rem;">4️⃣ Understand</h4>
                <p style="color: #f0f0f0; margin: 0; font-size: 0.9rem;">Review the solution with explanations and beautiful mathematical formatting</p>
            </div>
        </div>
        <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
            <p style="color: #f0f0f0; margin: 0; font-size: 0.9rem;">
                ✨ Powered by AI • 🧮 Advanced Mathematics • 📊 Beautiful Visualizations
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
