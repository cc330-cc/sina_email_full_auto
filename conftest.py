import sys
from pathlib import Path

# 将项目根目录添加到 Python 模块搜索路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))