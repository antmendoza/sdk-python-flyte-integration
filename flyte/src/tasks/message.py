def greeting(data: dict) -> dict:
    return {
        "greeting": f"Welcome to Serverless Workflow, {data['name']}!"
    }