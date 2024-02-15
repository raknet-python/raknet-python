#ifdef NDEBUG
#undef NDEBUG
#endif

#include "raknet/BitStream.h"
#include "raknet/GetTime.h"
#include "raknet/MessageIdentifiers.h"
#include "raknet/RakNetTypes.h"
#include "raknet/RakPeerInterface.h"
#include <cassert>
#include <cstdio>
#include <cstring>

int main() {
  constexpr auto server_port = 60000;
  RakNet::RakPeerInterface *server = RakNet::RakPeerInterface::GetInstance();
  const char *response_data = "Hello World From RakNet";
  server->SetOfflinePingResponse(response_data, strlen(response_data) + 1);
  server->SetMaximumIncomingConnections(2);
  RakNet::SocketDescriptor socketDescriptor(server_port, nullptr);
  assert(server->Startup(2, &socketDescriptor, 1) == RakNet::RAKNET_STARTED);

  RakNet::RakPeerInterface *client = RakNet::RakPeerInterface::GetInstance();
  socketDescriptor.port = 0;
  client->Startup(1, &socketDescriptor, 1);

  client->Ping("127.0.0.1", server_port, false);
  bool done = false;
  while (!done) {
    RakNet::Packet *p;
    bool packet_from_server;

    p = server->Receive();
    if (p) {
      packet_from_server = true;
    } else {
      packet_from_server = false;
      p = client->Receive();
    }

    if (!p) {
      continue;
    }

    switch (p->data[0]) {
    case ID_UNCONNECTED_PONG: {
      printf("ID_UNCONNECTED_PONG from SystemAddress %s.\n",
             p->systemAddress.ToString(true));

      RakNet::BitStream is(p->data, p->length, false);
      is.IgnoreBytes(1);
      assert(BITS_TO_BYTES(is.GetReadOffset()) == 1);

      RakNet::TimeMS time;
      is.Read(time);
      printf("Time is %i\n", time);
      printf("Ping is %i\n", RakNet::GetTimeMS() - time);
      assert(BITS_TO_BYTES(is.GetReadOffset()) == 1 + sizeof(RakNet::TimeMS));

      auto data_length =
          is.GetNumberOfBytesUsed() - BITS_TO_BYTES(is.GetReadOffset());
      printf("Data is %i bytes long.\n", data_length);
      assert(data_length == strlen(response_data) + 1);

      const char *data = reinterpret_cast<const char *>(
          p->data + BITS_TO_BYTES(is.GetReadOffset()));
      printf("Data is %s\n", data);
      assert(strncmp(data, response_data, data_length) == 0);

      done = true;
      client->Shutdown(100);
      break;
    }
    case ID_UNCONNECTED_PING:
    case ID_UNCONNECTED_PING_OPEN_CONNECTIONS:
      break;
    }

    if (packet_from_server) {
      server->DeallocatePacket(p);
    } else {
      client->DeallocatePacket(p);
    }
  }

  RakNet::RakPeerInterface::DestroyInstance(client);
  RakNet::RakPeerInterface::DestroyInstance(server);

  return 0;
}