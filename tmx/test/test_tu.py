import unittest


from tmx.tu import fromxml
from tmx.tu import LanguagePair

from tmx import TU, TransUnit
from lxml import etree as ET


class TestTU(unittest.TestCase):

    def setUp(self):
        expected_tu = '''
            <tu changedate="20141017T092614Z" \
      creationdate="20141016T091130Z" \
      creationid="Foo" changeid="Bar">
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
            '''
        self.xml_tu = ET.fromstring(expected_tu)
        self.lang_pair = LanguagePair(source='en', target='zh-CN')

        self.wrong_unit = ET.fromstring('''<a>Some dummy XML</a>''')

    def tearDown(self):
        pass

    def test_tu_from_xml_element_works(self):
        new_tu = fromxml(self.xml_tu)
        self.assertIsInstance(new_tu, TU, "TU object not created")

    def test_wrong_tu_raises_exception(self):

        with self.assertRaises(AttributeError):
            new_tu = fromxml(self.wrong_unit)

    def test_language_pair_is_correct(self):
        new_tu = fromxml(self.xml_tu)
        self.assertEqual(new_tu.language_pair, self.lang_pair)

    def test_segment_attributes_are_read(self):
        new_tu = fromxml(self.xml_tu)
        self.assertEqual(
            new_tu.attributes['creationdate'],
            '20141016T091130Z',
            'creationdate is wrong')
        self.assertEqual(
            new_tu.attributes['creationid'],
            'Foo',
            'creationid is wrong')
        self.assertEqual(
            new_tu.attributes['changeid'],
            'Bar',
            'changeid is wrong')
        self.assertEqual(
            new_tu.attributes['changedate'],
            '20141017T092614Z',
            'changedate is wrong')

    def test_set_user_id_works(self):
        new_tu = fromxml(self.xml_tu)
        updated_tu = new_tu.changeuserid('FooBaz')
        self.assertEqual(
            updated_tu.attributes['creationid'],
            'FooBaz',
            'creationid not updated')
        self.assertEqual(
            updated_tu.attributes['changeid'],
            'FooBaz',
            'changeid not updated')

    def test_equal_returns_true(self):
        first_tu = fromxml(self.xml_tu)
        same_tu = fromxml(self.xml_tu)

        self.assertEqual(first_tu == same_tu, True, 'Same TUs are not equal')

    def test_not_equal_returns_false(self):
        first_tu = fromxml(self.xml_tu)
        other_tu = fromxml(self.xml_tu)
        other_tu.source = 'Do not integrate'

        self.assertEqual(
            first_tu == other_tu,
            False,
            'Different TUs are equal')

    @unittest.skip('waiting for different implementation')
    def test_toxml_creates_expected_xml_element(self):
        new_tu = fromxml(self.xml_tu)

        saved_element = new_tu.toxml()

        reloaded_tu = fromxml(saved_element)
        self.assertEqual(reloaded_tu, new_tu)


class TestNewTU(unittest.TestCase):

    def setUp(self):
        self.attributes = {
            'creationid': 'Milengo',
            'changeid': 'Bar',
            'creationdate': '20141017T092614Z',
            'changedate': '20141017T092614Z'}
        self.lang_pair = ('en', 'de')
        self.properties = {
            'client': 'Milengo',
            'domain': 'IT - Network & Infrastructure'
        }

    def tearDown(self):
        pass

    def test_new_tu_is_created(self):
        self.assertIsInstance(TransUnit('', ''), TransUnit)

    def test_new_tu_has_language_pair(self):
        new_tu = TransUnit('', '', lang_pair=self.lang_pair)
        self.assertEqual(new_tu.lang_pair, self.lang_pair)

    def test_new_tu_has_obligatory_attributes(self):
        new_tu = TransUnit('', '', attributes=self.attributes)
        self.assertEqual(new_tu.attributes, self.attributes)

    def test_new_tu_has_properties(self):
        new_tu = TransUnit('', '', properties=self.properties)
        self.assertEqual(new_tu.properties, self.properties)
