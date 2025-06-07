import asyncio
from aioquic.asyncio.client import connect
from aioquic.quic.configuration import QuicConfiguration
from protocol.messages import *

async def main():
    """
    Establishes a QUIC connection to the server, registers the client,
    negotiates compression options, sends a log message, and performs a heartbeat check.
    """
    config = QuicConfiguration(is_client=True)
    config.verify_mode = False  # Disable certificate verification for testing
    config.server_name = None   # Server name set to None to avoid TLS mismatch

    async with connect("127.0.0.1", 9000, configuration=config) as client:
        reader, writer = await client.create_stream()

        # Register with API key
        writer.write(build_header(MSG_TYPE_REGISTER_REQUEST, payload=DEFAULT_API_KEY.encode()))
        print("🟡 Sent registration request.")
        resp = await reader.read(1024)
        print("✅ Registration raw response:", resp)
        print("✅ Registration parsed:", parse_header(resp))

        # Compression option negotiation
        writer.write(build_header(MSG_TYPE_OPTION_NEGOTIATE_REQ, payload=b"compression:gzip"))
        print("📱 Sent option negotiation request.")
        negotiation = await reader.read(1024)
        print("📱 Option negotiation response:", parse_header(negotiation), negotiation)

        # Send a single log message
        writer.write(build_header(MSG_TYPE_LOG_MESSAGE, payload=b"log: boot success"))
        print("🟡 Sent log message.")
        ack = await reader.read(1024)
        print("✅ Ack raw:", ack)
        print("✅ Ack parsed:", parse_header(ack))

        # Heartbeat request
        writer.write(build_header(MSG_TYPE_HEARTBEAT_REQUEST))
        hb = await reader.read(1024)
        print("🔄 Heartbeat raw:", hb)
        print("🔄 Heartbeat parsed:", parse_header(hb))

        writer.write_eof()

if __name__ == "__main__":
    asyncio.run(main())