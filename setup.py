from distutils.core import setup

setup(
    name="i3-workspace-rename",
    version="0.1.1",
    description='dynamic workspace rename tool.',
    author="Mk Safavi",
    author_email="mksafavi@gmail.com",
    py_modules=['main', 'workspace_rename'],
    install_requires=["i3ipc"],
    entry_points={
          'console_scripts': [
              'i3-workspace-rename=main:main'
          ]
      }
)
