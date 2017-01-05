from __future__ import print_function
from conans import ConanFile, CMake, tools
from glob import glob
from time import sleep

import os
import subprocess

class PkgConfigConan(ConanFile):
    name = 'pkg-config'
    version = '0.29.1'
    license = 'MIT'
    url = 'https://github.com/sztomi/pkg-config-conan'
    description = 'This is a tooling package for pkg-config'
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'cmake', 'virtualenv'

    def source(self):
        tarball_url = 'https://pkgconfig.freedesktop.org/releases/pkg-config-{}.tar.gz'.format(self.version)
        tgz = tarball_url.split('/')[-1]
        tools.download(tarball_url, tgz)
        tools.untargz(tgz)
        os.unlink(tgz)

    def build(self):
        self.dirname = glob('pkg-config-*')[0]
        os.chdir(self.dirname)        
        def run_in_env(cmd):
            activate = '. ../activate.sh &&'
            self.run(activate + cmd)
        run_in_env('./configure --with-internal-glib --prefix={}'.format(self.package_folder))
        self.run('make')
        self.run('make install')

    def package(self):
        pass

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
        self.env_info.path.append(os.path.join(self.package_folder, 'share/aclocal'))
        
