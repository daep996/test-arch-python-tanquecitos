# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = "#f1c40f"
SCORE_COLOR = "#c0c0c07b"

# Configuración del juego
PLAYER_POSITIONS = [
    (100, 100),   # Jugador 1 (tank1.png) - Esquina superior izquierda
    (700, 100),   # Jugador 2 (tank2.png) - Esquina superior derecha
    (100, 500),   # Jugador 3 (tank3.png) - Esquina inferior izquierda
    (700, 500)    # Jugador 4 (tank4.png) - Esquina inferior derecha
]
FONT_SIZE = 50

# Network settings
SERVER_URL = 'http://localhost:5000'
SYNC_RATE = 1/60  # 60 veces por segundo
MAX_PLAYERS = 4
