#!/usr/bin/env python3
"""
Test more specific word problem patterns that might be problematic
"""
from nlp_processor import NLPProcessor
from math_solver import MathSolver
from solution_formatter import SolutionFormatter

def test_problematic_patterns():
    """Test word problems that might be causing issues"""
    
    nlp = NLPProcessor()
    solver = MathSolver()
    formatter = SolutionFormatter()
    
    print("🔍 TESTING POTENTIALLY PROBLEMATIC WORD PROBLEMS")
    print("=" * 60)
    
    # More complex test cases that might have issues
    test_cases = [
        # Money problems with multiple items
        ("Sarah buys 3 books for $15 each and 2 pens for $2 each. What is the total cost?", "Expected: (3×15) + (2×2) = 49"),
        
        # Percentage increase/decrease
        ("A population of 1000 increases by 15%. What is the new population?", "Expected: 1000 × 1.15 = 1150"),
        
        # Distance problems
        ("If a train travels at 60 mph for 2.5 hours, how far does it go?", "Expected: 60 × 2.5 = 150"),
        
        # Proportion problems
        ("If 12 apples cost $6, how much do 8 apples cost?", "Expected: (8/12) × 6 = 4"),
        
        # Mixed units
        ("A rectangle is 10 inches long and 6 inches wide. What is the perimeter in inches?", "Expected: 2×(10+6) = 32"),
        
        # Complex money
        ("John has $50. He buys a book for $12 and a pen for $3. How much money does he have left?", "Expected: 50 - 12 - 3 = 35"),
        
        # Multi-step problems
        ("A store sells shirts for $20 each. If they give a 25% discount, what is the sale price?", "Expected: 20 × (1-0.25) = 15"),
    ]
    
    for i, (problem, expected) in enumerate(test_cases, 1):
        print(f"\n🧪 TEST {i}:")
        print(f"Problem: {problem}")
        print(f"Expected: {expected}")
        
        # Check each step
        is_word_problem = nlp.is_word_problem(problem)
        print(f"Word Problem: {'✅' if is_word_problem else '❌'}")
        
        if not is_word_problem:
            print("❌ ISSUE: Not detected as word problem")
            continue
            
        extracted = nlp.extract_math_from_text(problem)
        print(f"Extracted: {extracted}")
        
        if not extracted:
            print("❌ ISSUE: Failed to extract")
            continue
            
        # Get numbers and problem type for analysis
        numbers = nlp._extract_numbers(problem.lower())
        problem_type = nlp._identify_problem_type(problem.lower())
        print(f"Numbers: {numbers}")
        print(f"Type: {problem_type}")
        
        # Solve
        try:
            solution = solver.solve_problem(extracted)
            if solution and 'error' not in solution:
                formatted = formatter.format_solution(solution)
                answer = formatted.get('answer', 'No answer')
                print(f"Answer: {answer}")
                
                # Check if answer seems reasonable
                answer_num = float(str(answer).replace(',', '').split()[0]) if answer else 0
                
                if "total cost" in problem and "books" in problem and "pens" in problem:
                    if 45 <= answer_num <= 55:  # Should be around 49
                        print("✅ REASONABLE")
                    else:
                        print("❌ SEEMS WRONG")
                elif "population" in problem and "1000" in problem:
                    if 1100 <= answer_num <= 1200:  # Should be 1150
                        print("✅ REASONABLE") 
                    else:
                        print("❌ SEEMS WRONG")
                elif "train" in problem and "60 mph" in problem:
                    if 140 <= answer_num <= 160:  # Should be 150
                        print("✅ REASONABLE")
                    else:
                        print("❌ SEEMS WRONG")
                elif "apples" in problem and "cost" in problem:
                    if 3 <= answer_num <= 5:  # Should be 4
                        print("✅ REASONABLE")
                    else:
                        print("❌ SEEMS WRONG")
                else:
                    print("⚠️ NEED MANUAL CHECK")
                    
            else:
                error = solution.get('error', 'Unknown error') if solution else 'No solution'
                print(f"❌ ERROR: {error}")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_problematic_patterns()