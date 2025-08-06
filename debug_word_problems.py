#!/usr/bin/env python3
"""
Debug word problem issues to find incorrect answers
"""
from nlp_processor import NLPProcessor
from math_solver import MathSolver
from solution_formatter import SolutionFormatter

def debug_word_problems():
    """Debug various word problems to identify issues"""
    
    nlp = NLPProcessor()
    solver = MathSolver()
    formatter = SolutionFormatter()
    
    print("🔍 DEBUGGING WORD PROBLEM ISSUES")
    print("=" * 50)
    
    # Test cases that might have issues
    test_cases = [
        # Simple money problem
        ("Sarah buys 3 books for $15 each. What is the total cost?", "Expected: 3 × 15 = 45"),
        
        # Percentage problem
        ("What is 25% of 80?", "Expected: 0.25 × 80 = 20"),
        
        # Speed problem
        ("A car travels 120 miles in 3 hours. What is its speed?", "Expected: 120 ÷ 3 = 40"),
        
        # Age problem
        ("John is 5 years older than Mary. If Mary is 20 years old, how old is John?", "Expected: 20 + 5 = 25"),
        
        # Geometry problem
        ("What is the area of a rectangle with length 8 feet and width 5 feet?", "Expected: 8 × 5 = 40"),
        
        # Discount problem
        ("A shirt costs $25. If there's a 20% discount, what is the final price?", "Expected: 25 × (1 - 0.20) = 20"),
        
        # Boat problem
        ("A boat travels 24 km downstream in 3 hours and the same distance upstream in 4 hours. Find the speed of the boat in still water and the speed of the current.", "Expected: boat=7, current=1"),
    ]
    
    for i, (problem, expected) in enumerate(test_cases, 1):
        print(f"\n🧪 TEST {i}: {problem[:50]}...")
        print(f"Expected: {expected}")
        
        # Step 1: Check detection
        is_word_problem = nlp.is_word_problem(problem)
        print(f"Detected as word problem: {'✅' if is_word_problem else '❌'}")
        
        if not is_word_problem:
            print("❌ ISSUE: Not detected as word problem")
            continue
            
        # Step 2: Check extraction
        extracted = nlp.extract_math_from_text(problem)
        print(f"Extracted: {extracted}")
        
        if not extracted:
            print("❌ ISSUE: Failed to extract mathematical expression")
            continue
            
        # Step 3: Check numbers extraction
        numbers = nlp._extract_numbers(problem.lower())
        print(f"Numbers found: {numbers}")
        
        # Step 4: Check problem type identification
        problem_type = nlp._identify_problem_type(problem.lower())
        print(f"Problem type: {problem_type}")
        
        # Step 5: Solve and check result
        try:
            solution = solver.solve_problem(extracted)
            if solution and 'error' not in solution:
                formatted = formatter.format_solution(solution)
                answer = formatted.get('answer', 'No answer')
                print(f"Actual answer: {answer}")
                
                # Simple validation
                if "45" in str(answer) and "books" in problem:
                    print("✅ CORRECT")
                elif "20" in str(answer) and "25%" in problem:
                    print("✅ CORRECT") 
                elif "40" in str(answer) and "120 miles" in problem:
                    print("✅ CORRECT")
                elif "25" in str(answer) and "John" in problem:
                    print("✅ CORRECT")
                elif "40" in str(answer) and "rectangle" in problem:
                    print("✅ CORRECT")
                elif "20" in str(answer) and "discount" in problem:
                    print("⚠️ MIGHT BE WRONG - should be 20, not 500")
                elif "7" in str(answer) and "boat" in problem:
                    print("✅ CORRECT")
                else:
                    print("❌ POSSIBLY INCORRECT")
                    
            else:
                error = solution.get('error', 'Unknown error') if solution else 'No solution'
                print(f"❌ ERROR: {error}")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
        
        print("-" * 40)

if __name__ == "__main__":
    debug_word_problems()