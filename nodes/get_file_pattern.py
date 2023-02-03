# Copyright 2023 Fabrica Software, LLC

import iograft
import iobasictypes
import iosequencetypes


class GetFilePattern(iograft.Node):
    """
    Given a FileSequence object, return the file pattern the sequence
    represents.
    """
    sequence = iograft.InputDefinition("sequence",
                                       iosequencetypes.FileSequence())
    format_str = iograft.InputDefinition("format", iobasictypes.String(),
                        default_value="{dirname}{basename}{padding}{extension}")
    file_pattern = iograft.OutputDefinition("file_pattern", iobasictypes.Path())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("get_file_pattern", "fileseq")
        node.SetMenuPath("File Sequence")
        node.AddInput(cls.sequence)
        node.AddInput(cls.format_str)
        node.AddOutput(cls.file_pattern)
        return node

    @staticmethod
    def Create():
        return GetFilePattern()

    def Process(self, data):
        sequence = iograft.GetInput(self.sequence, data)
        format_str = iograft.GetInput(self.format_str, data)

        # Extract the file pattern from the sequence using the passed in
        # formatting string.
        file_pattern = sequence.format(template=format_str)
        iograft.SetOutput(self.file_pattern, data, file_pattern)


def LoadPlugin(plugin):
    node = GetFilePattern.GetDefinition()
    plugin.RegisterNode(node, GetFilePattern.Create)
