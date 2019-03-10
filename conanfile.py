#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class DcmtkConan(ConanFile):
    name = "dcmtk"
    version = "3.6.4"
    # TODO
    description = "Keep it short"
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("conan", "dcmtk", "DICOM")
    url = "https://github.com/bincrafters/conan-dcmtk"
    homepage = "https://github.com/DCMTK/dcmtk"
    author = "Bincrafters <bincrafters@gmail.com>"
    # TODO: this is the license of dcmtk? if so: BSD-3-Clause
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]      # Packages the license for the conanfile.py
    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"

    modules = [
        "ofstd", "oflog", "dcmdata", "dcmimgle", "dcmimage", "dcmjpeg", "dcmjpls", "dcmtls",
        "dcmnet", "dcmsr", "dcmsign", "dcmwlm", "dcmqrdb", "dcmpstat", "dcmrt", "dcmiod", "dcmfg",
        "dcmseg", "dcmtract", "dcmpmap"
    ]

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_apps": [True, False],
        "enable_private_tags": [True, False],
        "with_threads": [True, False],
        "with_doxygen": [True, False],
        "with_wide_char_io": [True, False],
        "with_wide_char_main": [True, False],
        "enable_stl": [True, False],
        "enable_builtin_dictionary": [True, False],
        "enable_external_dictionary": [True, False],
        "with_libxml": [True, False],
        "with_libpng": [True, False],
        "with_libtiff": [True, False],
        "with_openssl": [True, False],
        "with_zlib": [True, False],
        "with_libiconv": [True, False],
    }

    default_options = {
        "shared": False,
        "fPIC": True,
        "build_apps": False,
        "enable_private_tags": False,
        "with_threads": True,
        "with_doxygen": False,
        "with_wide_char_io": True,
        "with_wide_char_main": True,
        "enable_stl": True,
        "enable_builtin_dictionary": True,
        "enable_external_dictionary": True,
        "with_libxml": True,
        "with_libpng": True,
        "with_libtiff": True,
        "with_openssl": True,
        "with_zlib": True,
        "with_libiconv": True,
    }

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def requirements(self):
        if self.options.with_libxml:
            self.requires("libxml2/2.9.9@bincrafters/stable")
        if self.options.with_libpng:
            self.requires("libpng/1.6.36@bincrafters/stable")
        if self.options.with_libtiff:
            self.requires("libtiff/4.0.9@bincrafters/stable")
        if self.options.with_openssl:
            self.requires("OpenSSL/1.1.1b@conan/stable")
        if self.options.with_zlib:
            self.requires("zlib/1.2.11@conan/stable")
        if self.options.with_libiconv:
            self.requires("libiconv/1.15@bincrafters/stable")

    def source(self):
        source_url = "https://github.com/DCMTK/dcmtk"
        tools.get("{0}/archive/DCMTK-{1}.tar.gz".format(source_url, self.version), sha256="e4b1de804a3fef38fe8cb9edd00262c3cbbd114b305511c14479dd888a9337d2")
        extracted_dir = self.name + "-DCMTK-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def get_cmake_3rd_party(self):
        return "{}/CMake/3rdParty.cmake".format(self._source_subfolder)

    def patch_libxml(self):
        tools.replace_in_file(
            self.get_cmake_3rd_party(),
            'set(LIBXML_LIBS debug "${LIBXML_LIBDIR}/libxml2_d.lib" optimized "${LIBXML_LIBDIR}/libxml2_o.lib" debug "${LIBXML_LIBDIR}/iconv_d.lib" optimized "${LIBXML_LIBDIR}/iconv_o.lib")',
            'set(LIBXML_LIBS {})'.format(" ".join(self.deps_cpp_info["libxml2"].libs)))

    def patch_libpng(self):
        tools.replace_in_file(
            self.get_cmake_3rd_party(),
            'set(LIBPNG_LIBS debug "${LIBPNG_LIBDIR}/libpng_d.lib" optimized "${LIBPNG_LIBDIR}/libpng_o.lib")',
            'set(LIBPNG_LIBS {})'.format(" ".join(self.deps_cpp_info["libpng"].libs)))

    def patch_libtiff(self):
        tools.replace_in_file(
            self.get_cmake_3rd_party(),
            'set(LIBTIFF_LIBS debug "${LIBTIFF_LIBDIR}/libtiff_d.lib" optimized "${LIBTIFF_LIBDIR}/libtiff_o.lib")',
            'set(LIBTIFF_LIBS {})'.format(" ".join(self.deps_cpp_info["libtiff"].libs)))

    def patch_openssl(self):
        tools.replace_in_file(
            self.get_cmake_3rd_party(),
            'set(OPENSSL_LIBS "crypt32" debug "${OPENSSL_LIBDIR}/dcmtkssl_d.lib" optimized "${OPENSSL_LIBDIR}/dcmtkssl_o.lib" debug "${OPENSSL_LIBDIR}/dcmtkcrypto_d.lib" optimized "${OPENSSL_LIBDIR}/dcmtkcrypto_o.lib")',
            'set(OPENSSL_LIBS {})'.format(" ".join(self.deps_cpp_info["OpenSSL"].libs)))

    def patch_zlib(self):
        tools.replace_in_file(
            self.get_cmake_3rd_party(),
            'set(LIBICONV_LIBS debug "${LIBICONV_LIBDIR}/libiconv_d.lib" optimized "${LIBICONV_LIBDIR}/libiconv_o.lib")',
            'set(LIBICONV_LIBS {})'.format(" ".join(self.deps_cpp_info["libiconv"].libs)))

    def patch_libiconv(self):
        tools.replace_in_file(
            self.get_cmake_3rd_party(),
            'set(ZLIB_LIBS debug "${ZLIB_LIBDIR}/zlib_d.lib" optimized "${ZLIB_LIBDIR}/zlib_o.lib")',
            'set(ZLIB_LIBS {})'.format(" ".join(self.deps_cpp_info["zlib"].libs)))

    def patch_dcmtk(self):
        if self.options.with_libxml:
            self.patch_libxml()
        if self.options.with_libpng:
            self.patch_libpng()
        if self.options.with_libtiff:
            self.patch_libtiff()
        if self.options.with_openssl:
            self.patch_openssl()
        if self.options.with_zlib:
            self.patch_zlib()
        if self.options.with_libiconv:
            self.patch_libiconv()

    def _configure_cmake(self):
        cmake = CMake(self)

        if self.settings.compiler == "Visual Studio":
            cmake.definitions["DCMTK_OVERWRITE_WIN32_COMPILER_FLAGS"] = "ON" if self.settings.compiler.runtime == "MT" else "OFF"

        cmake.definitions["BUILD_APPS"] = "ON" if self.options["build_apps"] else "OFF"
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options["shared"] else "OFF"
        # TODO: BUILD_SINGLE_SHARED_LIBRARY?
        cmake.definitions["DCMTK_WITH_TIFF"] = "ON" if self.options["with_libtiff"] else "OFF"
        cmake.definitions["DCMTK_WITH_PNG"] = "ON" if self.options["with_libpng"] else "OFF"
        cmake.definitions["DCMTK_WITH_XML"] = "ON" if self.options["with_libxml"] else "OFF"
        cmake.definitions["DCMTK_WITH_ZLIB"] = "ON" if self.options["with_zlib"] else "OFF"
        cmake.definitions["DCMTK_WITH_OPENSSL"] = "ON" if self.options["with_openssl"] else "OFF"
        # TODO: DCMTK_WITH_SNDFILE?
        cmake.definitions["DCMTK_WITH_ICONV"] = "ON" if self.options["with_libiconv"] else "OFF"
        # TODO: DCMTK_WITH_ICU?
        # TODO: DCMTK_WITH_WRAP?
        # TODO: DCMTK_WITH_OPENJPEG?
        cmake.definitions["DCMTK_ENABLE_PRIVATE_TAGS"] = "ON" if self.options["enable_private_tags"] else "OFF"
        cmake.definitions["DCMTK_WITH_THREADS"] = "ON" if self.options["with_threads"] else "OFF"
        cmake.definitions["DCMTK_WITH_DOXYGEN"] = "ON" if self.options["with_doxygen"] else "OFF"
        # TODO: DCMTK_GENERATE_DOXYGEN_TAGFILE?
        cmake.definitions["DCMTK_WIDE_CHAR_FILE_IO_FUNCTIONS"] = "ON" if self.options["with_wide_char_io"] else "OFF"
        cmake.definitions["DCMTK_WIDE_CHAR_MAIN_FUNCTION"] = "ON" if self.options["with_wide_char_main"] else "OFF"
        cmake.definitions["DCMTK_ENABLE_STL"] = "ON" if self.options["enable_stl"] else "OFF"
        cmake.definitions["DCMTK_ENABLE_BUILTIN_DICTIONARY"] = "ON" if self.options["enable_builtin_dictionary"] else "OFF"
        cmake.definitions["DCMTK_ENABLE_EXTERNAL_DICTIONARY"] = "ON" if self.options["enable_external_dictionary"] else "OFF"

        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        self.patch_dcmtk()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        # TODO: self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
