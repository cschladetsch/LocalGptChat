import openai
import sys

def read_contents(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: coiuldn't open" + filename)
        return 0

def main():
    api_key = read_contents('key')
    model_name = read_contents('model')

    openai.api_key = api_key

    while True:
        user_input = input ("λ ")
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
        print("Σ", response)

if __name__ == "__main__":
    main()
