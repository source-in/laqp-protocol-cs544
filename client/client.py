import asyncio
from aioquic.asyncio.client import connect
from aioquic.quic.configuration import QuicConfiguration
from protocol.messages import *

async def main():
    config = QuicConfiguration(is_client=True)
    config.verify_mode = False
    config.server_name = None

    async with connect("127.0.0.1", 9000, configuration=config) as client:
        reader, writer = await client.create_stream()

        # Register
        writer.write(build_header(MSG_TYPE_REGISTER_REQUEST, payload=DEFAULT_API_KEY.encode()))
        print("🟡 Sent registration request.")
        resp = await reader.read(1024)
        print("✅ Registration raw response:", resp)
        print("✅ Registration parsed:", parse_header(resp))

        # Option Negotiation
        writer.write(build_header(MSG_TYPE_OPTION_NEGOTIATE_REQ, payload=b"compression:gzip"))
        print("📡 Sent option negotiation request.")
        negotiation = await reader.read(1024)
        print("📡 Option negotiation response:", parse_header(negotiation), negotiation)

        # Send log
        writer.write(build_header(MSG_TYPE_LOG_MESSAGE, payload=b"log: boot success"))
        print("🟡 Sent log message.")
        ack = await reader.read(1024)
        print("✅ Ack raw:", ack)
        print("✅ Ack parsed:", parse_header(ack))

        # Heartbeat
        writer.write(build_header(MSG_TYPE_HEARTBEAT_REQUEST))
        hb = await reader.read(1024)
        print("🔄 Heartbeat raw:", hb)
        print("🔄 Heartbeat parsed:", parse_header(hb))

        writer.write_eof()

if __name__ == "__main__":
    asyncio.run(main())
