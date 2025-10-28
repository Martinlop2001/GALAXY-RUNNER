"gestión de la base de datos usando SQLite"

import sqlite3
from typing import List, Dict, Optional
from paths import Paths

class DatabaseManager:
    def __init__(self, db_path: str = None):
        # Si no se proporciona ruta, obtenerla desde Paths
        if db_path is None:
            paths = Paths()
            db_path = str(paths.get_database_path())
        
        self.db_path = db_path
        self.initialize_database()
    
    def initialize_database(self):
        """Inicializar base de datos con las tablas requeridas"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Crear tablas necesarias
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jugadores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    fecha_registro TEXT DEFAULT (datetime('now'))
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS puntuaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jugador_id INTEGER NOT NULL,
                    puntuacion INTEGER NOT NULL,
                    nivel INTEGER NOT NULL DEFAULT 1,
                    tiempo INTEGER NOT NULL DEFAULT 0,
                    estrellas INTEGER NOT NULL DEFAULT 0,
                    combo_maximo INTEGER NOT NULL DEFAULT 0,
                    fecha TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (jugador_id) REFERENCES jugadores(id) ON DELETE CASCADE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ajustes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jugador_id INTEGER NOT NULL,
                    volumen INTEGER NOT NULL DEFAULT 50,
                    dificultad TEXT NOT NULL DEFAULT 'Normal',
                    FOREIGN KEY (jugador_id) REFERENCES jugadores(id) ON DELETE CASCADE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jugador_id INTEGER NOT NULL,
                    partidas INTEGER NOT NULL DEFAULT 0,
                    estrellas_totales INTEGER NOT NULL DEFAULT 0,
                    mejor_combo INTEGER NOT NULL DEFAULT 0,
                    mejor_tiempo INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (jugador_id) REFERENCES jugadores(id) ON DELETE CASCADE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS misiones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    objetivo INTEGER NOT NULL,
                    progreso INTEGER NOT NULL DEFAULT 0,
                    completada INTEGER NOT NULL DEFAULT 0,
                    vigente_desde TEXT DEFAULT (date('now')),
                    vigente_hasta TEXT,
                    tipo TEXT NOT NULL DEFAULT 'diaria'
                )
            """)
            
            conn.commit()
    
    def create_player(self, name: str) -> int:
        """Crear un nuevo jugador y devolver su ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO jugadores (nombre) VALUES (?)", (name,))
            player_id = cursor.lastrowid
            
            # Crear configuraciones y estadísticas por defecto
            cursor.execute("INSERT INTO ajustes (jugador_id) VALUES (?)", (player_id,))
            cursor.execute("INSERT INTO stats (jugador_id) VALUES (?)", (player_id,))
            
            conn.commit()
            return player_id
    
    def get_player(self, name: str) -> Optional[Dict]:
        """Obtener jugador por nombre"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jugadores WHERE nombre = ?", (name,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def save_score(self, player_id: int, score: int, level: int, time: int, 
                   stars: int, max_combo: int):
        """Guardar una nueva puntuación"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO puntuaciones 
                (jugador_id, puntuacion, nivel, tiempo, estrellas, combo_maximo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (player_id, score, level, time, stars, max_combo))
            conn.commit()
    
    def get_leaderboard(self, level: int = None, limit: int = 10) -> List[Dict]:
        """Obtener mejores puntuaciones"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if level:
                cursor.execute("""
                    SELECT p.*, j.nombre 
                    FROM puntuaciones p
                    JOIN jugadores j ON p.jugador_id = j.id
                    WHERE p.nivel = ?
                    ORDER BY p.puntuacion DESC
                    LIMIT ?
                """, (level, limit))
            else:
                cursor.execute("""
                    SELECT p.*, j.nombre 
                    FROM puntuaciones p
                    JOIN jugadores j ON p.jugador_id = j.id
                    ORDER BY p.puntuacion DESC
                    LIMIT ?
                """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def update_statistics(self, player_id: int, games: int = 0, stars: int = 0, 
                          best_combo: int = 0, best_time: int = 0):
        """Actualizar estadísticas del jugador"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE stats SET
                    partidas = partidas + ?,
                    estrellas_totales = estrellas_totales + ?,
                    mejor_combo = MAX(mejor_combo, ?),
                    mejor_tiempo = MAX(mejor_tiempo, ?)
                WHERE jugador_id = ?
            """, (games, stars, best_combo, best_time, player_id))
            conn.commit()
    
    def get_player_stats(self, player_id: int) -> Optional[Dict]:
        """Obtener estadísticas del jugador"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stats WHERE jugador_id = ?", (player_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def create_mission(self, description: str, target: int, kind: str = 'diaria') -> int:
        """Crear una nueva misión"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO misiones (descripcion, objetivo, tipo)
                VALUES (?, ?, ?)
            """, (description, target, kind))
            mission_id = cursor.lastrowid
            conn.commit()
            return mission_id
    
    def get_active_missions(self) -> List[Dict]:
        """Obtener misiones activas"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM misiones 
                WHERE completada = 0 
                AND (vigente_hasta IS NULL OR vigente_hasta >= date('now'))
                ORDER BY vigente_desde DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def update_mission_progress(self, mission_id: int, progress: int):
        """Actualizar progreso de misión"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE misiones 
                SET progreso = progreso + ?
                WHERE id = ?
            """, (progress, mission_id))
            
            # Verificar si la misión está completada
            cursor.execute("""
                SELECT objetivo, progreso FROM misiones WHERE id = ?
            """, (mission_id,))
            row = cursor.fetchone()
            
            if row and row[1] >= row[0]:
                cursor.execute("""
                    UPDATE misiones SET completada = 1 WHERE id = ?
                """, (mission_id,))
            
            conn.commit()
    
    def get_settings(self, player_id: int) -> Optional[Dict]:
        """Obtener configuraciones del jugador"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ajustes WHERE jugador_id = ?", (player_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_settings(self, player_id: int, volume: int = None, difficulty: str = None):
        """Actualizar configuraciones del jugador"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if volume is not None:
                updates.append("volumen = ?")
                params.append(volume)
            
            if difficulty is not None:
                updates.append("dificultad = ?")
                params.append(difficulty)
            
            if updates:
                params.append(player_id)
                cursor.execute(f"""
                    UPDATE ajustes SET {', '.join(updates)}
                    WHERE jugador_id = ?
                """, params)
                conn.commit()
