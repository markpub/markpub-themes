#!/usr/bin/env python3

# setup logging
import logging, os
log_level = os.environ.get('LOGLEVEL', 'WARNING').upper()

logging.basicConfig(
    level=getattr(logging, log_level, 'WARNING'),
    format="%(asctime)s - %(name)s - %(levelname)s: %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger('markpub-themes')

import argparse
from pathlib import Path
import shutil
import sys
import yaml
from . import get_theme_path, list_themes, __version__

def clone_theme(theme_name, destination):
    """Clone a theme to a destination directory."""
    try:
        source = Path(get_theme_path(theme_name))
        dest = Path(destination).expanduser().resolve()

        if dest.exists():
            logger.error(f"Error: Destination '{dest}' already exists", file=sys.stderr)
            return 1

        shutil.copytree(source, dest)
        logger.info(f"Theme '{theme_name}' cloned to {dest}")
        return 0
    except ValueError as e:
        logger.error(f"Error: {e}", file=sys.stderr)
        print(f"Available themes: {', '.join(sorted(list_themes()))}")
        return 1
    except Exception as e:
        logger.error(f"Error cloning theme: {e}", file=sys.stderr)
        return 1

def activate_theme(theme_name, config_file=None):
    """Activate a theme (sets it as the active theme)."""
    try:
        # Verify theme exists
        theme_path = get_theme_path(theme_name)

        if Path(config_file).exists():
            config_path = Path(config_file).expanduser().resolve()
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file,'r',encoding='utf-8') as f:
                config_doc = yaml.safe_load(f)
                config_doc['theme'] = theme_name
            with open(config_file,'w', encoding='utf-8') as f:
                yaml.safe_dump(config_doc, f, default_flow_style=False, sort_keys=False)
            print(f"Theme '{theme_name}' activated in {config_path}")
        else:
            logger.error(f"{config_file} not found; activation canceled.")

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
    # expected destination and config values
    markpub_dir = '.'
    destination = f"{markpub_dir}/themes"
    config_file = f"{markpub_dir}/markpub.yaml"
    
    parser = argparse.ArgumentParser(
        prog='markpub-themes',
        description='Manage markpub themes'
    )
    parser.add_argument('--version', '-V', action='version', version=f'%(prog)s {__version__}')
#    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    subparsers = parser.add_subparsers(required=True)
    # subparser for "list" command
    list_parser = subparsers.add_parser('list', help='List available themes')
    list_parser.set_defaults(cmd='list')
    # subparser for "clone" command
    clone_parser = subparsers.add_parser('clone', help='Install a theme in ./markpub/themes directory')
    clone_parser.add_argument('theme', help='Name of the theme to clone')
    clone_parser.set_defaults(cmd='clone')
    # subparser for "activate" command
    activate_parser = subparsers.add_parser('activate', help='Activate a theme')
    activate_parser.add_argument('theme', help='Name of the theme to activate')
    activate_parser.set_defaults(cmd='activate')

    args = parser.parse_args()
    logger.info(args)

    match args[0].cmd:
        case 'list':
            themes = list_themes()
            print("Available themes:")
            for theme in themes:
                print(f"  - {theme}")
        case 'clone':
        # clone will install theme in local directory and activate
        # show term-menu theme list
            return clone_theme(args.theme, destination)
        case 'activate':
        # activate updates configuration file
            return activate_theme(args.theme, config_file)
        case _:
            parser.print_help()
            return

if __name__ == '__main__':
    sys.exit(main())
