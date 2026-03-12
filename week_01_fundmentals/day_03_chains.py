import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()
def main():

    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash',
        temperature=0.0
    )

    #prompt template
    template="""" 
    You are an expert Application Secutiry Engineer
    Explain the most common security vulnerability when writing {topic} in {language}.
    Provide a concise explanation and one short example of how to prevent it."""

    prompt = PromptTemplate(
        input_variables=["language","topic"],
        template = template
    )

    parser = StrOutputParser()


    chain = prompt | llm | parser

    print("\nExecuting Chain...\n")

    result = chain.invoke({
        "language":"python",
        "topic":"SQL Database Queries"
    })

    print(result)


if __name__ == "__main__":
    main()
