# scg-SecureRandomStringGenerator
Generates cryptographically secure random strings of specified length, allowing users to specify the character set (alphanumeric, special characters, etc.). Provides a command-line interface to generate strings and securely copy them to the clipboard. - Focused on Automates the generation of basic secure code snippets (e.g., password hashing, input validation, secure random number generation) using Jinja2 templates and a set of predefined secure coding practices. Facilitates quick and consistent security implementation.

## Install
`git clone https://github.com/ShadowStrikeHQ/scg-securerandomstringgenerator`

## Usage
`./scg-securerandomstringgenerator [params]`

## Parameters
- `-l`: No description provided
- `-c`: Character set to use:\n
- `--custom_chars`: Custom character set to use when --charset is set to 
- `--copy`: Copy the generated string to the clipboard.
- `--template`: Path to Jinja2 template file for code generation.
- `--hash_password`: No description provided

## License
Copyright (c) ShadowStrikeHQ
