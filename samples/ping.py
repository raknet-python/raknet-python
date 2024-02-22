import argparse
import struct

import raknet
from raknet import RakPeer, MessageIdentifiers


def main(port: int):
    # https://wiki.vg/Raknet_Protocol#Unconnected_Pong
    message = "MCPE;Dedicated Server;390;1.14.60;0;10;13253860892328930865;Bedrock level;Survival;1;19132;19133;"
    server = RakPeer()
    server.offline_ping_response = struct.pack(">H", len(message)) + message.encode("utf-8")
    server.max_incoming_connections = 10
    server.startup(port=port, max_connections=10)

    client = RakPeer()
    client.startup()
    while True:
        client.ping("127.0.0.1", port)
        packet = client.receive()
        if not packet:
            continue
        if packet.data[0] == MessageIdentifiers.ID_UNCONNECTED_PONG:
            ping_time = struct.unpack(">I", packet.data[1:5])[0]
            print(f"ID_UNCONNECTED_PONG from SystemAddress {packet.system_address}")
            print(f"Time is {ping_time}")
            print(f"Ping is {(raknet.time_ms() - ping_time)}ms")
            print(f"Data is {len(packet.data[5:])} bytes long")
            if len(packet.data[5:]) > 0:
                print(f"Data is {packet.data[5:]}")

            client.shutdown(0.1)
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample of sending pings using raknet-python")
    parser.add_argument("--port", type=int, default=19132, help="The port to ping on the host.")
    args = parser.parse_args()
    main(args.port)
