import os
from dotenv import load_dotenv
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


load_dotenv()

def main():
    #client = genai.Client(api_key = os.getenv('GEMINI_API_KEY'))
    print("Initializing Gemini...")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7
    )

    prompt = "Explain the concept of 'Zero Trust' in cybersecurity in two simple sentences"
    print(f'\nUser: {prompt}')

    messages = [HumanMessage(content=prompt)]

    print("\nThinking")
    response = llm.invoke(messages)

    print(f"\nAI: {response.content}")

if __name__ == "__main__":
    main()