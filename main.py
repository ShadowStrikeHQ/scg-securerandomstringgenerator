import argparse
import secrets
import string
import logging
import pyperclip
from jinja2 import Environment, FileSystemLoader
import os
from Crypto.Hash import SHA256

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_random_string(length: int, char_set: str) -> str:
    """
    Generates a cryptographically secure random string of the specified length
    using the provided character set.

    Args:
        length: The desired length of the random string.
        char_set: The character set to use for generating the string.

    Returns:
        A cryptographically secure random string.

    Raises:
        TypeError: If length is not an integer.
        ValueError: If length is not positive or char_set is empty.
    """
    if not isinstance(length, int):
        raise TypeError("Length must be an integer.")
    if length <= 0:
        raise ValueError("Length must be a positive integer.")
    if not char_set:
        raise ValueError("Character set cannot be empty.")

    try:
        return ''.join(secrets.choice(char_set) for _ in range(length))
    except Exception as e:
        logging.error(f"Error generating random string: {e}")
        raise

def copy_to_clipboard(text: str) -> None:
    """
    Copies the given text to the clipboard.

    Args:
        text: The text to copy to the clipboard.
    """
    try:
        pyperclip.copy(text)
        logging.info("String copied to clipboard.")
    except pyperclip.PyperclipException as e:
        logging.warning(f"Unable to copy to clipboard: {e}.  Ensure xclip or xsel is installed.")

def setup_argparse() -> argparse.ArgumentParser:
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        An argparse.ArgumentParser object.
    """
    parser = argparse.ArgumentParser(
        description="Generates cryptographically secure random strings.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-l", "--length", type=int, default=16,
        help="Length of the random string (default: 16)."
    )

    parser.add_argument(
        "-c", "--charset", type=str, default="alphanumeric",
        choices=["alphanumeric", "alphanumeric_symbols", "digits", "letters", "symbols", "custom"],
        help="Character set to use:\n"
             "- alphanumeric:  a-z, A-Z, 0-9\n"
             "- alphanumeric_symbols: a-z, A-Z, 0-9, and common symbols\n"
             "- digits: 0-9\n"
             "- letters: a-z, A-Z\n"
             "- symbols: Common symbols\n"
             "- custom: Use --custom_chars to specify characters."
    )

    parser.add_argument(
        "--custom_chars", type=str,
        help="Custom character set to use when --charset is set to 'custom'."
    )

    parser.add_argument(
        "--copy", action="store_true",
        help="Copy the generated string to the clipboard."
    )
    
    parser.add_argument(
        "--template", type=str,
        help="Path to Jinja2 template file for code generation."
    )
    
    parser.add_argument(
        "--hash_password", action="store_true",
        help="Hashes the generated string using SHA256 (for password hashing example)."
    )

    return parser

def render_template(template_path: str, context: dict) -> str:
    """
    Renders a Jinja2 template with the given context.

    Args:
        template_path: The path to the Jinja2 template file.
        context: A dictionary containing the variables to pass to the template.

    Returns:
        The rendered template as a string.
    """
    try:
        env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
        template = env.get_template(os.path.basename(template_path))
        return template.render(context)
    except Exception as e:
        logging.error(f"Error rendering template: {e}")
        raise

def main():
    """
    Main function to parse arguments, generate a random string, and optionally
    copy it to the clipboard.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        # Determine character set
        if args.charset == "alphanumeric":
            char_set = string.ascii_letters + string.digits
        elif args.charset == "alphanumeric_symbols":
            char_set = string.ascii_letters + string.digits + string.punctuation
        elif args.charset == "digits":
            char_set = string.digits
        elif args.charset == "letters":
            char_set = string.ascii_letters
        elif args.charset == "symbols":
            char_set = string.punctuation
        elif args.charset == "custom":
            if not args.custom_chars:
                parser.error("When --charset is 'custom', you must specify --custom_chars.")
            char_set = args.custom_chars
        else:
            raise ValueError("Invalid character set specified.")

        # Generate random string
        random_string = generate_random_string(args.length, char_set)

        if args.hash_password:
            # Example password hashing (SHA256)
            hashed_password = SHA256.new(random_string.encode('utf-8')).hexdigest()
            print(f"Generated (and Hashed) Random String (SHA256): {hashed_password}")
            if args.copy:
                copy_to_clipboard(hashed_password)
        elif args.template:
            # Render Jinja2 template
            context = {"random_string": random_string}
            rendered_code = render_template(args.template, context)
            print(rendered_code)
            if args.copy:
                copy_to_clipboard(rendered_code)
        else:
            # Print the generated string
            print(f"Generated Random String: {random_string}")

            # Copy to clipboard if requested
            if args.copy:
                copy_to_clipboard(random_string)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()