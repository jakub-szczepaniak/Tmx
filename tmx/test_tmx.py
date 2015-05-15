import unittest
from unittest.mock import patch
from tmx.tmx import fromstring
from tmx.tmx import fromfile
from tmx.tmx import Tmx
from lxml import etree as ET


class TestTMXUnit(unittest.TestCase):

    def setUp(self):
        self.sample = '''<?xml version="1.0"?>
<!DOCTYPE tmx SYSTEM "tmx14.dtd">
<tmx version="1.4">
<header creationtool="MemoQ" \
creationtoolversion="7.0.70" \
segtype="sentence" adminlang="en-us" \
creationid="Karsten Weiss" srclang="en" \
o-tmf="MemoQTM" datatype="unknown">
  <prop type="defclient">Ooyala</prop>
  <prop type="defproject"> </prop>
  <prop type="defdomain">IT - Network &amp; Infrastructure</prop>
  <prop type="defsubject"> </prop>
  <prop type="description"> </prop>
  <prop type="targetlang">zh-CN</prop>
  <prop type="name">Ooyala_TestTranslation_EN2ZH-CN</prop>
</header>
<body>
  <tu changedate="20141017T092614Z" \
  creationdate="20141016T091130Z" \
  creationid="CN_Merlin_5" changeid="CN_Merlin_6">
    <prop type="client">Ooyala</prop>
    <prop type="project"> </prop>
    <prop type="domain"> </prop>
    <prop type="subject"> </prop>
    <prop type="corrected">no</prop>
    <prop type="aligned">no</prop>
    <prop type="x-document">backlot_integrate_with_tinypass.xml</prop>
    <tuv xml:lang="en">
      <prop type="x-context-post">\
      &lt;seg&gt;Paywalls enable you to require \
      payment before viewers can access your \
      content.&lt;/seg&gt;</prop>
      <seg>Integrate with Tinypass</seg>
    </tuv>
    <tuv xml:lang="zh-CN">
      <seg>与 Tinypass 集成</seg>
    </tuv>
  </tu>
  </body>
  </tmx>'''
        self.filename = 'sample.tmx'

    def tearDown(self):
        pass

    def test_create_from_string_returns_proper_Tmx_object(self):
        self.assertIsInstance(fromstring(self.sample), Tmx)

    @patch('tmx.tmx.ET')
    def test_create_from_file_returns_proper_Tmx_object(self, mock):
        mock.parse.return_value = ET.fromstring(self.sample)

        sample_tmx = fromfile(self.filename)

        self.assertEqual(mock.parse.called, True)
        self.assertIsInstance(sample_tmx, Tmx)

    def test_length_returns_proper_value(self):
        self.assertEqual(len(fromstring(self.sample)), 1)

    def test_custom_properties_are_not_empty(self):

        tmx = fromstring(self.sample)
        self.assertEqual(len(tmx.properties), 7)

    def test_tmx_attributes_are_not_empty(self):

        tmx = fromstring(self.sample)
        self.assertEqual(len(tmx.attributes), 8)

if __name__ == '__main__':
    unittest.main()
