"""
COGNIS - Utility Functions
Helper functions for the application
"""

import os
import re
from datetime import datetime
import json


def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove special characters
    text = re.sub(r'[^\w\s\-\.\,]', '', text)
    return text


def extract_numbers(text):
    """Extract all numbers from text"""
    if not text:
        return []
    numbers = re.findall(r'\d+\.?\d*', text)
    return [float(n) if '.' in n else int(n) for n in numbers]


def calculate_percentile(value, values_list):
    """Calculate percentile rank of a value"""
    if not values_list:
        return 0
    sorted_values = sorted(values_list)
    index = sorted_values.index(value) if value in sorted_values else 0
    percentile = (index / len(sorted_values)) * 100
    return percentile


def format_duration(days):
    """Format duration in days to human readable format"""
    if days < 30:
        return f"{days} days"
    elif days < 365:
        months = days / 30
        return f"{months:.1f} months"
    else:
        years = days / 365
        return f"{years:.1f} years"


def safe_divide(numerator, denominator):
    """Safely divide two numbers, return 0 if denominator is 0"""
    try:
        return numerator / denominator if denominator != 0 else 0
    except:
        return 0


def calculate_consistency_score(data_points):
    """Calculate consistency score from a list of data points"""
    if len(data_points) < 2:
        return 0

    # Calculate standard deviation
    mean = sum(data_points) / len(data_points)
    variance = sum((x - mean) ** 2 for x in data_points) / len(data_points)
    std_dev = variance ** 0.5

    # Normalize to 0-100 (lower std dev = higher consistency)
    max_std = 50  # Maximum expected standard deviation
    consistency = max(0, 100 - (std_dev / max_std) * 100)
    return consistency


def categorize_score(score):
    """Categorize a score into qualitative labels"""
    if score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Very Good"
    elif score >= 70:
        return "Good"
    elif score >= 60:
        return "Average"
    elif score >= 50:
        return "Below Average"
    else:
        return "Needs Improvement"


def generate_candidate_id(name):
    """Generate unique candidate ID"""
    timestamp = datetime.now().strftime("%Y%m%d")
    clean_name = re.sub(r'[^a-zA-Z]', '', name)[:5]
    return f"COG-{timestamp}-{clean_name.upper()}"


def read_file_safely(filepath):
    """Read a file safely with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None


def write_file_safely(filepath, content):
    """Write content to a file safely"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing to file {filepath}: {e}")
        return False


def create_directory_safely(directory):
    """Create directory safely"""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        return False


def validate_email(email):
    """Validate email address format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return False
    pattern = r'^\+?[\d\s\-()]{10,15}$'
    return bool(re.match(pattern, phone))


def get_file_extension(filename):
    """Get file extension from filename"""
    if not filename:
        return ""
    return os.path.splitext(filename)[1].lower()


def is_text_file(filename):
    """Check if file is a text file"""
    text_extensions = ['.txt', '.csv', '.json', '.xml', '.html', '.md', '.rst']
    extension = get_file_extension(filename)
    return extension in text_extensions


def remove_extra_spaces(text):
    """Remove extra spaces from text"""
    if not text:
        return ""
    return ' '.join(text.split())