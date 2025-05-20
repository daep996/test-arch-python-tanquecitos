import socketio
from config import SERVER_URL

class NetworkManager:
    def __init__(self, game):
        self.sio = socketio.Client()
        self.game = game
        self.player_number = None
        self.setup_events()

    def setup_events(self):
        def on_connect():
            print('Connected to server')

        def on_disconnect():
            print('Disconnected from server')

        def on_player_number(data):
            self.player_number = data['number']
            self.game.setup_multiplayer(data['number'], data['total_players'])

        def on_players_update(data):
            self.game.update_players_list(data)

        def on_game_state(data):
            self.game.update_other_players(data)

        def on_bullet_fired(data):
            self.game.handle_remote_shot(data)

        def on_player_eliminated(data):
            self.game.handle_player_elimination(data)

        # Registrar los eventos
        self.sio.on('connect', on_connect)
        self.sio.on('disconnect', on_disconnect)
        self.sio.on('player_number', on_player_number)
        self.sio.on('players_update', on_players_update)
        self.sio.on('game_state', on_game_state)
        self.sio.on('bullet_fired', on_bullet_fired)
        self.sio.on('player_eliminated', on_player_eliminated)

    def connect_to_server(self):
        try:
            self.sio.connect(SERVER_URL)
            return True
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return False

    def send_player_update(self, data):
        if self.sio.connected:
            self.sio.emit('player_update', data)

    def send_shot(self, data):
        if self.sio.connected:
            self.sio.emit('shoot', data)

    def report_hit(self, target_player):
        if self.sio.connected:
            self.sio.emit('player_hit', {'target': target_player})

    def disconnect(self):
        if self.sio.connected:
            self.sio.disconnect()
