import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient

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
    asyncio.run(main())

