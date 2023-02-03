# Copyright 2023 Fabrica Software, LLC

import iograft
import iobasictypes
import iosequencetypes

import fileseq


class FindSequenceOnDisk(iograft.Node):
    """
    Find the file sequence on disk matching the given file pattern.
    """
    file_pattern = iograft.InputDefinition("file_pattern", iobasictypes.Path())
    allow_no_match = iograft.InputDefinition("allow_no_match",
                                             iobasictypes.Bool(),
                                             default_value=False)

    sequence = iograft.OutputDefinition("sequence",
                                        iosequencetypes.FileSequence())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("find_sequence_on_disk", "fileseq")
        node.SetMenuPath("File Sequence")
        node.AddInput(cls.file_pattern)
        node.AddInput(cls.allow_no_match)
        node.AddOutput(cls.sequence)
        return node

    @staticmethod
    def Create():
        return FindSequenceOnDisk()

    def Process(self, data):
        file_pattern = iograft.GetInput(self.file_pattern, data)
        allow_no_match = iograft.GetInput(self.allow_no_match, data)

        # Search the disk for files that match the given pattern and return
        # the foudn sequence.
        try:
            sequence = fileseq.findSequenceOnDisk(
                                            file_pattern,
                                            preserve_padding=True,
                                            pad_style=fileseq.PAD_STYLE_HASH1)
        except fileseq.FileSeqException as e:
            if not allow_no_match:
                raise e

            sequence = fileseq.FileSequence(file_pattern,
                                            pad_style=fileseq.PAD_STYLE_HASH1)

        iograft.SetOutput(self.sequence, data, sequence)


def LoadPlugin(plugin):
    node = FindSequenceOnDisk.GetDefinition()
    plugin.RegisterNode(node, FindSequenceOnDisk.Create)
