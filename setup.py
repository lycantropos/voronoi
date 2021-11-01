import platform
from pathlib import Path

from setuptools import (find_packages,
                        setup)

import voronoi

project_base_url = 'https://github.com/lycantropos/voronoi/'


def read_file(path_string: str) -> str:
    return Path(path_string).read_text(encoding='utf-8')


parameters = dict(
        name=voronoi.__name__,
        packages=find_packages(exclude=('tests', 'tests.*')),
        version=voronoi.__version__,
        description=voronoi.__doc__,
        long_description=read_file('README.md'),
        long_description_content_type='text/markdown',
        author='Azat Ibrakov',
        author_email='azatibrakov@gmail.com',
        license='MIT License',
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
        ],
        url=project_base_url,
        download_url=project_base_url + 'archive/master.zip',
        python_requires='>=3.5',
        setup_requires=read_file('requirements-setup.txt'),
        install_requires=read_file('requirements.txt'))
if platform.python_implementation() == 'CPython':
    import sys
    import tempfile
    from collections import defaultdict
    from datetime import date
    from distutils.ccompiler import CCompiler
    from distutils.errors import CompileError
    from glob import glob
    from typing import (Any,
                        Iterable)

    from setuptools import (Command,
                            Extension)
    from setuptools.command.build_ext import build_ext
    from setuptools.command.develop import develop


    def is_flag_supported(flag: str, compiler: CCompiler) -> bool:
        with tempfile.NamedTemporaryFile('w',
                                         suffix='.cpp') as file:
            file.write('int main(void) { return 0; }')
            try:
                compiler.compile([file.name],
                                 extra_postargs=[flag])
            except CompileError:
                return False
        return True


    def to_first_supported_flag(flags: Iterable[str],
                                compiler: CCompiler) -> str:
        flags = list(flags)
        try:
            return next(flag
                        for flag in flags
                        if is_flag_supported(flag, compiler))
        except StopIteration:
            quote = '"{}"'.format
            raise CompileError('None of {flags} flags are supported '
                               'by {compiler} compiler.'
                               .format(flags=', '.join(map(quote, flags)),
                                       compiler=quote(compiler.compiler_type)))


    def year_to_standard(year: int) -> str:
        return 'c++{}'.format(str(year)[2:])


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
            cpp_standards = [
                year_to_standard(year)
                for year in reversed(range(2017, date.today().year + 1, 3))]
            if compiler_type == 'unix':
                compile_args.append(
                        to_first_supported_flag(
                                ['-std={}'.format(standard)
                                 for standard in cpp_standards],
                                self.compiler))
                if is_flag_supported('-fvisibility=hidden', self.compiler):
                    compile_args.append('-fvisibility=hidden')
            elif compiler_type == 'msvc':
                try:
                    standard_flag = to_first_supported_flag(
                            ['/std:{}'.format(standard)
                             for standard in cpp_standards],
                            self.compiler)
                except CompileError:
                    compile_args.append('/std:c++latest')
                else:
                    compile_args.append(standard_flag)
            define_macros = [('VERSION_INFO', self.distribution.get_version())]
            for extension in self.extensions:
                extension.extra_compile_args += compile_args
                extension.extra_link_args += link_args
                extension.define_macros += define_macros
            super().build_extensions()


    class Develop(develop):
        def reinitialize_command(self,
                                 name: str,
                                 reinit_subcommands: int = 0,
                                 **kwargs: Any) -> Command:
            if name == build_ext.__name__:
                kwargs.setdefault('debug', 1)
            result = super().reinitialize_command(name, reinit_subcommands,
                                                  **kwargs)
            if name == build_ext.__name__:
                result.ensure_finalized()
                for extension in result.extensions:
                    extension.undef_macros.append('NDEBUG')
            return result


    class LazyPybindInclude:
        def __str__(self) -> str:
            import pybind11
            return pybind11.get_include()


    project_root = Path(__file__).parent
    parameters.update(
            cmdclass={build_ext.__name__: BuildExt,
                      develop.__name__: Develop},
            ext_modules=[Extension('_' + voronoi.__name__,
                                   glob('src/*.cpp'),
                                   include_dirs=[LazyPybindInclude(),
                                                 project_root / 'include'],
                                   language='c++')],
            zip_safe=False)
setup(**parameters)
