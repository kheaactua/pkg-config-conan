#!/usr/bin/env python
# -*- coding: future_fstrings -*-
# -*- coding: utf-8 -*-

import os, re, sys, platform
from conans import ConanFile, tools, AutoToolsBuildEnvironment
from glob import glob


class PkgConfigConan(ConanFile):
    name        = 'pkg-config'
    version     = '0.29.2'
    license     = 'MIT'
    url         = 'https://github.com/kheaactua/pkg-config-conan'
    description = 'This is a tooling package for pkg-config'
    settings    = 'os', 'compiler', 'build_type', 'arch'

    settings = {
        'os_build':   ['Windows', 'Linux', 'Macos'],
        'arch_build': ['x86', 'x86_64', 'armv7'],
    }

    def source(self):
        tarball_url = f'https://pkgconfig.freedesktop.org/releases/pkg-config-{self.version}.tar.gz'
        tgz = tarball_url.split('/')[-1]
        tools.download(tarball_url, tgz)
        tools.untargz(tgz)
        os.unlink(tgz)

    def build(self):
        dirs = glob('pkg-config-*')
        if not len(dirs):
            self.output.error('Could not find pkg-config-* directory')
            sys.exit(-1)
        else:
            dirname = dirs[0]

        autotools = AutoToolsBuildEnvironment(self, win_bash=('Windows' == platform.system()))

        # When installed with mingw, the configure needs a bash path.
        def tweakPath(path):
            if 'Windows' == platform.system():
                path = re.sub(r'\\', r'/', path.lower())
                path = re.sub(r'c:/', r'/c/', path)
            return path


        with tools.chdir(dirname):
            args = []
            args.append('--with-internal-glib')
            args.append('--prefix=%s'%tweakPath(self.package_folder))
            autotools.configure(args=args)
            autotools.make()
            autotools.make(args=['install'])

    def package(self):
        pass

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
        self.env_info.path.append(os.path.join(self.package_folder, 'share/aclocal'))

        # This package results in erasing the default pkg-config, so attempt to
        # add it back.  That said, when pkg-config is used as a build
        # requirement, it's touch up's to the environment appear to be ignored.
        def filter_nonexistant(paths):
            outp = []
            for p in paths:
                if os.path.exists(p): outp.append(p)
            return outp

        if tools.os_info.is_linux:
            if 'x86_64' == self.settings.arch_build:
                self.env_info.PKG_CONFIG_PATH = os.environ.get('PKG_CONFIG_PATH', filter_nonexistant(['/usr/local/lib/x86_64-linux-gnu/pkgconfig', '/usr/local/lib/pkgconfig', '/usr/local/share/pkgconfig', '/usr/lib/x86_64-linux-gnu/pkgconfig', '/usr/lib/pkgconfig', '/usr/share/pkgconfig']))
            else:
                self.env_info.PKG_CONFIG_PATH = os.environ.get('PKG_CONFIG_PATH', filter_nonexistant(['/usr/local/lib/i386-linux-gnu/pkgconfig', '/usr/local/lib/pkgconfig', '/usr/local/share/pkgconfig', '/usr/lib/i386-linux-gnu/pkgconfig', '/usr/lib/pkgconfig', '/usr/share/pkgconfig']))

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
