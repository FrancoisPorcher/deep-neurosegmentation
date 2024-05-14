import os
from pathlib import Path
import configparser

def create_config_file(repo_path, config_filename='config.ini'):
    config = configparser.ConfigParser()

    # Create a section for directories in the config
    config['DIRECTORIES'] = {}

    # Navigate the directory structure
    repo = Path(repo_path).resolve()  # Ensure the base path is absolute
    # Limit to 2 levels deep (root level and one level down)
    for path in repo.iterdir():  # First level
        if path.is_dir():
            # Use resolve() to get the absolute path
            config['DIRECTORIES'][path.name] = str(path.resolve())
            # Second level
            for subpath in path.iterdir():
                if subpath.is_dir():
                    # Use resolve() to get the absolute path
                    config['DIRECTORIES'][subpath.name] = str(subpath.resolve())
                    # Special condition for `data/processed`
                    if str(subpath).endswith('data/processed'):  # Adjust the path string as necessary
                        # Go two more levels deep
                        for third_level in subpath.iterdir():
                            if third_level.is_dir():
                                config['DIRECTORIES'][third_level.name] = str(third_level.resolve())
                                for fourth_level in third_level.iterdir():
                                    if fourth_level.is_dir():
                                        config['DIRECTORIES'][fourth_level.name] = str(fourth_level.resolve())

    # Write the directory paths to a config file
    with open(config_filename, 'w') as configfile:
        config.write(configfile)

    print(f'Config file created at {config_filename}')

# Example usage: run this from the root of your repository
if __name__ == "__main__":
    create_config_file('.')
