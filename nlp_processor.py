import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

class NLPProcessor:
    def __init__(self):
        """Initialize the NLP processor for word problems"""
        self.number_words = {
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
            'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
            'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
            'eighty': 80, 'ninety': 90, 'hundred': 100, 'thousand': 1000, 'million': 1000000
        }
        
        self.operation_keywords = {
            'addition': ['+', 'plus', 'add', 'sum', 'total', 'combined', 'altogether', 'increased by'],
            'subtraction': ['-', 'minus', 'subtract', 'difference', 'less than', 'decreased by', 'reduced by'],
            'multiplication': ['*', 'times', 'multiply', 'product', 'of', 'twice', 'double', 'triple'],
            'division': ['/', 'divide', 'divided by', 'quotient', 'per', 'ratio', 'split', 'share'],
            'equals': ['=', 'equals', 'is', 'are', 'makes', 'gives', 'results in']
        }
    
    def is_word_problem(self, text):
        """Determine if the input is a word problem"""
        # Check for narrative indicators
        narrative_indicators = [
            'a car', 'a person', 'john', 'mary', 'the train', 'the bus',
            'if', 'when', 'how much', 'how many', 'what is', 'find',
            'calculate', 'determine', 'years old', 'miles', 'hours',
            'dollars', 'feet', 'meters', 'speed', 'rate', 'time'
        ]
        
        text_lower = text.lower()
        
        # Check if it contains narrative language
        has_narrative = any(indicator in text_lower for indicator in narrative_indicators)
        
        # Check if it's not just a mathematical expression
        has_math_symbols = any(symbol in text for symbol in ['+', '-', '*', '/', '=', '^', 'x', 'y'])
        
        # It's a word problem if it has narrative elements and isn't purely mathematical
        return has_narrative and not (has_math_symbols and len(text.split()) < 5)
    
    def extract_math_from_text(self, text):
        """Extract mathematical expressions from word problems"""
        try:
            # Convert text to lowercase for processing
            text_lower = text.lower()
            
            # Extract numbers from text
            numbers = self._extract_numbers(text_lower)
            
            # Identify the type of word problem
            problem_type = self._identify_problem_type(text_lower)
            
            # Generate mathematical expression based on problem type
            if problem_type == 'speed_distance_time':
                return self._handle_speed_problem(text_lower, numbers)
            elif problem_type == 'age_problem':
                return self._handle_age_problem(text_lower, numbers)
            elif problem_type == 'money_problem':
                return self._handle_money_problem(text_lower, numbers)
            elif problem_type == 'algebra_word':
                return self._handle_algebra_word_problem(text_lower, numbers)
            else:
                return self._handle_general_word_problem(text_lower, numbers)
                
        except Exception as e:
            return None
    
    def _extract_numbers(self, text):
        """Extract all numbers from text"""
        numbers = []
        
        # Extract digit numbers
        digit_numbers = re.findall(r'\d+(?:\.\d+)?', text)
        numbers.extend([float(num) for num in digit_numbers])
        
        # Extract word numbers
        words = text.split()
        for word in words:
            word_clean = re.sub(r'[^\w]', '', word)
            if word_clean in self.number_words:
                numbers.append(self.number_words[word_clean])
        
        return numbers
    
    def _identify_problem_type(self, text):
        """Identify the type of word problem"""
        if any(keyword in text for keyword in ['speed', 'miles', 'hours', 'mph', 'km/h', 'travels', 'distance']):
            return 'speed_distance_time'
        elif any(keyword in text for keyword in ['years old', 'age', 'older', 'younger']):
            return 'age_problem'
        elif any(keyword in text for keyword in ['dollars', 'cents', 'money', 'cost', 'price', 'buy', 'sell']):
            return 'money_problem'
        elif any(keyword in text for keyword in ['x', 'unknown', 'find', 'variable']):
            return 'algebra_word'
        else:
            return 'general'
    
    def _handle_speed_problem(self, text, numbers):
        """Handle speed, distance, time problems"""
        if 'speed' in text or 'mph' in text or 'km/h' in text:
            if len(numbers) >= 2:
                # Assume distance / time = speed
                if 'miles' in text and 'hours' in text:
                    return f"{numbers[0]} / {numbers[1]}"
        elif 'distance' in text:
            if len(numbers) >= 2:
                # Assume speed * time = distance
                return f"{numbers[0]} * {numbers[1]}"
        elif 'time' in text:
            if len(numbers) >= 2:
                # Assume distance / speed = time
                return f"{numbers[0]} / {numbers[1]}"
        
        return None
    
    def _handle_age_problem(self, text, numbers):
        """Handle age-related problems"""
        if len(numbers) >= 2:
            if 'older' in text or 'more than' in text:
                return f"x + {numbers[1]} = {numbers[0]}" if len(numbers) >= 2 else f"x + {numbers[0]}"
            elif 'younger' in text or 'less than' in text:
                return f"x - {numbers[1]} = {numbers[0]}" if len(numbers) >= 2 else f"x - {numbers[0]}"
        
        return None
    
    def _handle_money_problem(self, text, numbers):
        """Handle money-related problems"""
        if len(numbers) >= 2:
            if any(word in text for word in ['total', 'sum', 'altogether']):
                return f"{numbers[0]} + {numbers[1]}"
            elif any(word in text for word in ['change', 'difference', 'left']):
                return f"{numbers[0]} - {numbers[1]}"
            elif any(word in text for word in ['each', 'per', 'cost']):
                return f"{numbers[0]} * {numbers[1]}"
        
        return None
    
    def _handle_algebra_word_problem(self, text, numbers):
        """Handle general algebra word problems"""
        # Look for equation structure
        if '=' in text or 'equals' in text or 'is' in text:
            # Try to build an equation
            parts = re.split(r'\s+(?:is|equals|=)\s+', text)
            if len(parts) == 2:
                left_expr = self._text_to_expression(parts[0], numbers)
                right_expr = self._text_to_expression(parts[1], numbers)
                if left_expr and right_expr:
                    return f"{left_expr} = {right_expr}"
        
        return None
    
    def _handle_general_word_problem(self, text, numbers):
        """Handle general word problems"""
        if len(numbers) >= 2:
            # Determine operation based on keywords
            if any(keyword in text for keyword in self.operation_keywords['addition']):
                return f"{numbers[0]} + {numbers[1]}"
            elif any(keyword in text for keyword in self.operation_keywords['subtraction']):
                return f"{numbers[0]} - {numbers[1]}"
            elif any(keyword in text for keyword in self.operation_keywords['multiplication']):
                return f"{numbers[0]} * {numbers[1]}"
            elif any(keyword in text for keyword in self.operation_keywords['division']):
                return f"{numbers[0]} / {numbers[1]}"
        
        return None
    
    def _text_to_expression(self, text_part, numbers):
        """Convert text part to mathematical expression"""
        # Simple implementation - can be expanded
        text_part = text_part.strip()
        
        # Check if it's a number
        try:
            return str(float(text_part))
        except:
            pass
        
        # Check for variable mentions
        if 'x' in text_part or 'unknown' in text_part or 'number' in text_part:
            return 'x'
        
        # Use first available number
        if numbers:
            return str(numbers[0])
        
        return None
