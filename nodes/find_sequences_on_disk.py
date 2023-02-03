# Copyright 2023 Fabrica Software, LLC

import iograft
import iobasictypes
import iosequencetypes

import fileseq


class FindSequencesOnDisk(iograft.Node):
    """
    Given a file pattern representing sequences to search for on disk, return
    a list of FileSequences that were found on disk.
    """
    file_pattern = iograft.InputDefinition("file_pattern", iobasictypes.Path())

    sequences = iograft.OutputDefinition("sequences",
                                         iosequencetypes.FileSequenceList())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("find_sequences_on_disk", "fileseq")
        node.SetMenuPath("File Sequence")
        node.AddInput(cls.file_pattern)
        node.AddOutput(cls.sequences)
        return node

    @staticmethod
    def Create():
        return FindSequencesOnDisk()

    def Process(self, data):
        file_pattern = iograft.GetInput(self.file_pattern, data)

        # Search for sequences on disk that match the file pattern.
        sequences = fileseq.findSequencesOnDisk(file_pattern,
                                                pad_style=fileseq.PAD_STYLE_HASH1)
        iograft.SetOutput(self.sequences, data, sequences)


def LoadPlugin(plugin):
    node = FindSequencesOnDisk.GetDefinition()
    plugin.RegisterNode(node, FindSequencesOnDisk.Create)
