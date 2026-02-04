import sys
import os
import asyncio

# Import Hack
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.server.models import InitializationOptions
from mcp.server import NotificationService, Server
from mcp.server.stdio import stdio_server
import mcp.types as types

try:
    from logic import GarbageLogic
except ImportError as e:
    print(f"Import error: {e}", file=sys.stderr)
    class GarbageLogic:
        async def get_tp_realtime(self, **kwargs): return {"error": "Logic import failed"}
        async def get_tp_stations(self, **kwargs): return {"error": "Logic import failed"}

server = Server("mcp-tw-garbage")
logic = GarbageLogic()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_tp_realtime_location",
            description="獲取台北市垃圾車即時位置資訊 (Taipei Real-time Garbage Truck Location)",
            inputSchema={
                "type": "object",
                "properties": {
                    "car_number": {"type": "string", "description": "選填，過濾特定車號"}
                }
            },
        ),
        types.Tool(
            name="search_tp_garbage_stations",
            description="搜尋台北市垃圾清運點資訊 (Search Taipei Garbage Collection Stations)",
            inputSchema={
                "type": "object",
                "properties": {
                    "district": {"type": "string", "description": "行政區 (如：中山區、大安區)"},
                    "keyword": {"type": "string", "description": "地址或清運點關鍵字"}
                }
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "get_tp_realtime_location":
        car_number = arguments.get("car_number") if arguments else None
        results = await logic.get_tp_realtime(car_number)
        return [types.TextContent(type="text", text=str(results))]
    
    elif name == "search_tp_garbage_stations":
        district = arguments.get("district") if arguments else None
        keyword = arguments.get("keyword") if arguments else None
        results = await logic.get_tp_stations(district, keyword)
        return [types.TextContent(type="text", text=str(results))]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-tw-garbage",
                server_version="0.1.0",
                capabilities=server.get_capabilities(),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
