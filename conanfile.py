#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class LiblxiConan(ConanFile):
    name = "liblxi"
    version = "1.13"
    homepage = "https://github.com/lxi-tools/liblxi.git"
    description = "C library communicating with LXI compatible instruments."
    url = "https://github.com/lxi-tools/liblxi.git"
    author = "Martin Lund <martin.lund@keep-it-simple.com>"
    license = "COPYING"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [
        True, False], "avahi": [True, False]}
    default_options = "shared=True", "fPIC=True", "avahi=False"
    checksum = "5c2a97b1d098ac49f6c01c918298db8b3f7af505e463b4d3d8952aff447e9ac2"

    _autotools = None

    @property
    def _source_subfolder(self):
        return "{name}-v{version}".format(name=self.name, version=self.version)

    def system_requirements(self):
        packages = []
        if tools.os_info.linux_distro == "ubuntu":
            packages.append("autogen")
            packages.append("autoconf")
            packages.append("automake")
            packages.append("libtool")

            if self.options.avahi:
                packages.append("libavahi-client-dev")

            packages.append("libxml2-dev")
            packages.append("libtirpc-dev")

        for pkg in packages:
            installer = tools.SystemPackageTool()
            installer.install(pkg)

    def source(self):
        targz_name = "{name}-v{version}.tar.gz".format(name=self.name,
                                                       version=self.version)
        tools.download("https://github.com/lxi-tools/liblxi/archive/v{version}.tar.gz".format(
            version=self.version), targz_name)
        tools.check_sha256(targz_name, self.checksum)
        tools.untargz(
            targz_name, destination=self._source_subfolder, strip_root=True)
        os.unlink(targz_name)

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools

        args = []
        if self.options.shared:
            args.append("--enable-shared")
            args.append("--disable-static")
        else:
            args.append("--disable-shared")
            args.append("--enable-static")

        if not self.options.avahi:
            args.append("--disable-avahi")

        with tools.chdir(self._source_subfolder):
            self.run("autoreconf --force --install")

            self._autotools = AutoToolsBuildEnvironment(self)
            self._autotools.fpic = self.options.fPIC
            self._autotools.configure(args=args)

        return self._autotools

    def build(self):

        autotools = self._configure_autotools()

        with tools.chdir(self._source_subfolder):
            autotools.make()

    def package(self):
        autotools = self._configure_autotools()
        
        with tools.chdir(self._source_subfolder):
            autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
