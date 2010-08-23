#!/usr/bin/python26

import unittest
from datetime import datetime
from hdfs import *


class ConnectDisconnectTestCase(unittest.TestCase):
  def test_connect_disconnect(self):
    fs = hdfsConnect('hadoop.twitter.com', 8020)
    hdfsDisconnect(fs)


class ExistsTestCase(unittest.TestCase):
  def setUp(self):
    self.fs = hdfsConnect('hadoop.twitter.com', 8020)

  def test_exists(self):
    self.assertTrue(hdfsExists(self.fs, '/'))

  def test_does_not_exist(self):
    self.assertFalse(hdfsExists(self.fs, '/doesnotexist'))

  def tearDown(self):
    hdfsDisconnect(self.fs)


class ListDirectoryTestCase(unittest.TestCase):
  def setUp(self):
    self.fs = hdfsConnect('hadoop.twitter.com', 8020)

  def test_list_diretory(self):
    entries = hdfsListDirectory(self.fs, '/user')
    self.assertTrue(entries)

  def test_list_missing_directory(self):
    entries = hdfsListDirectory(self.fs, '/doesnotexist')
    self.assertEqual(entries, None)

  def tearDown(self):
    hdfsDisconnect(self.fs)


class OpenCloseTestCase(unittest.TestCase):
  def setUp(self):
    self.fs = hdfsConnect('hadoop.twitter.com', 8020)

  def test_open_close_read(self):
    fh = hdfsOpen(self.fs, '/user/travis/hosts', 'r')
    hdfsClose(self.fs, fh)

  def test_open_close_write(self):
    path = '/user/travis/test_%s' % datetime.now().strftime('%Y%m%dT%H%M%SZ')
    fh = hdfsOpen(self.fs, path, 'w')
    hdfsClose(self.fs, fh)

  def tearDown(self):
    hdfsDisconnect(self.fs)

class ReadWriteTestCase(unittest.TestCase):
  def setUp(self):
    self.fs = hdfsConnect('hadoop.twitter.com', 8020)

  def test_read_write(self):
    path = '/user/travis/test_%s' % datetime.now().strftime('%Y%m%dT%H%M%SZ')
    data = 'read write test'
    #path = '/user/travis/scribe.conf'

    fh = hdfsOpen(self.fs, path, 'w')
    bytes_written = hdfsWrite(self.fs, fh, data)
    self.assertEqual(bytes_written, len(data))
    hdfsClose(self.fs, fh)

    fh = hdfsOpen(self.fs, path, 'r')
    read_data = hdfsRead(self.fs, fh)
    self.assertEqual(read_data, data)
    hdfsClose(self.fs, fh)

  def tearDown(self):
    hdfsDisconnect(self.fs)


if __name__ == '__main__':
  test_cases = [ConnectDisconnectTestCase,
                ExistsTestCase,
                ListDirectoryTestCase,
                OpenCloseTestCase,
                ReadWriteTestCase,
               ]
  for test_case in test_cases:
    suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
    unittest.TextTestRunner(verbosity=2).run(suite)

# EOF