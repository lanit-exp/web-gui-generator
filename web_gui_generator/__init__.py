from os.path import dirname, abspath
from pathlib import Path
import fileproc as fp

SRC_ROOT_DIR: Path = Path(dirname(abspath(__file__)))
PROJ_ROOT_DIR: Path = Path(SRC_ROOT_DIR).parent
TREES_PATH: Path = PROJ_ROOT_DIR / "resources/gen_trees"
CONF_PATH: Path = PROJ_ROOT_DIR / "resources/conf"
#DESCR = fp.Reader.read_descriptions(CONF_PATH)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
