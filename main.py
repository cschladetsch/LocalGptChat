import openai
import sys

def read_api_key():
    try:
        with open('key', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: API key file 'key' not found.")
        sys.exit(1)

def main():
    api_key = read_api_key()
    openai.api_key = api_key

    model_name = "gpt-4"  # Or any other appropriate model

    while True:
        user_input = input("You: ")
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
        print("GPT-4:", response)

if __name__ == "__main__":
    main()
