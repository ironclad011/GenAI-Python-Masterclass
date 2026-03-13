import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

load_dotenv()

malicious_ips = ["192.168.1.100","10.0.0.5"]
@tool
def analyze_ip_address(ip_address:str)->str:
    """"
    Use this tool to analyze an IP address for known mallicious activity or open ports.
    Always use this tool if the user asks about the safety or status of an IP address."""
    
    
    print(f"\n[SYSTEM LOG] Running anaylze_ip_address Python function on: {ip_address}...\n")

    if ip_address in malicious_ips:
        return f"ALERT: IP {ip_address} is flagged for maliciious port scanning activity."
    return f"SAFE: IP {ip_address} shows no sign of threats."

@tool
def provide_ip_solutions(ip_address:str)->str:
    """"Use this tools to provide solutions related to any paticular IP address if its known for any malicious activity or open ports."""
    print(f"\n[SYSTEM LOG] Running provide_ip_solutions on the IP address {ip_address}...")
    if ip_address in malicious_ips:
        return f"SOLUTION: Block {ip_address} at the perimeter firewall and isolate any internal hosts."
    return f"INFO: {ip_address} is not currently flagged. No actions required."

def main():
    print("Initializing LLM with Tools...")

    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash',
        temperature=0.0
    )

    llm_with_tools = llm.bind_tools([analyze_ip_address,provide_ip_solutions])

    tool_map = {
        'analyze_ip_address':analyze_ip_address,
        'provide_ip_solutions':provide_ip_solutions
    }

    prompt = "Can you check if the IP address 192.168.1.100 is safe? And if found unsafe provide me the fix for that"
    print(f"User:{prompt}\n")

    # response = llm_with_tools.invoke(HumanMessage(content=prompt))
    response = llm_with_tools.invoke(prompt)

    if response.tool_calls:
        print(response.tool_calls)
        print("LLM Descision: I need to use a tool to answer this!")


        for tool_call in response.tool_calls:
           tool_call_name = tool_call["name"]
           tool_call_args = tool_call["args"]
           print(f"Requested Tool: {tool_call_name}")
           print(f"Extracted Arguments: {tool_call_args}")

        if tool_call_name in tool_map and tool_call_name=='analyze_ip_address':
            selected_tool = tool_map[tool_call_name]
            tool_result = selected_tool.invoke(tool_call_args)
            print(f"Result from Tool: {tool_result}")     
    
    else:
        print(f"AI: {response.content}")


if __name__ == "__main__":
    main()