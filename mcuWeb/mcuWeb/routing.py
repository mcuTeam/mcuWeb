# In routing.py
from channels.routing import route
from fun.consumers import ws_message,ws_connect

channel_routing = [
    # route("websocket.receive", ws_message),
    route("websocket.connect", ws_connect),
    # route("websocket.disconnect", ws_disconnect),
    #
    # route("websocket.keepalive", ws_keepalive),
]
