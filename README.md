# Galaxy Runner

Un juego de tipo "endless runner" desarrollado en Python con Pygame.

## Características

- **3 niveles de dificultad** con jefes únicos al final de cada nivel
- **Sistema de power-ups** con escudos temporales
- **Misiones diarias** con objetivos variados
- **Sistema de puntuación** con combos y estadísticas
- **Base de datos SQLite** para guardar progreso y rankings
- **Dificultad progresiva** que aumenta con el tiempo
- **Interfaz completa** con menús, opciones y ranking
- **Código completamente en español** para facilitar la comprensión y mantenimiento

## Instalación

1. Instala Python 3.7 o superior
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Cómo jugar

1. Ejecuta el juego:
```bash
python main.py
```

2. **Controles:**
   - `←` / `→` o `A` / `D`: Mover nave
   - `P`: Pausar juego
   - `ESC`: Salir al menú principal

3. **Objetivos:**
   - Esquiva meteoritos
   - Recolecta estrellas para puntos
   - Usa power-ups (escudos) para protección
   - Completa misiones diarias
   - Sobrevive el mayor tiempo posible

## Mecánicas del juego

### Power-ups
- **Escudo**: Absorbe un golpe (duración: 6 segundos)

### Sistema de Combos
- Recolecta estrellas consecutivas para aumentar el combo
- El combo se resetea si recibes daño o pasan 3 segundos sin recolectar

### Dificultad Progresiva
- Cada 20 segundos aumenta la velocidad y frecuencia de spawn
- Máximo aumento: +60%

### Niveles
- **Nivel 1**: Tutorial básico
- **Nivel 2**: Velocidad aumentada + Jefe
- **Nivel 3**: Máxima dificultad + Jefe final

### Misiones
- Recolecta estrellas
- Sobrevive tiempo específico
- Alcanza combos altos
- Destruye meteoritos
- Usa power-ups

## Estructura del proyecto

```
galaxy_runner/
├── main.py                 # Punto de entrada principal
├── db.py                   # Gestión de base de datos SQLite
├── paths.py                # Gestión de rutas y recursos
├── ui.py                   # Utilidades de interfaz
├── requirements.txt        # Dependencias
├── scenes/                 # Escenas del juego
│   ├── __init__.py
│   ├── base_scene.py       # Clase base para escenas
│   ├── start_menu.py       # Menú principal
│   ├── game_scene.py       # Escena de juego principal
│   ├── leaderboard_scene.py # Ranking de puntuaciones
│   └── options_scene.py    # Configuraciones
└── res/                    # Recursos (imágenes, sonidos, fuentes)
    ├── img/
    ├── sfx/
    └── fonts/
```

## Base de datos

El juego utiliza SQLite para almacenar:
- **Jugadores**: Información de usuarios
- **Puntuaciones**: Historial de partidas
- **Estadísticas**: Estadísticas acumuladas por jugador
- **Misiones**: Objetivos y progreso
- **Ajustes**: Configuraciones por jugador

## Personalización

Puedes agregar tus propias imágenes en la carpeta `res/img/`:
- `ship.png`: Nave del jugador
- `meteor.png`: Meteoritos
- `star.png`: Estrellas recolectables
- `shield.png`: Power-up de escudo
- `boss1.png`, `boss2.png`, `boss3.png`: Jefes de cada nivel

## Desarrollo

Para contribuir o modificar el juego:

1. El código está completamente en español para facilitar la comprensión
2. Cada escena hereda de `EscenaBase`
3. La lógica del juego está en `EscenaJuego`
4. La base de datos se maneja en `db.py` con métodos en español
5. Todas las clases, funciones y variables están traducidas al español

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
