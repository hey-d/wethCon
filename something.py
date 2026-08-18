import os 
import json

from dotenv import load_dotenv
from groq import Groq

from tools import weather_city


load_dotenv()


client = Groq(
    api_key = os.getenv("groq_api_key")
)



tools = [
    {
        "type": "function",
        "function": {
            "name": "weather_city",
            "description": "get the current weather temperature of a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "the name of the city to get the wether temperature for"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

user_input = input("Hey: ")

messages = [
    {
        "role": "system", 
        "content": "you are a helpful assistant that provides the current weathe temperature of a city in celsius. you can use the weather_city tool to get the current weathe temperature of a city in celsius. you should only use the weather_city tool when user asks to access or fetch the current weather temperature for a city otherwise do not use it"
    },
    {
        "role": "user",
        "content": user_input
    }
]

max_iterations = 5

for iteration in range(max_iterations):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = messages,
        tools = tools,
        tool_choice = "auto"
    )
    
    message = response.choices[0].message   
    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print("\n agent decided to use: ", function_name)
            print("\n arguments: ", function_args)
            
            if function_name == "weather_city":
                result = weather_city(function_args["city"])
            
                print("\n tool result: ", result)
                
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    }
                )
    
    if not message.tool_calls:
        print("\nAI: ", message.content)
        break
 
else:
    print("max iterations reached, exiting...")           
