import asyncio
from asyncio.streams import StreamReader, StreamWriter

async def handle_client(reader: StreamReader, writer):
    
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Получено {message!r} от {addr!r}")
    response = f"Обработано: {message!r}"
    writer.write(response.encode())
    await writer.drain()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 12345)

    addr = server.sockets[0].getsockname()
    print(f'Сервер запущен на {addr}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())