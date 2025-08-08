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
        # Enhanced narrative indicators for better detection
        narrative_indicators = [
            # People and objects
            'a car', 'a person', 'john', 'mary', 'the train', 'the bus', 'a store', 'a student',
            'a teacher', 'a worker', 'sarah', 'mike', 'a farmer', 'a builder', 'the company',
            
            # Question words and phrases
            'if', 'when', 'how much', 'how many', 'what is', 'find', 'calculate', 'determine',
            'how old', 'how long', 'how far', 'how fast', 'how tall', 'how wide',
            
            # Time and measurement units
            'years old', 'miles', 'hours', 'minutes', 'seconds', 'days', 'weeks', 'months',
            'feet', 'meters', 'inches', 'centimeters', 'kilometers', 'yards',
            
            # Money and commerce
            'dollars', 'cents', 'price', 'cost', 'buy', 'sell', 'profit', 'discount', 'sale',
            'budget', 'spend', 'earn', 'save', 'total cost', 'change',
            
            # Motion and physics
            'speed', 'rate', 'time', 'distance', 'travels', 'drives', 'walks', 'runs',
            'acceleration', 'velocity', 'moves',
            
            # Geometry and shapes
            'rectangle', 'square', 'circle', 'triangle', 'area', 'perimeter', 'volume',
            'length', 'width', 'height', 'radius', 'diameter',
            
            # Common problem scenarios
            'population', 'temperature', 'weight', 'shares', 'distributes', 'splits',
            'mixture', 'recipe', 'ingredients', 'concentration', 'percentage'
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
            
            # First check for complex relationship patterns
            relationship_result = self._handle_relationship_problems(text_lower, numbers)
            if relationship_result:
                return relationship_result
            
            # Identify the type of word problem
            problem_type = self._identify_problem_type(text_lower)
            
            # Generate mathematical expression based on problem type
            if problem_type == 'complex_motion_problem':
                return self._handle_complex_motion_problem(text_lower, numbers)
            elif problem_type == 'speed_distance_time':
                return self._handle_speed_problem(text_lower, numbers)
            elif problem_type == 'age_problem':
                return self._handle_age_problem(text_lower, numbers)
            elif problem_type == 'money_problem':
                return self._handle_money_problem(text_lower, numbers)
            elif problem_type == 'geometry_problem':
                return self._handle_geometry_problem(text_lower, numbers)
            elif problem_type == 'percentage_problem':
                return self._handle_percentage_problem(text_lower, numbers)
            elif problem_type == 'mixture_problem':
                return self._handle_mixture_problem(text_lower, numbers)
            elif problem_type == 'work_problem':
                return self._handle_work_problem(text_lower, numbers)
            elif problem_type == 'growth_problem':
                return self._handle_growth_problem(text_lower, numbers)
            elif problem_type == 'system_word_problem':
                return self._handle_system_word_problem(text_lower, numbers)
            elif problem_type == 'algebra_word':
                return self._handle_algebra_word_problem(text_lower, numbers)
            else:
                return self._handle_general_word_problem(text_lower, numbers)
                
        except Exception as e:
            return None
    
    def _extract_numbers(self, text):
        """Extract all numbers from text with enhanced parsing"""
        numbers = []
        
        # Extract percentages as decimals FIRST to avoid double counting, e.g., 15% -> 0.15
        percentage_matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
        numbers.extend([float(p) / 100 for p in percentage_matches])
        
        # Extract fractions like "1/2" FIRST to avoid counting their components as digits
        fraction_matches = re.findall(r'(?<!\d)(\d+)/(\d+)(?!\d)', text)
        for num, den in fraction_matches:
            if int(den) != 0:  # Avoid division by zero
                numbers.append(float(num) / float(den))
        
        # Remove percentage and fraction tokens before extracting plain digit numbers
        cleaned_text = re.sub(r'\d+(?:\.\d+)?\s*%', ' ', text)
        cleaned_text = re.sub(r'(?<!\d)\d+/\d+(?!\d)', ' ', cleaned_text)
        
        # Extract digit numbers (including decimals), excluding those already handled via % or fraction
        digit_numbers = re.findall(r'\d+(?:\.\d+)?', cleaned_text)
        numbers.extend([float(num) for num in digit_numbers])
        
        # Extract word numbers with better compound number handling
        words = text.split()
        i = 0
        while i < len(words):
            word = re.sub(r'[^\w]', '', words[i].lower())
            
            # Handle compound numbers like "twenty-five"
            if word in self.number_words:
                current_num = self.number_words[word]
                
                # Check for compound numbers
                if i + 1 < len(words):
                    next_word = re.sub(r'[^\w]', '', words[i + 1].lower())
                    if next_word in self.number_words:
                        next_num = self.number_words[next_word]
                        # Handle cases like "twenty five" or "one hundred"
                        if current_num >= 20 and next_num < 10:  # e.g., "twenty five"
                            current_num += next_num
                            i += 1  # Skip next word as it's been processed
                        elif current_num == 100 and next_num < 100:  # e.g., "one hundred fifty"
                            current_num += next_num
                            i += 1
                
                numbers.append(current_num)
            i += 1
        
        # Remove duplicates while preserving order
        seen = set()
        unique_numbers = []
        for num in numbers:
            if num not in seen:
                seen.add(num)
                unique_numbers.append(num)
        
        return unique_numbers
    
    def _handle_relationship_problems(self, text, numbers):
        """Handle complex relationship problems like 'twice as many as'"""
        
        # Handle "twice as many as" patterns
        if re.search(r'twice as many.*as', text) or re.search(r'has twice', text):
            if len(numbers) >= 1:
                # Pattern: "John has twice as many apples as Mary, and Mary has 5 apples"
                # This means John = 2 * Mary = 2 * 5
                return f"2 * {numbers[0]}"
        
        # Handle "three times as many" patterns
        if re.search(r'three times.*as', text) or re.search(r'triple.*as', text):
            if len(numbers) >= 1:
                return f"3 * {numbers[0]}"
        
        # Handle "half as many" patterns
        if re.search(r'half.*as', text) or re.search(r'half of', text):
            if len(numbers) >= 1:
                return f"{numbers[0]} / 2"
        
        # Handle comparative problems with explicit relationships
        if re.search(r'(\w+) has (\d+) more than (\w+)', text):
            # Extract the specific relationship
            match = re.search(r'(\w+) has (\d+) more than (\w+)', text)
            if match and len(numbers) >= 2:
                difference = match.group(2)
                # If we know one person's amount, calculate the other
                return f"x + {difference} = {numbers[-1]}"
        
        return None
    
    def _identify_problem_type(self, text):
        """Identify the type of word problem with enhanced categorization"""
        # Complex motion problems (upstream/downstream, etc.)
        if any(keyword in text for keyword in ['upstream', 'downstream', 'current', 'still water', 'wind']):
            return 'complex_motion_problem'
        
        # Motion and physics problems
        elif any(keyword in text for keyword in ['speed', 'miles', 'hours', 'mph', 'km/h', 'travels', 'distance', 'far', 'velocity', 'acceleration']):
            return 'speed_distance_time'
        
        # Age-related problems
        elif any(keyword in text for keyword in ['years old', 'age', 'older', 'younger', 'born']):
            return 'age_problem'
        
        # Money and commerce problems
        elif any(keyword in text for keyword in ['dollars', 'cents', 'money', 'cost', 'price', 'buy', 'sell', 'profit', 'discount', 'budget', 'earn', 'spend']):
            return 'money_problem'
        
        # Geometry problems
        elif any(keyword in text for keyword in ['rectangle', 'square', 'circle', 'triangle', 'area', 'perimeter', 'volume', 'length', 'width', 'height', 'radius']):
            return 'geometry_problem'
        
        # Percentage and ratio problems
        elif any(keyword in text for keyword in ['percent', '%', 'percentage', 'ratio', 'proportion', 'rate']):
            return 'percentage_problem'
        
        # Mixture and concentration problems
        elif any(keyword in text for keyword in ['mixture', 'solution', 'concentration', 'pure', 'dilute', 'mix']):
            return 'mixture_problem'
        
        # Work and time problems
        elif any(keyword in text for keyword in ['work', 'job', 'complete', 'finish', 'together', 'alone', 'rate of work']):
            return 'work_problem'
        
        # System of equations problems (two unknowns)
        elif any(phrase in text for phrase in ['two numbers', 'find the numbers', 'sum and difference', 'sum to']) and any(keyword in text for keyword in ['difference', 'sum']):
            return 'system_word_problem'
        
        # Number problems and algebra
        elif any(keyword in text for keyword in ['consecutive', 'number', 'sum', 'product', 'difference', 'twice', 'half', 'triple']):
            return 'algebra_word'
        
        # Population and growth problems
        elif any(keyword in text for keyword in ['population', 'growth', 'increase', 'decrease', 'double', 'triple']):
            return 'growth_problem'
        
        # General calculation problems
        elif any(keyword in text for keyword in ['calculate', 'what is', 'find', 'determine']):
            return 'general'
        
        # Variable-based problems
        elif any(keyword in text for keyword in ['x', 'unknown', 'variable', 'equals', 'is equal']):
            return 'algebra_word'
        
        else:
            return 'general'
    
    def _handle_speed_problem(self, text, numbers):
        """Handle speed, distance, time problems"""
        if len(numbers) >= 2:
            # Speed calculation: distance / time
            if 'speed' in text or ('what is' in text and 'mph' in text):
                if 'miles' in text and 'hours' in text:
                    return f"{numbers[0]} / {numbers[1]}"
            
            # Distance calculation: speed * time
            elif 'distance' in text or 'far' in text or 'how far' in text:
                if 'mph' in text and 'hours' in text:
                    return f"{numbers[0]} * {numbers[1]}"
            
            # Time calculation: distance / speed
            elif 'time' in text or 'how long' in text:
                return f"{numbers[0]} / {numbers[1]}"
            
            # Default for travel problems - if it mentions traveling, assume speed calculation
            elif 'travel' in text:
                return f"{numbers[0]} / {numbers[1]}"
        
        return None
    
    def _handle_age_problem(self, text, numbers):
        """Handle age-related problems"""
        if len(numbers) >= 2:
            if 'older' in text:
                # "John is X years older than Mary. Mary is Y years old."
                # John's age = Mary's age + X = Y + X
                return f"{numbers[1]} + {numbers[0]}"
            elif 'younger' in text:
                # "John is X years younger than Mary. Mary is Y years old."
                # John's age = Mary's age - X = Y - X
                return f"{numbers[1]} - {numbers[0]}"
        
        return None
    
    def _handle_money_problem(self, text, numbers):
        """Handle money-related problems"""
        if len(numbers) >= 2:
            # Multiple items priced 'each' or 'per'
            if 'each' in text or 'per' in text:
                total_cost = 0.0
                # Pair consecutive numbers as (quantity, price)
                for idx in range(0, len(numbers) - 1, 2):
                    qty = numbers[idx]
                    price = numbers[idx + 1]
                    total_cost += qty * price
                if total_cost > 0:
                    return f"{total_cost}"
                else:
                    return f"{numbers[0]} * {numbers[1]}"
            
            # Discount problems
            elif 'discount' in text and ('percent' in text or '%' in text):
                base = numbers[0]
                rate = numbers[1]
                percentage = rate if rate <= 1 else rate / 100
                return f"{base} * (1 - {percentage})"
            
            # Total cost problems
            elif any(word in text for word in ['total', 'sum', 'altogether']):
                return " + ".join(str(n) for n in numbers)
            
            # Change / remaining money problems
            elif any(word in text for word in ['change', 'difference', 'left']):
                initial = numbers[0]
                expenses_sum = sum(numbers[1:]) if len(numbers) > 1 else 0
                return f"{initial} - {expenses_sum}"
                
        return None
    
    def _handle_algebra_word_problem(self, text, numbers):
        """Handle general algebra word problems"""
        
        # Handle consecutive integers first
        if 'consecutive' in text and 'integer' in text:
            if 'sum' in text and len(numbers) >= 1:
                # Find the largest number as it's likely the sum
                sum_value = max(numbers)
                # Sum of two consecutive integers is N -> x + (x+1) = N
                return f"x + (x + 1) = {sum_value}"
        
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
        """Handle general word problems with improved logical reasoning"""
        
        # Handle "increased by" / "decreased by" patterns
        if any(phrase in text for phrase in ['increased by', 'more than']):
            if 'equal' in text or 'is' in text:
                # Pattern: "A number increased by X is Y" -> "x + X = Y"
                if len(numbers) >= 2:
                    return f"x + {numbers[0]} = {numbers[1]}"
        
        if any(phrase in text for phrase in ['decreased by', 'reduced by']):
            if 'equal' in text or 'is' in text:
                # Pattern: "A number decreased by X equals Y" -> "x - X = Y"
                if len(numbers) >= 2:
                    return f"x - {numbers[0]} = {numbers[1]}"
        
        # Handle "twice as many" / "double" / "triple" patterns
        if 'twice' in text or 'double' in text:
            if len(numbers) >= 1:
                return f"2 * {numbers[0]}"
        elif 'triple' in text:
            if len(numbers) >= 1:
                return f"3 * {numbers[0]}"
        
        # Handle consecutive integers
        if 'consecutive' in text and 'integer' in text:
            if 'sum' in text and len(numbers) >= 1:
                # Find the largest number as it's likely the sum
                sum_value = max(numbers)
                # Sum of two consecutive integers is N -> x + (x+1) = N
                return f"x + (x + 1) = {sum_value}"
        
        # Handle simple calculation patterns (not equations)
        if any(phrase in text for phrase in ['what is', 'calculate', 'find the value of']):
            if len(numbers) >= 2:
                if any(keyword in text for keyword in self.operation_keywords['addition']):
                    return f"{numbers[0]} + {numbers[1]}"
                elif any(keyword in text for keyword in self.operation_keywords['subtraction']):
                    return f"{numbers[0]} - {numbers[1]}"
                elif any(keyword in text for keyword in self.operation_keywords['multiplication']):
                    return f"{numbers[0]} * {numbers[1]}"
                elif any(keyword in text for keyword in self.operation_keywords['division']):
                    return f"{numbers[0]} / {numbers[1]}"
        
        # Default behavior for other cases
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
        
        # Handle common patterns
        if 'decreased by' in text_part and len(numbers) >= 2:
            return f"x - {numbers[0]}"
        elif 'increased by' in text_part and len(numbers) >= 2:
            return f"x + {numbers[0]}"
        
        # Check for variable mentions
        if 'x' in text_part or 'unknown' in text_part or 'number' in text_part:
            return 'x'
        
        # Use first available number
        if numbers:
            return str(numbers[0])
        
        return None
    
    def _handle_geometry_problem(self, text, numbers):
        """Handle geometry-related problems"""
        if len(numbers) >= 1:
            # Area of rectangle: length * width
            if 'rectangle' in text and 'area' in text and len(numbers) >= 2:
                return f"{numbers[0]} * {numbers[1]}"
            
            # Area of square: side * side
            elif 'square' in text and 'area' in text:
                return f"{numbers[0]} * {numbers[0]}"
            
            # Area of circle: π * r²
            elif 'circle' in text and 'area' in text:
                return f"pi * {numbers[0]}**2"
            
            # Perimeter of rectangle: 2 * (length + width)
            elif 'rectangle' in text and 'perimeter' in text and len(numbers) >= 2:
                return f"2 * ({numbers[0]} + {numbers[1]})"
            
            # Perimeter of square: 4 * side
            elif 'square' in text and 'perimeter' in text:
                return f"4 * {numbers[0]}"
            
            # Circumference of circle: 2 * π * r
            elif 'circle' in text and ('circumference' in text or 'perimeter' in text):
                return f"2 * pi * {numbers[0]}"
            
            # Volume of cube: side³
            elif 'cube' in text and 'volume' in text:
                return f"{numbers[0]}**3"
                
        return None
    
    def _handle_percentage_problem(self, text, numbers):
        """Handle percentage-related problems"""
        if len(numbers) >= 2:
            # What is X% of Y?
            if 'percent of' in text or '% of' in text:
                # Convert percentage to decimal and multiply
                percentage = numbers[0] if numbers[0] <= 1 else numbers[0] / 100
                return f"{percentage} * {numbers[1]}"
            
            # X is what percent of Y?
            elif 'what percent' in text:
                return f"({numbers[0]} / {numbers[1]}) * 100"
            
            # Increase by percentage
            elif 'increase' in text and ('percent' in text or '%' in text):
                percentage = numbers[0] if numbers[0] <= 1 else numbers[0] / 100
                return f"{numbers[1]} * (1 + {percentage})"
            
            # Decrease by percentage  
            elif 'decrease' in text and ('percent' in text or '%' in text):
                percentage = numbers[0] if numbers[0] <= 1 else numbers[0] / 100
                return f"{numbers[1]} * (1 - {percentage})"
                
        return None
    
    def _handle_mixture_problem(self, text, numbers):
        """Handle mixture and concentration problems"""
        if len(numbers) >= 2:
            # Simple mixture: amount1 + amount2
            if 'mix' in text or 'combine' in text:
                return f"{numbers[0]} + {numbers[1]}"
            
            # Concentration problems (basic)
            elif 'concentration' in text:
                return f"({numbers[0]} / {numbers[1]}) * 100"
                
        return None
    
    def _handle_work_problem(self, text, numbers):
        """Handle work and rate problems"""
        if len(numbers) >= 2:
            # Combined work rates: 1/rate1 + 1/rate2
            if 'together' in text and ('work' in text or 'job' in text):
                return f"1/({numbers[0]}) + 1/({numbers[1]})"
            
            # Work = rate * time
            elif 'work' in text and 'time' in text:
                return f"{numbers[0]} * {numbers[1]}"
                
        return None
    
    def _handle_growth_problem(self, text, numbers):
        """Handle population growth and similar problems"""
        if len(numbers) >= 2:
            # Exponential growth: initial * growth_rate^time
            if 'growth' in text or 'increase' in text:
                return f"{numbers[0]} * {numbers[1]}**{numbers[2] if len(numbers) > 2 else 1}"
            
            # Simple increase/decrease
            elif 'double' in text:
                return f"{numbers[0]} * 2"
            elif 'triple' in text:
                return f"{numbers[0]} * 3"
            elif 'half' in text:
                return f"{numbers[0]} / 2"
                
        return None
    
    def _handle_complex_motion_problem(self, text, numbers):
        """Handle complex motion problems like upstream/downstream boat problems"""
        if len(numbers) >= 3:  # Need distance, downstream time, upstream time minimum
            
            # Boat upstream/downstream problems
            if any(keyword in text for keyword in ['boat', 'ship', 'vessel']):
                if 'downstream' in text and 'upstream' in text:
                    # Standard pattern: distance, downstream_time, upstream_time
                    # Let b = boat speed in still water, c = current speed
                    # downstream: (b + c) * time_down = distance
                    # upstream: (b - c) * time_up = distance
                    # This gives us: b + c = distance/time_down, b - c = distance/time_up
                    
                    distance = numbers[0]  # First number is usually distance
                    
                    # Find downstream and upstream times
                    downstream_time = None
                    upstream_time = None
                    
                    # Look for patterns in text
                    if len(numbers) >= 3:
                        # Assume pattern: distance, downstream_time, upstream_time
                        downstream_time = numbers[1]
                        upstream_time = numbers[2]
                    
                    if downstream_time and upstream_time:
                        # Create system of equations
                        # b + c = distance/downstream_time
                        # b - c = distance/upstream_time
                        downstream_speed = distance / downstream_time
                        upstream_speed = distance / upstream_time
                        
                        # Return as system: boat_speed + current = downstream_speed, boat_speed - current = upstream_speed
                        return f"b + c = {downstream_speed}, b - c = {upstream_speed}"
            
            # Airplane with wind problems
            elif any(keyword in text for keyword in ['plane', 'airplane', 'aircraft']):
                if 'tailwind' in text and 'headwind' in text:
                    # Similar logic but with wind instead of current
                    distance = numbers[0]
                    tailwind_time = numbers[1] if len(numbers) > 1 else None
                    headwind_time = numbers[2] if len(numbers) > 2 else None
                    
                    if tailwind_time and headwind_time:
                        tailwind_speed = distance / tailwind_time
                        headwind_speed = distance / headwind_time
                        return f"p + w = {tailwind_speed}, p - w = {headwind_speed}"
        
        return None
    
    def _handle_system_word_problem(self, text, numbers):
        """Handle general system of equations word problems"""
        if len(numbers) >= 2:
            # Two numbers with sum and difference
            if 'sum' in text and 'difference' in text:
                if len(numbers) >= 2:
                    # Assume first number is sum, second is difference
                    sum_val = numbers[0] if numbers[0] > numbers[1] else numbers[1] 
                    diff_val = numbers[1] if numbers[0] > numbers[1] else numbers[0]
                    # x + y = sum, x - y = difference
                    return f"x + y = {sum_val}, x - y = {diff_val}"
        
        return None
