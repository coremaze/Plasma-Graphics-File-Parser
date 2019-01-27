import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import struct
import io
from PlasmaNames import *


def ReadWideString(bstring):
    length, = struct.unpack('<I', bstring[:4])
    string = bstring[4:4+length*2].decode('UTF-16')
    return string
def ReadString(bstring):
    length, = struct.unpack('<I', bstring[:4])
    string = bstring[4:4+length].decode('UTF-8')
def MakeWideString(string):
    blength = struct.pack('<I', len(string))
    bstring = string.encode('UTF-16')[2:]
    return blength + bstring
def MakeString(string):
    blength = struct.pack('<I', len(string))
    bstring = string.encode('UTF-8')
    return blength + bstring


def HexDumpToBin(string):
    return bytes([int(x, base=16) for x in string.strip().split(' ')])
def FloatArrayStringToBin(string):
    string = string.strip().lstrip('[').rstrip(']')
    lst = string.split(',')
    lst = [float(x.strip()) for x in lst]
    return b''.join([struct.pack('f', x) for x in lst])
def LengthPrefixedUintArrayFromStringToBin(string): #mistakes have been made
    string = string.strip().lstrip('[').rstrip(']')
    lst = string.split(',')
    lst = [int(x.strip()) for x in lst]
    blen = struct.pack('<I', len(lst))
    return blen + b''.join([struct.pack('I', x) for x in lst])
def IntArrayStringToBin(string):
    string = string.strip().lstrip('[').rstrip(']')
    lst = string.split(',')
    lst = [int(x.strip()) for x in lst]
    return b''.join([struct.pack('i', x) for x in lst])



# a 64-bit version of java's String.hashCode,
def JavaLongStringHash(bytestring):
    h = 1125899906842597
    for x in bytestring:
        h = (31*h + x) & 0xFFFFFFFFFFFFFFFF
    return struct.pack('<Q', h)


#The key used to obfuscate chunk type declaration names
CONST_OBFU_KEY = JavaLongStringHash(b'PlasmaXGraphics')

def DeobfuscateData(data):
    data_size = len(data)
    key = CONST_OBFU_KEY
    first_bytes_as_uint32 = struct.unpack('I', key[0:4])[0]
    key_offset = first_bytes_as_uint32 % data_size
    output = bytearray(data_size)
    for i in range(data_size):
        cur = data[i]
        out_idx = (key_offset+i)%data_size
        key_idx = out_idx%8
        cur_key = key[key_idx]
        out_byte = (cur - cur_key) & 0xff
        output[out_idx] = out_byte
    return output
def ObfuscateData(data): 
    data_size = len(data)
    key = CONST_OBFU_KEY 
    first_bytes_as_uint32 = struct.unpack('I', key[0:4])[0] 
    key_offset = first_bytes_as_uint32 % data_size 
    output = bytearray(data_size) 
    for i in range(data_size): 
        in_idx = (key_offset+i)%data_size
        out_idx=i
        cur = data[in_idx]
        key_idx = in_idx%8
        cur_key = key[key_idx]
        out_byte = (cur + cur_key)&0xff
        output[out_idx] = out_byte
    return output  


class Chunk():
    def __init__(self, _id, data):
        self.id = _id
        self.data = data
        self.typeName = ''

    @classmethod 
    def ReadFrom(self, rdr):
        _id = struct.unpack('I', rdr.read(4))[0]
        data_size = struct.unpack('I', rdr.read(4))[0]
        data = rdr.read(data_size)
        return self(_id, data)

    @classmethod
    def FromXML(self, element, parent, IDs, obfuscated=False):
        data = b''
        if list(element):
            for e in element:
                data += Chunk.FromXML(e, element, IDs, obfuscated=obfuscated)
        else:
            #raw data
            #int
            if element.tag in INT_TYPES:
                data = struct.pack('<i', int(element.text))
            #uint
            elif element.tag in UINT_TYPES:
                data = struct.pack('<I', int(element.text))
            #length prefixed wstring
            elif element.tag in LENGTH_PREFIXED_WSTRING_TYPES:
                if element.text:
                    data = MakeWideString(element.text.strip())
                else:
                    data = MakeWideString('')

            #float
            elif element.tag in FLOAT_TYPES:
                data = struct.pack('<f', float(element.text))

            #float array
            elif element.tag in FLOAT_ARRAY_TYPES:
                data = FloatArrayStringToBin(element.text)

            #uint array
            elif element.tag in UINT_ARRAY_TYPES:
                data = LengthPrefixedUintArrayFromStringToBin(element.text)

            #special cases for each ArrayAttribute.frame
            elif element.tag == 'Attribute.frame':
                if parent.tag in FLOAT_ATTRIBUTE_CONTAINERS:
                    data = FloatArrayStringToBin(element.text)
                elif parent.tag in LENGTH_PREFIXED_WSTRING_ATTRIBUTE_CONTAINERS:
                    if element.text:
                        data = MakeWideString(element.text.strip())
                    else:
                        data = MakeWideString('')

                #int array    
                elif parent.tag in INT_ATTRIBUTE_CONTAINERS:
                    data = IntArrayStringToBin(element.text)
            elif element.tag == 'ArrayAttribute.frame': 
                if parent.tag in FLOAT_ARRAYATTRIBUTE_CONTAINERS:
                    data = FloatArrayStringToBin(element.text)

        if data == b'':
            data = HexDumpToBin(element.text)
            

        typeName = element.tag

        header_data = b''
        if typeName not in IDs:
            #allocate a new ID
            ID = max([IDs[k] for k in IDs]) + 1
            print(f'Assigning ID {ID} for {typeName}')
            #construct a header
            IDs[typeName] = ID
            header_name_data = MakeString(typeName)
            if obfuscated:
                header_name_data = header_name_data[:4] + ObfuscateData(header_name_data[4:])
            header_size = len(header_name_data) + 4
            header_data += struct.pack('<III', 0, header_size, ID) + header_name_data
        else:
            ID = IDs[typeName]

        size = len(data)
        data = header_data + struct.pack('<II', ID, size) + data
        
        return data
    
    def __str__(self):
        return self.typeName
    __repr__ = __str__


    

class PLX():
    def __init__(self, fileName):
        self.id_type_map = {}
        self.fileName = fileName
        self.obfuscated = False
        with open(fileName, 'rb') as f:
            self.length = len(f.read())

    def __enter__(self):
        self.fd = open(self.fileName, 'rb')
        return self

    def __exit__(self, _type, value, traceback):
        self.fd.close()

    def toXML(self, reader=None, length=None, xml_parent=None, parent=None):
        if length == None:
            length = self.length
        if reader is None:
            reader = self.fd
        if xml_parent is None:
            xml_parent = ET.Element('root')
        if parent is None:
            parent = self

        while reader.tell() < length:
            chunk = Chunk.ReadFrom(reader)

            #Type definition
            if chunk.id == 0:
                name_def = Chunk.ReadFrom(io.BytesIO(chunk.data))

                #Get name, or decode if obfuscated
                if self.obfuscated:
                    name = DeobfuscateData(name_def.data).decode('UTF-8')
                else:
                    name = name_def.data.decode('UTF-8')

                #If Seal is present, future chunks are obfuscated.
                if name == 'Seal':
                    self.obfuscated = True

                #Rememeber that this ID corresponds to this name.
                self.id_type_map[name_def.id] = name
                print(f'{name} was defined with ID {name_def.id}')

            #Actual data; not a type definition
            else:
                type_name = self.id_type_map[chunk.id]
                chunk.typeName = type_name
                chunk_xml_node = ET.SubElement(xml_parent, chunk.typeName)

                #If it's not the lowest level of data.
                if type_name in objectNames:
                    self.toXML(reader=io.BytesIO(chunk.data), length=len(chunk.data), xml_parent=chunk_xml_node, parent=chunk)
                #raw data
                else:
                    dump = ' '.join(['%02X' % x for x in chunk.data])

                    data_text = dump

                    #int
                    if chunk_xml_node.tag in INT_TYPES:
                        data_text = str(struct.unpack('<i', chunk.data)[0])

                    #uint
                    elif chunk_xml_node.tag in UINT_TYPES:
                        data_text = str(struct.unpack('<I', chunk.data)[0])

                    #length prefixed wstring
                    elif chunk_xml_node.tag in LENGTH_PREFIXED_WSTRING_TYPES:
                        data_text = ReadWideString(chunk.data)

                    #float
                    elif chunk_xml_node.tag in FLOAT_TYPES:
                        data_text = str(struct.unpack('<f', chunk.data)[0])

                    #float array
                    elif chunk_xml_node.tag in FLOAT_ARRAY_TYPES:
                        lst = []
                        for i in range(0, len(chunk.data), 4):
                            lst.append(struct.unpack('<f', chunk.data[i:i+4])[0])
                        data_text = str(lst)

                    #uint array
                    elif chunk_xml_node.tag in UINT_ARRAY_TYPES:
                        array_length, = struct.unpack("<i", chunk.data[:4])
                        lst = []
                        for i in range(4, len(chunk.data), 4):
                            lst.append(struct.unpack('<I', chunk.data[i:i+4])[0])
                        data_text = str(lst)
                    

                    #special cases for each ArrayAttribute.frame
                    elif chunk_xml_node.tag == 'Attribute.frame':
                        if xml_parent.tag in FLOAT_ATTRIBUTE_CONTAINERS:
                            lst = []
                            for i in range(0, len(chunk.data), 4):
                                lst.append(struct.unpack('<f', chunk.data[i:i+4])[0])
                            data_text = str(lst)
                        elif xml_parent.tag in LENGTH_PREFIXED_WSTRING_ATTRIBUTE_CONTAINERS:
                            data_text = ReadWideString(chunk.data)

                        #int array    
                        elif xml_parent.tag in INT_ATTRIBUTE_CONTAINERS:
                            lst = []
                            for i in range(0, len(chunk.data), 4):
                                lst.append(struct.unpack('<i', chunk.data[i:i+4])[0])
                            data_text = str(lst)

                    elif chunk_xml_node.tag == 'ArrayAttribute.frame': 
                        if xml_parent.tag in FLOAT_ARRAYATTRIBUTE_CONTAINERS:
                            lst = []
                            for i in range(0, len(chunk.data), 4):
                                lst.append(struct.unpack('<f', chunk.data[i:i+4])[0])
                            data_text = str(lst)


                    if data_text == dump:
                        print('Leaving as hex dump:', chunk_xml_node.tag, xml_parent.tag, dump)
                    chunk_xml_node.text = data_text
                
        return xml_parent

    @staticmethod
    def ConvertToXMLTree(fileName):
        this = PLX(fileName)
        with this:
            root = this.toXML()
        return root
        

    @classmethod
    def FromXML(self, xml_file):
        IDs = {None:0}
        data = b''
        xml = ET.parse(xml_file)
        root = xml.getroot()
        obfuscated = False
        for e in root:
            data += Chunk.FromXML(e, root, IDs, obfuscated=obfuscated)
            if e.tag == 'Seal':
                obfuscated = True
        return data
        
        

import sys
def main():
    if len(sys.argv) != 4:
        print("USAGE: PLXML.py <XML | PLX - file type to create> <input file> <output file>")
        type_to_make = input("Type to make: ")
        input_file = input("Input file: ")
        output_file = input("Output file: ")
    else:
        _, type_to_make, input_file, output_file = sys.argv

    if type_to_make.lower() == 'plx':
        data = PLX.FromXML(input_file)
        with open(output_file, 'wb') as f:
            f.write(data)
    elif type_to_make.lower() == 'xml':
        root = PLX.ConvertToXMLTree(input_file)

        ENCODING = 'UTF-16'
        xml = ET.tostring(root, encoding=ENCODING)
        with open(output_file, 'wb') as f:
            pretty_xml = BeautifulSoup(xml, "xml").prettify(ENCODING)
            f.write(pretty_xml)
            
if __name__ == '__main__':
    main()

    
    

