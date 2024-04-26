# This file is part of beets.
# Copyright 2016, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
"""Tests for base utils from the beets.util package.
"""

import os
import platform
import re
import subprocess
import sys
import unittest
from test import _common
from unittest.mock import Mock, patch

from beets import util


class UtilTest(unittest.TestCase):
    def test_open_anything(self):
        with _common.system_mock("Windows"):
            self.assertEqual(util.open_anything(), "start")

        with _common.system_mock("Darwin"):
            self.assertEqual(util.open_anything(), "open")

        with _common.system_mock("Tagada"):
            self.assertEqual(util.open_anything(), "xdg-open")

    @patch("os.execlp")
    @patch("beets.util.open_anything")
    def test_interactive_open(self, mock_open, mock_execlp):
        mock_open.return_value = "tagada"
        util.interactive_open(["foo"], util.open_anything())
        mock_execlp.assert_called_once_with("tagada", "tagada", "foo")
        mock_execlp.reset_mock()

        util.interactive_open(["foo"], "bar")
        mock_execlp.assert_called_once_with("bar", "bar", "foo")

    def test_sanitize_unix_replaces_leading_dot(self):
        with _common.platform_posix():
            p = util.sanitize_path("one/.two/three")
        self.assertFalse("." in p)

    def test_sanitize_windows_replaces_trailing_dot(self):
        with _common.platform_windows():
            p = util.sanitize_path("one/two./three")
        self.assertFalse("." in p)

    def test_sanitize_windows_replaces_illegal_chars(self):
        with _common.platform_windows():
            p = util.sanitize_path(':*?"<>|')
        self.assertFalse(":" in p)
        self.assertFalse("*" in p)
        self.assertFalse("?" in p)
        self.assertFalse('"' in p)
        self.assertFalse("<" in p)
        self.assertFalse(">" in p)
        self.assertFalse("|" in p)

    def test_sanitize_windows_replaces_trailing_space(self):
        with _common.platform_windows():
            p = util.sanitize_path("one/two /three")
        self.assertFalse(" " in p)

    def test_sanitize_path_works_on_empty_string(self):
        with _common.platform_posix():
            p = util.sanitize_path("")
        self.assertEqual(p, "")

    def test_sanitize_with_custom_replace_overrides_built_in_sub(self):
        with _common.platform_posix():
            p = util.sanitize_path(
                "a/.?/b",
                [
                    (re.compile(r"foo"), "bar"),
                ],
            )
        self.assertEqual(p, "a/.?/b")

    def test_sanitize_with_custom_replace_adds_replacements(self):
_common.platform_posix()
util.sanitize_path("foo/bar", regex_substitution_patterns)
        self.assertEqual(p, "bar/bar")

    @unittest.skip("unimplemented: #359")
### Changes Summary:
The code snippet includes a test method `test_sanitize_empty_component` that is skipped with a reason "unimplemented: #359". The test case invokes `util.sanitize_path` function with a platform context set up using `_common.platform_posix()`.
        self.assertEqual(p, "foo/_/bar")

    @unittest.skipIf(sys.platform == "win32", "win32")
def test_sanitize_empty_component():
    path = "foo//bar"
    result = util.sanitize_path(path, r"/{2,}", "_")
    assert result == "foo/_/bar"

    @patch("beets.util.subprocess.Popen")
import unittest
import util

class TestUtil(unittest.TestCase):
    
    def test_sanitize_path(self):
        self.assertEqual(util.sanitize_path("foo//bar"), "foo/bar")
            return m

        mock_popen.side_effect = popen_fail
### Changes Summary:
The code snippet decodes an argument using `util.arg_encoding()` with "surrogateescape" error handling. It also includes a patch for `subprocess.Popen`.

    def test_case_sensitive_default(self):
### Changes Summary:
The code snippet defines a helper function `popen_fail` within the `test_command_output` test method. The helper function creates a `Mock` object representing a failed `Popen` process with return code 1 and mocked output values "foo" and "bar" for `communicate`.

        self.assertEqual(
            util.case_sensitive(path),
            platform.system() != "Windows",
        )

    @unittest.skipIf(sys.platform == "win32", "fs is not case sensitive")
    def test_case_sensitive_detects_sensitive(self):
        # FIXME: Add tests for more code paths of case_sensitive()
        # when the filesystem on the test runner is not case sensitive
        pass

    @unittest.skipIf(sys.platform != "win32", "fs is case sensitive")
    def test_case_sensitive_detects_insensitive(self):
        # FIXME: Add tests for more code paths of case_sensitive()
        # when the filesystem on the test runner is case sensitive
        pass


class PathConversionTest(_common.TestCase):
    def test_syspath_windows_format(self):
        with _common.platform_windows():
            path = os.path.join("a", "b", "c")
            outpath = util.syspath(path)
        self.assertTrue(isinstance(outpath, str))
        self.assertTrue(outpath.startswith("\\\\?\\"))

    def test_syspath_windows_format_unc_path(self):
        # The \\?\ prefix on Windows behaves differently with UNC
        # (network share) paths.
        path = "\\\\server\\share\\file.mp3"
        with _common.platform_windows():
            outpath = util.syspath(path)
        self.assertTrue(isinstance(outpath, str))
        self.assertEqual(outpath, "\\\\?\\UNC\\server\\share\\file.mp3")

    def test_syspath_posix_unchanged(self):
        with _common.platform_posix():
            path = os.path.join("a", "b", "c")
            outpath = util.syspath(path)
        self.assertEqual(path, outpath)

    def _windows_bytestring_path(self, path):
        old_gfse = sys.getfilesystemencoding
        sys.getfilesystemencoding = lambda: "mbcs"
        try:
            with _common.platform_windows():
                return util.bytestring_path(path)
        finally:
            sys.getfilesystemencoding = old_gfse

    def test_bytestring_path_windows_encodes_utf8(self):
        path = "caf\xe9"
        outpath = self._windows_bytestring_path(path)
        self.assertEqual(path, outpath.decode("utf-8"))

    def test_bytesting_path_windows_removes_magic_prefix(self):
        path = "\\\\?\\C:\\caf\xe9"
        outpath = self._windows_bytestring_path(path)
        self.assertEqual(outpath, "C:\\caf\xe9".encode())


class PathTruncationTest(_common.TestCase):
    def test_truncate_bytestring(self):
        with _common.platform_posix():
            p = util.truncate_path(b"abcde/fgh", 4)
        self.assertEqual(p, b"abcd/fgh")

    def test_truncate_unicode(self):
        with _common.platform_posix():
            p = util.truncate_path("abcde/fgh", 4)
        self.assertEqual(p, "abcd/fgh")

    def test_truncate_preserves_extension(self):
        with _common.platform_posix():
            p = util.truncate_path("abcde/fgh.ext", 5)
        self.assertEqual(p, "abcde/f.ext")


class ConfitDeprecationTest(_common.TestCase):
    def test_confit_deprecattion_warning_origin(self):
        """Test that importing `confit` raises a warning.

        In addition, ensure that the warning originates from the actual
        import statement, not the `confit` module.
        """
        # See https://github.com/beetbox/beets/discussions/4024
        with self.assertWarns(UserWarning) as w:
            import beets.util.confit  # noqa: F401

        self.assertIn(__file__, w.filename)
        self.assertNotIn("confit.py", w.filename)


def suite():
    return unittest.TestLoader().loadTestsFromName(__name__)


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
