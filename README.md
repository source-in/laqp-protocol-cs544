# LAQP - Log Aggregation QUIC Protocol

**Student:** Saurabh Sawant
**Course:** CS 544 – Computer Networks
**Project:** Protocol Implementation – Part 3

---

## 🔧 Overview

This project implements a reliable and extensible **Log Aggregation Protocol** over the QUIC transport layer. The client securely connects to the server and supports registration, log message transmission, compression negotiation, and heartbeat checks.

---

## 💪 Features Implemented

### ✅ QUIC-based Transport Layer

- Uses [aioquic](https://github.com/aiortc/aioquic) for encrypted, multiplexed connections over UDP.

### ✅ Client Registration

- `MSG_TYPE_REGISTER_REQUEST` / `MSG_TYPE_REGISTER_RESPONSE`
- Clients must register using a static API key.

### ✅ Log Submission

- `MSG_TYPE_LOG_MESSAGE` allows clients to send logs.
- Each message is acknowledged using `MSG_TYPE_ACKNOWLEDGEMENT`.

### ✅ Option Negotiation

- `MSG_TYPE_OPTION_NEGOTIATE_REQ` negotiates compression options.
- Current support: `gzip`, `no compression`.

### ✅ Heartbeat Mechanism

- Periodic health check with `MSG_TYPE_HEARTBEAT_REQUEST` and `MSG_TYPE_HEARTBEAT_RESPONSE`.

### ✅ Error Handling

- `MSG_TYPE_ERROR_RESPONSE` is used for malformed or out-of-order messages.
- Includes error codes for easier debugging.

---

## 📆 Folder Structure

```
laqp/
├── client/
│   └── client.py
├── server/
│   └── server.py
├── protocol/
│   ├── constants.py
│   ├── dfa.py
│   └── messages.py
├── certs/
│   ├── cert.pem
│   └── key.pem
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛡️ Certificate Setup (QUIC over TLS)

Generate a self-signed certificate for testing:

```bash
mkdir certs
openssl req -newkey rsa:2048 -nodes -keyout certs/key.pem -x509 -days 365 -out certs/cert.pem
```

Use `localhost` as the Common Name (CN) during setup.

---

## 💪 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd laqp
```

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Project

### Start Server

```bash
PYTHONPATH=. python server/server.py
```

### Start Client

```bash
PYTHONPATH=. python client/client.py
```

Ensure both are run from the root directory of the project.

---

## 🧪 Message Types

| Code | Message Type         |
| ---- | -------------------- |
| 1    | REGISTER_REQUEST     |
| 2    | REGISTER_RESPONSE    |
| 3    | LOG_MESSAGE          |
| 4    | LOG_BATCH            |
| 5    | ACKNOWLEDGEMENT      |
| 6    | OPTION_NEGOTIATE_REQ |
| 7    | HEARTBEAT_REQUEST    |
| 8    | HEARTBEAT_RESPONSE   |
| 9    | ERROR_RESPONSE       |

---

## ✅ Example Output

```
🟡 Sent registration request.
✅ Registration parsed: {'msg_type': 2, ...}
📱 Sent option negotiation request.
📱 Option negotiation response: compression:gzip
🟡 Sent log message.
✅ Ack parsed: {'msg_type': 5, ...}
🔄 Heartbeat parsed: {'msg_type': 8, ...}
```

---

## 📙 Future Improvements

- Support for batch logging (`MSG_TYPE_LOG_BATCH`)
- Dynamic API key authentication
- Real-time compression of logs using gzip/zstd

---

## 📖 License

This project is for academic use under Drexel University's CS 544 course.
