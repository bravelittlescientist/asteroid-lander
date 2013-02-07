"""Tools to build a client. Each player or user will run a separate client. The client can connect
and disconnect from a server. Once connected, the client sends commands to the server, and receives
state representations of the world. The client must intelligently interpolate those
states to provide a smooth feel. Some game objects may also be simulated on the client according
to the same physics as they are modelled on the server using client-side prediction, but must
handle cases where it is incorrect.

Generally, your project's should always start by subclassing astral.client.gameclient.GameClient
Any game objects modelled by the server will be represented on the client by a
subclass of astral.client.local.RemoteObject."""