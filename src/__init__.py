

import os

import sys

path = os.path.abspath(os.path.join(__file__, '..', '..'))

if path not in sys.path:
    sys.path.append(path)

path = os.path.abspath(os.path.join(__file__, '..'))

if path not in sys.path:
    sys.path.append(path)


sys.path.insert(0, '..')
sys.path.insert(0, '.')

sys.path.append('/project')
sys.path.append('/project/src')
sys.path.append('.src.utils')
sys.path.append('utils.cors')
sys.path.append('.src.utils.cors')
sys.path.append('.src')
sys.path.append('./src')
sys.path.append('./src/utils')
sys.path.append('./utils')

sys.path.append('../src')
sys.path.append('..src')
sys.path.append('.src')
sys.path.append('.utils')

print(sys.path)
print(os.getcwd())

print(sys.executable)