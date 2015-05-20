from lxml import etree as ET
from collections import namedtuple
from hashlib import md5
import codecs


TMX_NAMESPACE = "{http://www.w3.org/XML/1998/namespace}"
LanguagePair = namedtuple('LanguagePair', ['source', 'target'])


def create_properties_dict(element):
    '''retrieves prop elements from TU'''
    properties = dict()
    for prop in element.findall('prop'):
        properties[prop.attrib['type']] = prop.text
    return properties


def fromxml(tu_element):
    return TU(tuv=tu_element)


class TU(object):

    """TU - translation unit"""

    def __init__(self, tuv=None):

        self.source = ""
        self.target = ""
        # custom properties for a translation unit
        self.properties = dict()
        # obligatory attributes for a translation unit
        self.attributes = dict()
        self.language_pair = LanguagePair(source='', target='')
        if tuv is not None:
            self.fromxml(xml_tu=tuv)

    def __eq__(self, other):
        return self.get_source_hash() == other.get_source_hash()

    def __ne__(self, other):
        return self.get_source_hash() != other.get_source_hash()

    def toxml(self):
        '''creates xml tuv element according to TMX specification'''
        tuv = ET.Element('tu')
        tuv.attrib.update(self.attributes)
        for prop_name, prop_value in self.properties.items():
            prop = ET.SubElement(tuv, 'property')
            prop.attrib['type'] = prop_name
            prop.text = prop_value

        tu1 = ET.SubElement(tuv, 'tuv')
        tu1.attrib['lang'] = self.language_pair[0]
        seg1 = ET.fromstring('<seg>{}</seg>'.format(self.source))
        tu1.append(seg1)

        tu2 = ET.SubElement(tuv, 'tuv')
        tu2.attrib['lang'] = self.language_pair[1]
        seg2 = ET.fromstring('<seg>{}</seg>'.format(self.target))
        tu2.append(seg2)

        return tuv

    def fromxml(self, xml_tu):
        '''parses tuv element to read data'''

        if xml_tu is not None and xml_tu.tag == 'tu':
            self.properties = create_properties_dict(xml_tu)
            self.attributes.update(xml_tu.attrib)

            list_tuv = xml_tu.findall('tuv')

            self.language_pair = LanguagePair(
                list_tuv[0].attrib['{}lang'.format(TMX_NAMESPACE)],
                list_tuv[1].attrib['{}lang'.format(TMX_NAMESPACE)])
            segments = xml_tu.findall('./tuv/seg')
            self.source = ET.tostring(
                segments[0],
                method='text',
                encoding='unicode')
            self.target = ET.tostring(
                segments[1],
                method='text',
                encoding='unicode')
        else:
            raise AttributeError('Not valid Translation Unit')

    def get_source_hash(self):
        '''calculates hash of the source text - used to detect repetitions'''
        return md5(codecs.encode(self.source)).hexdigest()

    def changeuserid(self, new_id):
        self.attributes['creationid'] = self.attributes['changeid'] = new_id
        return self
