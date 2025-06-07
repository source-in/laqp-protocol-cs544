class ClientState:
    INIT = 0
    REGISTERED = 1
    NEGOTIATED = 2

class ServerDFA:
    def __init__(self):
        self.states = {}

    def get_state(self, client_id):
        return self.states.get(client_id, ClientState.INIT)

    def set_state(self, client_id, state):
        self.states[client_id] = state

    def validate_transition(self, client_id, msg_type):
        state = self.get_state(client_id)
        if state == ClientState.INIT and msg_type == 1:  # REGISTER_REQUEST
            return True
        if state == ClientState.REGISTERED and msg_type in (3, 5, 6, 7):  # Allow OPTION_NEGOTIATE_REQ
            return True
        if state == ClientState.NEGOTIATED and msg_type in (3, 7):  # LOG_MESSAGE, HEARTBEAT
            return True
        return False
