import struct
from protocol.constants import *

HEADER_FMT = "!B H H B H"  # version, msg_type, request_id, flags, length

def build_header(msg_type, request_id=0, payload=b""):
    length = len(payload) + struct.calcsize(HEADER_FMT)
    header = struct.pack(HEADER_FMT, PROTOCOL_VERSION, msg_type, request_id, 0, length)
    return header + payload

def parse_header(data):
    if len(data) < struct.calcsize(HEADER_FMT):
        return None
    version, msg_type, request_id, flags, length = struct.unpack(HEADER_FMT, data[:8])
    return {
        "version": version,
        "msg_type": msg_type,
        "request_id": request_id,
        "flags": flags,
        "length": length
    }

