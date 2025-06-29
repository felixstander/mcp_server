import asyncio

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient

from langchain_model import ChatOpenRouter
from mcp_server import adjacent_area

client = MultiServerMCPClient(
    {
        "adjacent_area":{
                    "url":"http://127.0.0.1:8000/mcp",
                    "transport":"streamable_http"
    }
     }
)
async def main():

    print("\n--- 1. 发现可用工具 ---")
    available_tools =  await client.get_tools()
    print(f"发现 {len(available_tools)} 个工具:")
    for t in available_tools:
        print(f"  - 名称: {t.name}")
        print(f"    描述: {t.description}")
        # print(f"    参数: {t.args_schema.schema()['properties'] if t.args_schema else '无'}")


    area_input = {'area_gps':[('南山区','113.92,22.52'),('福田区','114.05,22.53'),('罗湖区','114.12,22.55')]}

    tool_map = {t.name: t for t in available_tools}

    adjacent_area_tool = tool_map['adjacent_area']
    result = await adjacent_area_tool.ainvoke(input = area_input)
    print(result)


if __name__ == "__main__":
    # asyncio.run(main())

    # llm = ChatGoogleGenerativeAI(
    #     model="gemini-2.0-flash",
    #     temperature=0,
    #     max_tokens=None,
    #     timeout=None,
    #     max_retries=2,
    #     # other params...
    # )

    llm = ChatOpenRouter(
        model_name="openai/gpt-4o"
)
    messages = [
    (
        "system",
        "You are a helpful assistant that translates English to Chinese. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
    ai_msg = llm.invoke(messages)
    print(ai_msg)

