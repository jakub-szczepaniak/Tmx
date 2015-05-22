from lxml import etree as ET
from lxml.builder import ElementMaker
from collections import namedtuple
from hashlib import md5
import codecs


TMX_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
TMX = "{%s}" % TMX_NAMESPACE
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
    E = ElementMaker(
        namespace=TMX_NAMESPACE,
        nsmap={None: TMX_NAMESPACE})
    TRANS_UNIT = E.tu
    TUV = E.tuv
    PROP = E.prop
    SEG = E.seg

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

    def __create_tuv(self):

        source = TU.E.tuv(
            self.__create_seg(self.source),
            {'lang': self.language_pair.source})
        target = TU.E.tuv(
            self.__create_seg(self.source),
            {'lang': self.language_pair.target})
        return [source, target]

    def __create_seg(self, text):
        return TU.E.seg(text)

    def __create_properties(self):
        
        return [TU.PROP({'type': k}, v) for k, v in self.properties]

    def toxml(self):
        '''creates xml tuv element according to TMX specification'''
        new_tuv = TU.E.tu(
            self.attributes,
            *self.__create_properties()
            )

        print(ET.tostring(new_tuv, pretty_print=True))
        NSMAP = {None: TMX_NAMESPACE}
        tuv = ET.Element(TMX + 'tu', nsmap=NSMAP)
        tuv.attrib.update(self.attributes)
        for prop_name, prop_value in self.properties.items():
            prop = ET.SubElement(tuv, TMX + 'property')
            prop.attrib['type'] = prop_name
            prop.text = prop_value

        tu1 = ET.SubElement(tuv, TMX + 'tuv')
        tu1.attrib['lang'] = self.language_pair[0]
        seg1 = ET.fromstring('<seg>{}</seg>'.format(self.source))
        tu1.append(seg1)

        tu2 = ET.SubElement(tuv, TMX + 'tuv')
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
                list_tuv[0].attrib['{}lang'.format(TMX)],
                list_tuv[1].attrib['{}lang'.format(TMX)])
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
            raise AttributeError('Not valid Translation Unit' + xml_tu.tag)

    def get_source_hash(self):
        '''calculates hash of the source text - used to detect repetitions'''
        return md5(codecs.encode(self.source)).hexdigest()

    def changeuserid(self, new_id):
        self.attributes['creationid'] = self.attributes['changeid'] = new_id
        return self


class TransUnit(object):

    def __init__(
            self,
            source,
            target,
            lang_pair=('', ''),
            attributes={},
            properties={}):
        self.lang_pair = lang_pair
        self.attributes = attributes
        self.properties = properties
        self.source = source
        self.target = target


def toxml(transunit):
    TMX_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
    TMX = "{%s}" % TMX_NAMESPACE
    E = ElementMaker(
        namespace=TMX_NAMESPACE,
        nsmap={None: TMX_NAMESPACE})
    TU = E.tu
    TUV = E.tuv
    PROP = E.prop
    SEG = E.seg
    prop = [PROP({'type': k}, v) for k, v in transunit.properties.items()]
    source = TUV({'lang': transunit.lang_pair[0]}, SEG(transunit.source))
    target = TUV({'lang': transunit.lang_pair[1]}, SEG(transunit.target))
    result = TU(transunit.attributes, source, target, *prop)
    print(ET.tostring(result, pretty_print=True))
    return result
