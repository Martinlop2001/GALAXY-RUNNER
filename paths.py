"""
Gestión de rutas para Galaxy Runner
Gestiona todas las rutas de archivos y la carga de recursos.
"""

from pathlib import Path
import os

class Paths:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.resources = self.project_root / "res"
        self.images = self.resources / "img"
        self.sounds = self.resources / "sfx"
        self.fonts = self.resources / "fonts"
        self.database = self.project_root / "galaxy_runner.db"
        
        # Crear directorios si no existen
        self._create_directories()
    
    def _create_directories(self):
        """Crear directorios necesarios"""
        directories = [
            self.resources,
            self.images,
            self.sounds,
            self.fonts
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_image_path(self, filename):
        """Obtener ruta a un archivo de imagen"""
        return self.images / filename
    
    def get_sound_path(self, filename):
        """Obtener ruta a un archivo de sonido"""
        return self.sounds / filename
    
    def get_font_path(self, filename):
        """Obtener ruta a un archivo de fuente"""
        return self.fonts / filename
    
    def get_database_path(self):
        """Obtener ruta al archivo de base de datos"""
        return self.database
