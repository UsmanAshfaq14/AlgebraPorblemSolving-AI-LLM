import re
from datetime import datetime
import math
class AlgebraAssistant:
    def __init__(self):
        self.valid_operators = {'+', '-', '*', '/', '^', '(', ')'}
        self.variables = set('abcdefghijklmnopqrstuvwxyz')
    def format_markdown(self, text, level=1):
        """Format text as markdown heading based on level."""
        return f"{'#' * level} {text}\n"
    def format_code(self, text):
        """Format text as inline code."""
        return f"`{text}`"
    def format_step(self, step_num, description):
        """Format a solution step in markdown."""
        return f"\n### Step {step_num}: {description}\n"
    def get_greeting(self):
        """Generate appropriate greeting based on time of day."""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning!"
        elif 12 <= hour < 17:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
        return self.format_markdown(greeting)
    def detect_user_tone(self, user_input):
        """Analyze user's tone based on their message."""
        frustrated_words = {'stuck', 'confused', 'help', 'difficult', 'hard'}
        excited_words = {'love', 'fun', 'exciting', 'great', 'awesome'}
        user_words = set(user_input.lower().split())
        if any(word in user_words for word in frustrated_words):
            return "frustrated"
        elif any(word in user_words for word in excited_words):
            return "excited"
        return "neutral"
    def validate_markdown_format(self, user_input):
        """Check if equation is properly formatted with triple backticks."""
        validation_steps = [self.format_markdown("Input Validation", 2)]
        pattern = r'```[\s\S]*?```'
        validation_steps.append("* Checking markdown format...")
        if not re.match(pattern, user_input.strip()):
            validation_steps.append("* :x: Invalid markdown format")
            validation_steps.append(
                f"* Required format: {self.format_code('```equation```')}")
            return False, "\n".join(validation_steps)
        validation_steps.append("* :white_check_mark: Valid markdown format")
        return True, "\n".join(validation_steps)
    def extract_equation(self, user_input):
        """Extract equation from markdown format."""
        return user_input.strip('`').strip()
    def validate_equation(self, equation):
        """Validate the mathematical equation with detailed steps."""
        validation_steps = []
        # Check for equality sign
        validation_steps.append("* Checking for equality sign...")
        if '=' not in equation:
            validation_steps.append("* :x: No equality sign found")
            return False, "\n".join(validation_steps)
        validation_steps.append("* :white_check_mark: Equality sign present")
        # Check for variables
        validation_steps.append("\n* Checking for variables...")
        has_variable = False
        found_variables = set()
        for char in equation:
            if char.lower() in self.variables:
                has_variable = True
                found_variables.add(char)
        if not has_variable:
            validation_steps.append("* :x: No variables found")
            return False, "\n".join(validation_steps)
        validation_steps.append(
            f"* :white_check_mark: Variables found: {', '.join(self.format_code(v) for v in found_variables)}")
        # Check for valid operators
        validation_steps.append("\n* Checking operators...")
        equation_chars = set(equation.replace(' ', ''))
        invalid_chars = equation_chars - self.valid_operators - \
            self.variables - set('0123456789=.')
        if invalid_chars:
            validation_steps.append(
                f"* :x: Invalid characters found: {', '.join(self.format_code(c) for c in invalid_chars)}")
            return False, "\n".join(validation_steps)
        validation_steps.append("* :white_check_mark: All operators are valid")
        # Check for division by zero
        validation_steps.append("\n* Checking for division by zero...")
        if '/0' in equation.replace(' ', ''):
            validation_steps.append("* :x: Division by zero detected")
            return False, "\n".join(validation_steps)
        validation_steps.append("* :white_check_mark: No division by zero found")
        return True, "\n".join(validation_steps)
    def standardize_equation(self, equation):
        """Standardize the equation format with detailed steps."""
        steps = []
        # Remove spaces
        steps.append("* Removing unnecessary spaces...")
        equation = equation.replace(' ', '')
        steps.append(f"* Result: {self.format_code(equation)}")
        # Split into left and right sides
        steps.append("\n* Separating left and right sides...")
        left, right = equation.split('=')
        steps.append(f"* Left side: {self.format_code(left)}")
        steps.append(f"* Right side: {self.format_code(right)}")
        standardized = f"{left} = {right}"
        steps.append(
            f"\n* Final standardized form: {self.format_code(standardized)}")
        return standardized, "\n".join(steps)
    def analyze_terms(self, equation):
        """Analyze and classify terms in the equation."""
        left, right = equation.split('=')
        def classify_term(term):
            """Classify a term as variable or constant."""
            has_variable = any(c in self.variables for c in term)
            return "variable" if has_variable else "constant"
        # Split terms by + or - signs, preserving the signs
        def split_terms(expr):
            terms = []
            current_term = ""
            for char in expr:
                if char in '+-' and current_term:
                    terms.append(current_term)
                    current_term = char
                else:
                    current_term += char
            if current_term:
                terms.append(current_term)
            return terms
        left_terms = split_terms(left)
        right_terms = split_terms(right)
        analysis = []
        analysis.append("\n* Analyzing left side terms:")
        for term in left_terms:
            term_type = classify_term(term)
            analysis.append(f"  * {self.format_code(term)}: {term_type} term")
        analysis.append("\n* Analyzing right side terms:")
        for term in right_terms:
            term_type = classify_term(term)
            analysis.append(f"  * {self.format_code(term)}: {term_type} term")
        return "\n".join(analysis)
    def solve_equation(self, equation):
        """Main method to solve the equation step by step."""
        solution = []
        # First validate the format
        is_valid_format, format_validation = self.validate_markdown_format(
            equation)
        solution.append(format_validation)
        if not is_valid_format:
            return "\n".join(solution)
        # Extract equation from markdown
        clean_equation = self.extract_equation(equation)
        # Validate equation
        is_valid_equation, equation_validation = self.validate_equation(
            clean_equation)
        solution.append("\n" + equation_validation)
        if not is_valid_equation:
            return "\n".join(solution)
        # Standardize equation
        solution.append(self.format_step(1, "Standardizing the Equation"))
        standardized, standardize_steps = self.standardize_equation(
            clean_equation)
        solution.append(standardize_steps)
        # Analyze terms
        solution.append(self.format_step(2, "Analyzing Terms"))
        term_analysis = self.analyze_terms(standardized)
        solution.append(term_analysis)
        # Show solving strategy
        solution.append(self.format_step(3, "Solving Strategy"))
        solution.append("1. Move all variable terms to the left side")
        solution.append("2. Move all constant terms to the right side")
        solution.append("3. Combine like terms")
        solution.append("4. Isolate the variable")
        # Final solution
        solution.append(self.format_step(4, "Final Solution"))
        solution.append(
            f"Standardized equation: {self.format_code(standardized)}")
        return "\n".join(solution)
    def get_user_feedback(self):
        """Request user feedback on solution clarity."""
        return self.format_markdown("Feedback", 2) + "Did this explanation help you? Please rate the clarity of the solution on a scale from 1 to 5."
    def process_feedback(self, rating):
        """Process user feedback and provide appropriate response."""
        try:
            rating = int(rating)
            if rating < 3:
                return "How can I improve the explanation? Would you like additional steps or alternative methods?"
            return "Thank you for your feedback! Is there anything else you'd like help with?"
        except ValueError:
            return "Please provide a valid rating between 1 and 5."
def main():
    assistant = AlgebraAssistant()
    # Initial greeting
    print(assistant.get_greeting())
    print(assistant.format_markdown("Welcome to the Algebra Assistant!", 2))
    print("Please share your equation in the format: ```equation```")
    while True:
        user_input = input("\nEnter your equation (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            print(assistant.format_markdown(
                "Thank you for using the Algebra Assistant. Goodbye!", 2))
            break
        # Detect user tone and respond appropriately
        tone = assistant.detect_user_tone(user_input)
        if tone == "frustrated":
            print(assistant.format_markdown(
                "I understand this might be frustrating. Let's break it down step by step.", 3))
        elif tone == "excited":
            print(assistant.format_markdown(
                "I love your enthusiasm! Let's solve this together!", 3))
        # Solve the equation
        solution = assistant.solve_equation(user_input)
        print("\n" + solution)
        # Get feedback
        print("\n" + assistant.get_user_feedback())
        rating = input("Your rating (1-5): ")
        print("\n" + assistant.process_feedback(rating))
if __name__ == "__main__":
    main()









