# Copyright 2023 Fabrica Software, LLC

import iograft
import iobasictypes
import iosequencetypes


class EnumerateFileSequence(iograft.Node):
    """
    Convert a FileSequence object into a list of paths.
    """
    sequence = iograft.InputDefinition("sequence",
                                       iosequencetypes.FileSequence())
    files = iograft.OutputDefinition("files", iobasictypes.PathList())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("enumerate_file_sequence", "fileseq")
        node.SetMenuPath("File Sequence")
        node.AddInput(cls.sequence)
        node.AddOutput(cls.files)
        return node

    @staticmethod
    def Create():
        return EnumerateFileSequence()

    def Process(self, data):
        sequence = iograft.GetInput(self.sequence, data)

        # Use the fileseq.FileSequence type's default path expansion unless
        # the sequence has an empty frame set in which case we return an empty
        # list.
        files = []
        if not sequence.frameSet().is_null:
            files = list(sequence)

        iograft.SetOutput(self.files, data, files)


def LoadPlugin(plugin):
    node = EnumerateFileSequence.GetDefinition()
    plugin.RegisterNode(node, EnumerateFileSequence.Create)
