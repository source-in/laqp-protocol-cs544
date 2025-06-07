import asyncio
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from protocol.messages import *
from protocol.dfa import ServerDFA, ClientState
import struct

dfa = ServerDFA()

class LAQPServerProtocol:
    def __init__(self, stream_id, quic, stream_reader, stream_writer):
        self.stream_id = stream_id or 0
        self.quic = quic
        self.reader = stream_reader
        self.writer = stream_writer
        self.client_id = None

    async def handle(self):
        print(f"📶 Stream {self.stream_id} opened.")
        while True:
            data = await self.reader.read(1024)
            if not data:
                print(f"❌ Stream {self.stream_id} closed.")
                break

            header = parse_header(data)
            if not header:
                print("⚠️ Invalid header received.")
                self.writer.write(build_header(MSG_TYPE_ERROR_RESPONSE, payload=b"Invalid header"))
                await self.writer.drain()
                continue

            msg_type = header["msg_type"]
            payload = data[struct.calcsize(HEADER_FMT):]

            if not dfa.validate_transition(self.client_id or self.stream_id, msg_type):
                print(f"🚫 Invalid transition: msg_type={msg_type}")
                self.writer.write(build_header(MSG_TYPE_ERROR_RESPONSE, payload=b"Invalid transition"))
                await self.writer.drain()
                continue

            if msg_type == MSG_TYPE_REGISTER_REQUEST:
                if payload.decode() != DEFAULT_API_KEY:
                    print(f"❌ Invalid API key: {payload.decode()}")
                    self.writer.write(build_header(MSG_TYPE_ERROR_RESPONSE, payload=b"Invalid API Key"))
                    await self.writer.drain()
                    continue
                self.client_id = self.stream_id
                dfa.set_state(self.client_id, ClientState.REGISTERED)
                print(f"✅ Client {self.client_id} registered.")
                self.writer.write(build_header(MSG_TYPE_REGISTER_RESPONSE))
                await self.writer.drain()

            elif msg_type == MSG_TYPE_OPTION_NEGOTIATE_REQ:
                print(f"🧠 Option negotiation from client {self.client_id}")
                dfa.set_state(self.client_id, ClientState.NEGOTIATED)
                self.writer.write(build_header(MSG_TYPE_ACKNOWLEDGEMENT, payload=b"compression:gzip"))
                await self.writer.drain()

            elif msg_type == MSG_TYPE_LOG_MESSAGE:
                print(f"📥 Received log from client {self.client_id}")
                self.writer.write(build_header(MSG_TYPE_ACKNOWLEDGEMENT))
                await self.writer.drain()

            elif msg_type == MSG_TYPE_HEARTBEAT_REQUEST:
                print(f"❤️ Heartbeat from client {self.client_id}")
                self.writer.write(build_header(MSG_TYPE_HEARTBEAT_RESPONSE))
                await self.writer.drain()

async def handle_stream(stream_reader, stream_writer):
    print("🔗 New QUIC stream opened.")
    protocol = LAQPServerProtocol(stream_id=0, quic=None, stream_reader=stream_reader, stream_writer=stream_writer)
    await protocol.handle()

async def main():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain("certs/cert.pem", "certs/key.pem")
    print("🚀 LAQP Server starting on 127.0.0.1:9000...")

    await serve(
        "127.0.0.1", 9000,
        configuration=config,
        stream_handler=lambda r, w: asyncio.create_task(handle_stream(r, w))
    )
    print("✅ LAQP Server is now running. Waiting for clients...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
