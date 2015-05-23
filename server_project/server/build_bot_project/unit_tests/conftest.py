from build_bot_project.languages.cpp_language import CPPLanguage
from build_bot_project.languages.cs_language import CSLanguage
from build_bot_project.languages.fp_language import FPLanguage

import ConfigParser

import os
import shutil
import pytest

@pytest.fixture(scope="class")
def test_build_directory_fixture(request):
    request.cls.test_name = getattr(request.module, "test_name", "default_module")

    project_path = os.path.dirname(os.path.dirname(__file__))
    request.cls.build_dir = os.path.join(os.path.join(project_path, "_build"), request.cls.test_name)

    if os.path.exists(request.cls.build_dir):
        shutil.rmtree(request.cls.build_dir)

    request.cls.build_dir_bin = os.path.join(request.cls.build_dir, "bin")
    if not os.path.exists(request.cls.build_dir_bin):
        os.makedirs(request.cls.build_dir_bin)

    request.cls.src_code_dir = os.path.join(project_path, "code_to_compile")


@pytest.fixture(scope="class")
def test_config_fixture(request, test_build_directory_fixture):
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    config_file_path = os.path.join(project_path, "config.cfg")

    request.cls.config_parser = ConfigParser.ConfigParser()

    request.cls.is_config_read_ok = request.cls.config_parser.read(config_file_path)

    cpp_compiler_dir = request.cls.config_parser.get('compiler_paths', 'cpp_path')
    request.cls.cpp_compiler_path = os.path.join(cpp_compiler_dir, CPPLanguage.COMPILER_FILE)
    request.cls.vc_bat_path = os.path.join(os.path.dirname(cpp_compiler_dir), CPPLanguage.VC_BAT_FILE)

    cs_compiler_dir = request.cls.config_parser.get('compiler_paths', 'cs_path')
    request.cls.cs_compiler_path = os.path.join(cs_compiler_dir, CSLanguage.COMPILER_FILE)

    fp_compiler_dir = request.cls.config_parser.get('compiler_paths', 'fp_path')
    request.cls.fp_compiler_path = os.path.join(fp_compiler_dir, FPLanguage.COMPILER_FILE)


