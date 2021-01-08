import os

from conans import ConanFile, CMake, tools, RunEnvironment


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {"shared": [True, False], "fPIC": [True, False], "withzlib": [True, False]}
    default_options = "shared=False", "fPIC=True", "withzlib=True"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            self.run(os.path.join("bin", "libtar-test-package"))
