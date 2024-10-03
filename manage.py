import os
import sys

def main():
    """Point d'entrée principal pour les commandes Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plm_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Assurez-vous qu'il est installé et "
            "disponible dans votre environnement PYTHONPATH. Activez également "
            "l'environnement virtuel si nécessaire."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
