# Copyright 2023 Fabrica Software, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import iograft
import fileseq


class FrameSet(iograft.PythonType):
    """
    Type wrapping the fileseq.FrameSet object providing functionality for
    defining a set of frames.
    """
    type_id = iograft.TypeId("FrameSet", "fileseq")
    value_type = fileseq.FrameSet

    def __init__(self):
        super(FrameSet, self).__init__(FrameSet.type_id,
                                       value_type=FrameSet.value_type)

    @staticmethod
    def ToString(value):
        """
        Return the string representation of a fileseq.FrameSet object for
        display in the iograft UI.
        """
        return str(value)

    @staticmethod
    def FromString(string_value):
        """
        Generate a fileseq.FrameSet object from the given string.
        """
        return fileseq.FrameSet(string_value)

    @staticmethod
    def SerializeValue(value):
        """
        Serialization function for fileseq.FrameSet objects. Uses the
        frame set's string representation.
        """
        # First convert to string and then use iograft's default serialization
        # function.
        str_value = str(value)
        return iograft.SerializeValue(str_value)

    @staticmethod
    def DeserializeValue(serialized_value):
        """
        Deserialization function for fileseq.FrameSet objects.
        """
        # First deserialize the string using iograft's default deserialization.
        str_value = iograft.DeserializeValue(serialized_value)
        return fileseq.FrameSet(str_value)


@iograft.castfunction
def _FrameSetToString(value):
    return FrameSet.ToString(value)

@iograft.castfunction
def _FrameSetFromString(value):
    return FrameSet.FromString(value)


class FileSequence(iograft.PythonType):
    """
    Type wrapping a fileseq.FileSequence object providing functionality for
    working with sequences.
    """
    type_id = iograft.TypeId("FileSequence", "fileseq")
    value_type = fileseq.FileSequence

    def __init__(self):
        super(FileSequence, self).__init__(FileSequence.type_id,
                                           value_type=FileSequence.value_type)

    @staticmethod
    def ToString(value):
        """

        """
        # Create a custom output string format that resembles the Nuke
        # file output.
        output_str = "".join([value.dirname(),
                              value.basename(),
                              value.framePadding(),
                              value.extension()])
        # Add the frame range after the formatting.
        output_str += " ({})".format(value.frameSet())
        return output_str

    @staticmethod
    def FromString(string_value):
        """

        """
        # Detect if the input string matches the format of the ToString
        # function of this iograft wrapping.
        range_start = string_value.rfind("(")
        if string_value.endswith(")") and range_start > 0:
            # Extract the frame range striping down to just the numbers.
            range_str = string_value[range_start:].strip("( )")

            # Create the sequence.
            filename = string_value[:range_start].strip()
            sequence = fileseq.FileSequence(filename,
                                            pad_style=fileseq.PAD_STYLE_HASH1)

            # Set the frame range.
            sequence.setFrameSet(range_str)
            return sequence

        # Otherwise, treat as a standard input to the FileSequence constructor.
        # Create the FileSequence object. At the moment, this is not able
        # to take additional arguments when constructing the sequence
        # object.
        sequence = fileseq.FileSequence(string_value,
                                        pad_style=fileseq.PAD_STYLE_HASH1)
        return sequence

    @staticmethod
    def SerializeValue(value):
        """

        """
        # Convert the sequence to the dictionary form and then use iograft's
        # default serialization function.
        seq_dict = value.to_dict()
        return iograft.SerializeValue(seq_dict)

    @staticmethod
    def DeserializeValue(serialized_value):
        """

        """
        # Unpack the serialized value using iograft's default serialization
        # and then convert from the dictionary to a FileSequence object.
        seq_dict = iograft.DeserializeValue(serialized_value)
        return fileseq.FileSequence.from_dict(seq_dict)


class FileSequenceList(iograft.PythonListType):
    """
    Type representing a list of Python floating point numbers.
    """
    def __init__(self):
        super(FileSequenceList, self).__init__(
                                        FileSequence.type_id,
                                        base_value_type=FileSequence.value_type)


def LoadPlugin(plugin):
    # Register the FrameSet type.
    frame_set_type = plugin.RegisterPythonType(FrameSet.type_id,
                                               FrameSet(),
                                               FrameSet.ToString,
                                               FrameSet.FromString,
                                               FrameSet.SerializeValue,
                                               FrameSet.DeserializeValue,
                                               menu_path="File Sequence")

    # Try to register casts between FrameSets and strings.
    try:
        import iobasictypes
        plugin.RegisterTypeCast(iobasictypes.String().GetTypeId(),
                                FrameSet.type_id,
                                _FrameSetFromString)
        plugin.RegisterTypeCast(FrameSet.type_id,
                                iobasictypes.String().GetTypeId(),
                                _FrameSetToString)
    except ImportError:
        pass

    # Register the FileSequence type.
    sequence_type = plugin.RegisterPythonType(FileSequence.type_id,
                                              FileSequence(),
                                              FileSequence.ToString,
                                              FileSequence.FromString,
                                              FileSequence.SerializeValue,
                                              FileSequence.DeserializeValue,
                                              menu_path="File Sequence")

    # Also register the list type for FileSequences.
    plugin.RegisterPythonListType(sequence_type,
                                  FileSequenceList(),
                                  menu_path="File Sequence")
