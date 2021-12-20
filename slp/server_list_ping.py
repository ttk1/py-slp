import socket
from io import BytesIO
import argparse

from slp.varint import from_int, to_int


class ServerListPing():
    def __init__(self, host: str, port: int, protocol_version: int = -1):
        self.host = host
        self.port = port
        self.protocol_version = protocol_version
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.sock.connect((host, port))

    def _sendall(self, payload: bytes):
        self.sock.sendall(from_int(len(payload)) + payload)

    def _read(self, length: int) -> bytes:
        packet_data = self.sock.recv(length)
        if len(packet_data) < length:
            raise Exception('Received few bytes!')
        return packet_data

    def _read_varint(self) -> int:
        b = b''
        while True:
            t = self._read(1)
            b += t
            if t[0] & 0b1000_0000 == 0:
                break
        return to_int(BytesIO(b))

    def _handshake(self):
        payload = (
            # Packet ID = 0x00
            b'\x00' +
            # Protcol Version
            from_int(self.protocol_version) +
            # Host
            from_int(len(self.host)) +
            self.host.encode(encoding='utf-8') +
            # Port
            self.port.to_bytes(2, byteorder='big') +
            # Next state
            from_int(1)
        )
        self._sendall(payload)

    def _request(self):
        payload = (
            # Packet ID = 0x00
            b'\x00'
        )
        self._sendall(payload)

    def _response(self) -> str:
        # Packet Length
        length = self._read_varint()
        # Payload
        payload = BytesIO(self._read(length))
        # Packet ID
        packet_id = payload.read1(1)
        if packet_id != b'\x00':
            raise Exception(f'Invalid Packet ID: {packet_id}')
        # JSON Response
        length = to_int(payload)
        res = payload.read1(length)
        return res.decode(encoding='utf-8')

    def execute(self) -> str:
        self._handshake()
        self._request()
        return self._response()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='host name', type=str)
    parser.add_argument('-p', '--port', help='port number',
                        type=int, default=25565)
    args = parser.parse_args()
    print(ServerListPing(args.host, args.port).execute())
