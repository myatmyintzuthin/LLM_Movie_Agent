from typing import List, Tuple, Optional
from neo4j_semantic_layer import agent_executor
from neo4j_semantic_layer.utils import graph

class StreamHandler:
    def __init__(self):
        self.text = ""

    def new_token(self, token: str) -> None:
        self.text += token
        print(token, end="", flush=True)

    def reset(self):
        self.text = "" 

def get_agent_response(input_text: str, chat_history: Optional[List[Tuple]] = [], stream_handler=None):
    response = agent_executor.invoke({"input": input_text, "chat_history": chat_history})

    if isinstance(response, dict):
        agent_response = response['output']
        for value in agent_response:
            stream_handler.new_token(value)

    print()

def generate_history(user_input: str, agent_response: str, chat_history: List[Tuple] = []):
    # Store conversation history for context
    chat_history.append((user_input, agent_response))
    return chat_history

def main():
    print("*"*10)
    # print("\n 🎥 Movie Agent へようこそ!")
    # print("質問をするか、「exit」と入力して終了します。\n")

    print("\n 🎥 Welcome to Movie Agent")
    print("Add question or type 'exit' to stop.\n")
    print("*"*10)
    chat_history = []
    stream_handler = StreamHandler()

    while True:
        # user_input = input("\nあなた: ")
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            # print("またね!👋")
            print("Good Bye👋")
            graph._driver.close()
            break

        # Display "thinking" message for the user (optional, can be omitted if preferred)
        # print("\nAgent は考えています🤖 。。。\n")
        print("\nAgent is thinking 🤖 。。。\n")

        # Get the agent's response and display it as it streams
        get_agent_response(user_input, chat_history, stream_handler)

        # Store the agent's response history
        chat_history = generate_history(user_input, stream_handler.text, chat_history)

        # Reset stream handler for the next round of interaction
        stream_handler.reset()

if __name__ == "__main__":
    main()
