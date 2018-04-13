from io import StringIO
from conans import ConanFile, tools, AutoToolsBuildEnvironment

class PkgConfigTestConan(ConanFile):
    build_requires = ('pkg-config/0.29.2@ntc/stable')

    def build(self):
        pass

    def test(self):
        output = StringIO()
        self.run('pkg-config --version', output=output)
        ver = str(output.getvalue()).strip()
        self.output.info(f'Installed: "{ver}"')

        assert ver == '0.29.2', 'Version mismatch'

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
