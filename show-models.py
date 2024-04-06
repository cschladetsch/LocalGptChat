import openai

def read_api_key():
    try:
        with open('key', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: API key file 'key' not found.")
        sys.exit(1)

def list_available_models():
    api_key = read_api_key()
    openai.api_key = api_key

    response = openai.Engine.list()
    if 'data' in response:
        models = [model['id'] for model in response['data']]
        return models
    else:
        print("Error fetching models:", response)
        return []

if __name__ == "__main__":
    available_models = list_available_models()
    if available_models:
        print("Available Models:")
        for model_name in available_models:
            print(model_name)
    else:
        print("No models available.")

