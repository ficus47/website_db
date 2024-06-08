import asyncio
import websockets

async def hello():
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as websocket:
        with open("video.mp4", "rb") as video_file:
            video_data = video_file.read()
        await websocket.send(video_data)
        response = await websocket.recv()
        print(response)

asyncio.run(hello())
