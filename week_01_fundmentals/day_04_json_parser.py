import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

class SecurityReport(BaseModel):
    vulnerability_name: str = Field(description="The name of the most common vulnerability")
    severity: str = Field(desctiption="Based on its impact classify into: Low, Medium, High, or Critical")
    fix_recommendation:str = Field(description="One concise point on how to fix it")


def main():
    print("Initializing Strict JSON Parser chain....")


    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash',
        temperature=0.0
    )

    parser = PydanticOutputParser(pydantic_object=SecurityReport)


    template=""""
    You are a strict code analyzer. Analyze the following technology:{technology}.
    {format_instructions}
    """

    prompt = PromptTemplate(
        input_variables=["technology"],
        template=template,
        partial_variables={"format_instructions":parser.get_format_instructions()}
    )

    chain = prompt | llm | parser


    print("\nAnalyzing...\n")
    result = chain.invoke({"technology":"JSON Web Tokens (JWT) used for authentication"})

    print(f"Data Type Returned: {type(result)}\n")
    print(f"Vunlerability: {result.vulnerability_name}")
    print(f"Severity: {result.severity}")
    print(f"fix:{result.fix_recommendation}")


if __name__ == "__main__":
    main()


