import websockets
import asyncio

class WSserver():
    async def handle(self,websocket,path):
        recv_msg = await websocket.recv()
        recv_msg = recv_msg.decode(encoding = "utf-8")
        print("i received %s" %recv_msg)
        await websocket.send('server send ok'.encode(encoding = "utf-8"))
    def run(self):
        ser = websockets.serve(self.handle,"127.0.0.1","8240")
        asyncio.get_event_loop().run_until_complete(ser)
        asyncio.get_event_loop().run_forever()
ws = WSserver();
ws.run()