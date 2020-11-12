import sys
import tempfile
from collections import defaultdict
from datetime import date
from distutils.ccompiler import CCompiler
from distutils.errors import CompileError
from glob import glob
from pathlib import Path

import pybind11
from setuptools import (Extension,
                        find_packages,
                        setup)
from setuptools.command.build_ext import build_ext

import voronoi


def has_flag(compiler: CCompiler, name: str) -> bool:
    """Detects whether a flag name is supported on the specified compiler."""
    with tempfile.NamedTemporaryFile('w',
                                     suffix='.cpp') as file:
        file.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([file.name],
                             extra_postargs=[name])
        except CompileError:
            return False
    return True


def cpp_flag(compiler: CCompiler) -> str:
    """
    Returns the -std=c++[11|...] compiler flag.
    The newer version is preferred when available.
    """
    flags = ['-std=c++{}'.format(str(year)[2:])
             for year in range(2011, date.today().year + 1, 3)]
    for flag in reversed(flags):
        if has_flag(compiler, flag):
            return flag
    raise RuntimeError('Unsupported compiler: '
                       'at least C++11 support is needed.')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    compile_args = defaultdict(list, {'msvc': ['/EHsc'], 'unix': []})
    link_args = defaultdict(list, {'msvc': [], 'unix': []})

    if sys.platform == 'darwin':
        darwin_args = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        compile_args['unix'] += darwin_args
        link_args['unix'] += darwin_args

    def build_extensions(self) -> None:
        compiler_type = self.compiler.compiler_type
        compile_args = self.compile_args[compiler_type]
        link_args = self.link_args[compiler_type]
        if compiler_type == 'unix':
            compile_args.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                compile_args.append('-fvisibility=hidden')
        define_macros = [('VERSION_INFO', self.distribution.get_version())]
        for extension in self.extensions:
            extension.extra_compile_args = compile_args
            extension.extra_link_args = link_args
            extension.define_macros = define_macros
        super().build_extensions()


project_base_url = 'https://github.com/lycantropos/voronoi/'

setup(name=voronoi.__name__,
      packages=find_packages(exclude=('tests', 'tests.*')),
      version=voronoi.__version__,
      description=voronoi.__doc__,
      long_description=Path('README.md').read_text(encoding='utf-8'),
      long_description_content_type='text/markdown',
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: Implementation :: CPython',
      ],
      license='MIT License',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.zip',
      python_requires='>=3.5',
      install_requires=Path('requirements.txt').read_text(),
      cmdclass={'build_ext': BuildExt},
      ext_modules=[Extension('_' + voronoi.__name__,
                             glob('src/*.cpp'),
                             include_dirs=[pybind11.get_include(),
                                           pybind11.get_include(True),
                                           Path.cwd() / 'include'],
                             language='c++')],
      zip_safe=False)
