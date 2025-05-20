import socketio
import eventlet
from config import *

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Almacenar información de los jugadores
players = {}

@sio.event
def connect(sid, environ):
    print(f'Player connected: {sid}')
    if len(players) < MAX_PLAYERS:
        player_number = len(players)
        players[sid] = {
            'position': PLAYER_POSITIONS[player_number],
            'angle': 0,
            'player_number': player_number,
            'alive': True,
            'lives': 3
        }
        # Enviar información inicial al jugador
        sio.emit('player_number', {
            'number': player_number,
            'total_players': len(players)
        }, room=sid)
        
        # Notificar a todos los jugadores del nuevo jugador
        sio.emit('players_update', players)
        print(f'Sent player_number {player_number} to {sid}')
        print(f'Current players: {players}')
    else:
        return False  # Rechazar conexión si ya hay MAX_PLAYERS jugadores

@sio.event
def disconnect(sid):
    if sid in players:
        del players[sid]
        print(f'Player disconnected: {sid}')
        # Notificar a todos los jugadores restantes
        sio.emit('players_update', players)

@sio.event
def player_update(sid, data):
    if sid in players:
        players[sid].update(data)
        # Emitir actualización a todos excepto al remitente
        sio.emit('game_state', players, skip_sid=sid)

@sio.event
def shoot(sid, data):
    if sid in players:
        # Incluir información del jugador que dispara
        data['player_number'] = players[sid]['player_number']
        sio.emit('bullet_fired', data)

@sio.event
def player_hit(sid, data):
    if sid in players and 'target' in data:
        target_sid = data['target']
        if target_sid in players:
            if players[target_sid]['alive']:
                players[target_sid]['alive'] = False
                players[target_sid]['lives'] -= 1
                sio.emit('player_eliminated', {
                    'player': target_sid,
                    'eliminated_by': sid,
                    'lives': players[target_sid]['lives']
                })

if __name__ == '__main__':
    print(f"Starting server on port 5000...")
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
