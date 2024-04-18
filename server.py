import asyncio

async def handle_client(reader, writer):
    global currentId, pos
    writer.write(str.encode(currentId))
    await writer.drain()

    currentId = "1"
    while True:
        try:
            data = await reader.read(2048)
            reply = data.decode('utf-8')
            if not data:
                writer.write(str.encode("Adios"))
                await writer.drain()
                break
            else:
                print("Recibiendo: " + reply)
                # Divide las posiciones de los gusanos separadas por '|' y actualiza ambas posiciones
                positions = reply.split('|')
                for position in positions:
                    arr = position.split(":")
                    client_id = int(arr[0])
                    pos[client_id] = position

                # Envía ambas posiciones al cliente correspondiente
                writer.write(str.encode(pos[client_id]))
                await writer.drain()
        except:
            break

    print("Conexion cerrada")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '10.10.0.36', 5555)

    async with server:
        await server.serve_forever()

currentId = "0"
pos = ["0:50,50", "1:100,100"]

asyncio.run(main())
