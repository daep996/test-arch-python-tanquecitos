# Tanquecitos - Juego Multijugador en Tiempo Real

Un juego multijugador de tanques desarrollado con Python, Pygame y Socket.IO que permite a múltiples jugadores competir en tiempo real.

## 🚀 Características

- Juego multijugador en tiempo real
- Sistema de vidas y respawn
- Colisiones y física de proyectiles
- Interfaz gráfica intuitiva
- Sincronización de estado en tiempo real

## 📋 Requisitos

- Python 3.x
- Pygame
- Python-SocketIO
- Eventlet

## 🛠️ Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/daep996/test-arch-python-tanquecitos
cd test-pygame
```

2. Crear y activar un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
# o
.venv\Scripts\activate  # En Windows
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

### Paquetes usados:

- pygame: Para el desarrollo del juego y la interfaz gráfica
- python-socketio: Para la comunicación en tiempo real entre cliente y servidor
- eventlet: Para el servidor asíncrono de Socket.IO

## 🎮 Ejecución

### Servidor

Para iniciar el servidor:
```bash
python server.py
```
El servidor se ejecutará en el puerto 5000 por defecto.

### Cliente

Para iniciar el cliente:
```bash
python game.py
```

## 🏗️ Estructura del Proyecto

```
test-pygame/
├── assets/              # Recursos gráficos
├── game.py             # Cliente principal del juego
├── server.py           # Servidor Socket.IO
├── network.py          # Gestión de la comunicación en red
├── sprites.py          # Clases de sprites del juego
├── bullet.py           # Lógica de proyectiles
└── config.py           # Configuración global
```

## 🔄 Arquitectura y Comunicación

### Arquitectura Cliente-Servidor

El juego utiliza una arquitectura cliente-servidor con Socket.IO para la comunicación en tiempo real:

1. **Servidor (server.py)**
   - Gestiona las conexiones de los jugadores
   - Mantiene el estado del juego
   - Coordina las interacciones entre jugadores
   - Maneja la lógica de colisiones y eliminación

2. **Cliente (game.py)**
   - Renderiza la interfaz gráfica
   - Procesa la entrada del usuario
   - Sincroniza el estado con el servidor
   - Maneja la física local

### Sistema de Comunicación

El juego utiliza Socket.IO para la comunicación en tiempo real:

1. **Eventos del Servidor**
   - `connect`: Maneja nuevas conexiones
   - `disconnect`: Gestiona desconexiones
   - `player_update`: Actualiza posiciones de jugadores
   - `shoot`: Maneja disparos
   - `player_hit`: Procesa impactos

2. **Eventos del Cliente**
   - `player_number`: Asigna número de jugador
   - `players_update`: Actualiza lista de jugadores
   - `game_state`: Sincroniza estado del juego
   - `bullet_fired`: Notifica disparos
   - `player_eliminated`: Maneja eliminaciones

## 💡 Buenas Prácticas Implementadas

1. **Separación de Responsabilidades**
   - Módulos independientes para cada funcionalidad
   - Clases bien definidas con responsabilidades únicas
   - Separación clara entre lógica de red y juego

2. **Manejo de Errores**
   - Try-catch para conexiones de red
   - Validación de datos recibidos
   - Manejo de desconexiones

3. **Optimización**
   - Uso de grupos de sprites para renderizado eficiente
   - Actualizaciones selectivas de estado
   - Gestión eficiente de memoria

4. **Código Limpio**
   - Nombres descriptivos de variables y funciones
   - Documentación clara
   - Estructura modular y mantenible

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 