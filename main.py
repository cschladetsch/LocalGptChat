import openai
import sys
import os
import re
from datetime import datetime

# ANSI color codes
BLUE = '\033[94m'
GREEN = '\033[92m'
CYAN = '\033[96m'
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
    match = re.match(r'```(.*?)```', code, re.DOTALL)
    if match:
        code_content = match.group(1).strip()

        # Write the code content to file
        timestamp = datetime.now().isoformat(timespec='seconds').replace(':', '-')
        file_name = f'request_{timestamp}.txt'
        file_path = os.path.join(dir_path, file_name)
        with open(file_path, 'w') as f:
            f.write(code_content)
        
        print(f"{DARK_GREY}Σ{END} Code written to file: {file_path}")
    else:
        print(f"{DARK_GREY}Σ{END} Error: Could not extract code snippet from the input.")

def append_to_log(content, log_file):
    timestamp = datetime.now().isoformat(timespec='seconds')
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {content}\n")

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

    log_file = 'log.txt'

    while True:
        user_input = input(f"{BLUE}λ {END}")
        append_to_log(f'User input: {user_input}', log_file)
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
        append_to_log(f'AI response: {response}', log_file)

        if '```' in response:
            print(f"{DARK_GREY}Σ{END} {CYAN}{response}{END}")
            write_code_to_file(response)
        else:
            print(f"Σ{END} {GREEN}{response}{END}")

if __name__ == "__main__":
    main()
