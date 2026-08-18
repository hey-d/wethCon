import os
import json

from dotenv import load_dotenv
from groq import Groq

from tools import weather_city, calculator 

load_dotenv()


client = Groq(
    api_key = os.getenv("groq_api_key")
)



tools =[
    {
        "type":"function",
        "function": {
            "name": "weather_city",
            "description": "get the current weather temperature of the given city in degree celsius",
            "parameters":{
                "type": "object",
                "properties":{
                    "city": {
                        "type": "string",
                        "description": "the name of the city whose temperature is to be fetched"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "to solve any mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "mathematical expression that needs to be evaluated"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

user_input = input("Hey: ")

messages = [
    {
        "role": "system",
        "content": "you are a helpful assistant that provides the current weather temperature for the given city. remember we have a weather_city tool to fetch the current weather temperature for the city. so choose the weathre_city tool only when the user asks to access or fetch the current weather toemperature for a city otherwise do not choose the tool"
    },
    {
        "role": "user", 
        "content": user_input
    }
]

max_iterations = 5

for iteration in range(max_iterations):
    response = client.chat.completions.create(
        model = "openai/gpt-oss-120b",
        messages = messages,
        tools = tools,
        tool_choice = "auto"
    )
    
    message = response.choices[0].message
    messages.append(message)
    
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            print("Tool chosen for this service: ", function_name)
            if function_name=="weather_city":
                arguments = json.loads(tool_call.function.arguments)
                print("\nThe arguments for the tool is", arguments)
                
                result = weather_city(
                    arguments["city"]
                )
                
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    }
                )
            elif function_name == "calculator":
                arguments = json.loads(tool_call.function.arguments)
                
                print("\nthe tool chosen for this is:  ", function_name)
                print("\n arguments for this tool are: ", arguments)
                
                
                result = calculator(
                    expression=arguments["expression"]
                )
                
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    }
                )
            
    else:
        print ("AI result: ", message.content)
        print(message)
        break
        
else:
    print("max iterations reached, breaking...")
        
    