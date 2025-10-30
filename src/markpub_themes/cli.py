import argparse
from pathlib import Path
import shutil
import sys
from . import get_theme_path, list_themes, __version__

def clone_theme(theme_name, destination):
    """Clone a theme to a destination directory."""
    try:
        source = Path(get_theme_path(theme_name))
        dest = Path(destination).expanduser().resolve()

        if dest.exists():
            print(f"Error: Destination '{dest}' already exists", file=sys.stderr)
            return 1

        shutil.copytree(source, dest)
        print(f"Theme '{theme_name}' cloned to {dest}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(f"Available themes: {', '.join(list_themes())}")
        return 1
    except Exception as e:
        print(f"Error cloning theme: {e}", file=sys.stderr)
        return 1

def activate_theme(theme_name, config_file=None):
    """Activate a theme (sets it as the active theme)."""
    try:
        # Verify theme exists
        theme_path = get_theme_path(theme_name)

        # If config_file is provided, write to it
        if config_file:
            config_path = Path(config_file).expanduser().resolve()
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                f.write(f"MARKPUB_THEME={theme_name}\n")
            print(f"Theme '{theme_name}' activated in {config_path}")
        else:
            # Otherwise just show the theme path
            print(f"Theme '{theme_name}' is available at: {theme_path}")
            print(f"\nTo activate, set MARKPUB_THEME environment variable:")
            print(f"  export MARKPUB_THEME={theme_name}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(f"Available themes: {', '.join(list_themes())}")
        return 1
    except Exception as e:
        print(f"Error activating theme: {e}", file=sys.stderr)
        return 1

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='markpub-themes',
        description='Manage markpub themes'
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List command
    list_parser = subparsers.add_parser('list', help='List available themes')

    # Clone command
    clone_parser = subparsers.add_parser('clone', help='Clone a theme to a directory')
    clone_parser.add_argument('theme', help='Name of the theme to clone')
    clone_parser.add_argument('destination', help='Destination directory')

    # Activate command
    activate_parser = subparsers.add_parser('activate', help='Activate a theme')
    activate_parser.add_argument('theme', help='Name of the theme to activate')
    activate_parser.add_argument('-c', '--config', help='Config file to write activation to')

    args = parser.parse_args()

    if args.command == 'list':
        themes = list_themes()
        print("Available themes:")
        for theme in themes:
            print(f"  - {theme}")
        return 0
    elif args.command == 'clone':
        return clone_theme(args.theme, args.destination)
    elif args.command == 'activate':
        return activate_theme(args.theme, args.config)
    else:
        parser.print_help()
        return 0

if __name__ == '__main__':
    sys.exit(main())
