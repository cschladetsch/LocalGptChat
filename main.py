import openai
import sys
import os
import re

# ANSI color codes
BLUE = '\033[94m'
GREEN = '\033[92m'
DARK_GREY = '\033[90m'
END = '\033[0m'

# Mapping of language to file extensions
ext_map = {
    'python': '.py',
    'java': '.java',
    'c': '.c',
    'cpp': '.cpp',
    # Add more language to file extension maps if needed
}

def write_code_to_file(code, dir_path='./'):
    # Extract language and code content from the code snippet
    match = re.match(r'.*```(.*?)```', code, re.DOTALL)
    if match:
        action = match.group(1).strip()
        language = match.group(2).strip()
        code_content = match.group(3).strip()
        
        # Determine file extension based on the language
        file_ext = ext_map.get(language.lower())
        if not file_ext:
            print(f"{DARK_GREY}Σ{END} Error: Unsupported language '{language}'")
            return
        
        # Write the code content to file
        file_name = f'file_{len(os.listdir(dir_path)) + 1}{file_ext}'
        file_path = os.path.join(dir_path, file_name)
        with open(file_path, 'w') as f:
            f.write(code_content.strip('`'))
        
        print(f"{DARK_GREY}Σ{END} Code written to file: {file_path}")
    else:
        print(f"{DARK_GREY}Σ{END} Error: Could not extract code snippet from the input.")

def read_contents(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: Couldn't open {filename}")
        return 0

def main():
    api_key = read_contents('key')
    model_name = read_contents('model')

    openai.api_key = api_key

    while True:
        user_input = input(f"{BLUE}λ {END}")
        if user_input.lower() == 'exit':
            print("Exiting...")
            break

        completion = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        response = completion.choices[0].message['content']

        #if '```' in response:
        #write_code_to_file(response)
        #else:
        print(f"{DARK_GREY}Σ{END} {GREEN}{response}{END}")

if __name__ == "__main__":
    main()

