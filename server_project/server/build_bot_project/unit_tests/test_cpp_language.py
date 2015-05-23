import os
import unittest

import pytest

from common.cmd_utils import find_tool, shell, split_lines, screen_str
from build_bot_project.languages.cpp_language import CPPLanguage


test_name = __name__


@pytest.mark.usefixtures("test_build_directory_fixture", "test_config_fixture")
class CPPLanguageTests(unittest.TestCase):
    def setUp(self):
        self.cpp_language_without_config = CPPLanguage()
        self.test_file_name = "cpp_basic"
        self.test_src_name = self.test_file_name + ".cpp"
        self.test_exe_name = self.test_file_name + ".exe"

        self.test_src_file_path = os.path.join(self.src_code_dir, self.test_src_name)
        self.test_exe_file_path = os.path.join(self.build_dir_bin, self.test_exe_name)

    def test_are_all_fixture_attributes_set(self):
        assert hasattr(self, "build_dir")
        assert hasattr(self, "build_dir_bin")
        assert hasattr(self, "src_code_dir")
        assert hasattr(self, "config_parser")
        assert hasattr(self, "is_config_read_ok")
        assert hasattr(self, "cpp_compiler_path")
        assert hasattr(self, "vc_bat_path")

    def test_can_find_build_dir_bin(self):
        self.assertTrue(os.path.exists(self.build_dir_bin))

    def test_can_find_test_src_file(self):
        self.assertTrue(os.path.exists(self.test_src_file_path))

    def test_can_create_cpp_language_without_config(self):
        self.assertIsNotNone(self.cpp_language_without_config)

    def test_can_get_default_cpp_compiler_path(self):
        self.assertEquals(self.cpp_language_without_config.get_compiler_path(), CPPLanguage.DEFAULT_COMPILER_PATH)

    def test_can_get_default_vc_bat_path(self):
        self.assertEquals(self.cpp_language_without_config.vc_bat_path, CPPLanguage.DEFAULT_VC_BAT_PATH)

    def test_is_default_compiler_path_exists(self):
        self.assertTrue(os.path.exists(self.cpp_compiler_path))

    def test_is_default_vc_bat_path_exists(self):
        self.assertTrue(os.path.exists(self.vc_bat_path))

    def test_can_set_env_from_bat(self):
        self.assertIsNotNone(os.getenv("INCLUDE"))
        self.assertIsNotNone(os.getenv("LIB"))

    def test_can_find_cl(self):
        cpp_language_with_config = CPPLanguage(self.config_parser)
        (is_found, path) = find_tool("cl")
        self.assertTrue(is_found)
        self.assertEquals(path.pop(0), cpp_language_with_config.compiler_path)

    def test_can_successfully_call_cl_only(self):
        cpp_language_with_config = CPPLanguage(self.config_parser)
        (ret_code, out, err) = shell(cpp_language_with_config.compiler_path)
        self.assertEquals(ret_code, 0)

    def test_can_successfully_call_cl_to_compile_test_file(self):
        cpp_language_with_config = CPPLanguage(self.config_parser)
        (ret_code, out, err) = self._compile(cpp_language_with_config)
        self.assertEquals(ret_code, 0)
        self.assertTrue(os.path.exists(self.test_exe_file_path))

    def test_can_successfully_compile_and_run_test_file(self):
        cpp_language_with_config = CPPLanguage(self.config_parser)
        self._compile(cpp_language_with_config)
        (ret_code, out, err) = shell(self.test_exe_file_path)
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(0), "This is a native C++ program.")

    def test_can_successfully_compile_and_run_test_file_with_config(self):
        cpp_language_with_config = CPPLanguage(self.config_parser)
        self._compile(cpp_language_with_config)
        (ret_code, out, err) = shell(self.test_exe_file_path)
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(0), "This is a native C++ program.")

    def _compile(self, language):
        compile_cmd = screen_str(language.compiler_path) + " " + self.test_src_file_path \
                      + " /Fo" + self.build_dir + os.sep + " /Fe" + self.test_exe_file_path
        return shell(compile_cmd)