# Overview

AI Math Problem Solver is a web-based application that uses Streamlit to provide an interactive interface for solving various types of mathematical problems. The system leverages SymPy for symbolic mathematics and includes natural language processing capabilities to handle word problems. Users can input mathematical expressions or word problems and receive step-by-step solutions with formatted output.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses Streamlit as the web framework, providing a simple and interactive user interface. The main interface is built in `app.py` with a two-column layout featuring a sidebar for problem type selection and a main area for problem input. The UI includes example problems and supports auto-detection of problem types.

## Backend Architecture
The system follows a modular architecture with three core components:

1. **MathSolver (`math_solver.py`)** - Handles the core mathematical computations using SymPy. This component can solve algebraic equations, perform calculus operations (derivatives and integrals), and process general mathematical expressions. It includes preprocessing capabilities to clean and normalize mathematical input.

2. **NLPProcessor (`nlp_processor.py`)** - Processes natural language word problems and converts them into mathematical expressions. It includes keyword mapping for mathematical operations and can identify narrative indicators to distinguish word problems from direct mathematical expressions.

3. **SolutionFormatter (`solution_formatter.py`)** - Formats solution output for display, providing step-by-step explanations and organizing results based on problem type. This component handles error formatting and can generate additional information about solutions.

## Data Flow
The application follows a sequential processing pipeline:
1. User input is captured through the Streamlit interface
2. Input is preprocessed and problem type is determined (auto-detection or user-selected)
3. The appropriate solver method is called based on problem type
4. Results are formatted for display with step-by-step solutions
5. Output is rendered in the Streamlit interface

## Error Handling
The system implements comprehensive error handling with try-catch blocks around component initialization and problem solving. Errors are gracefully displayed to users with descriptive messages.

# External Dependencies

## Python Libraries
- **Streamlit** - Web application framework for the user interface
- **SymPy** - Symbolic mathematics library for equation solving, calculus operations, and mathematical expression parsing
- **NumPy** - Numerical computing support
- **Matplotlib** - Plotting and visualization capabilities
- **Regular Expressions (re)** - Text processing and pattern matching for NLP functionality

## Mathematical Computing
The application relies heavily on SymPy's symbolic mathematics engine for:
- Algebraic equation solving
- Calculus operations (derivatives and integrals)
- Expression parsing and simplification
- Mathematical plotting capabilities

## No External APIs
The system operates as a self-contained application without dependencies on external mathematical APIs or web services, ensuring consistent performance and offline capability.