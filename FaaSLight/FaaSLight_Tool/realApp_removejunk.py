import sys
sys.setrecursionlimit(5000000)
import removefile

print("Remove Junk Files")

assetsDir = {
    'ignorDir': [
        '__pycache__', 'tests', '.serverless',
        'pip', 'pkg_resources', 'setuptools', 'wheel'
    ],
    'ignorSpeDir': ['.dist-info'],
    'ignorFile': ['.pyc', '.pyi', '.pth', '.md'],
}

removefile.delFiles('realApp', assetsDir)

print("Complete Remove Junk File")
