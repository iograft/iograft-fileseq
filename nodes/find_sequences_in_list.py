# Copyright 2023 Fabrica Software, LLC

import iograft
import iobasictypes
import iosequencetypes

import fileseq


class FindSequencesInList(iograft.Node):
    """
    Given a list of paths, convert to a list of fileseq.FileSequence objects
    representing those same paths.
    """
    files = iograft.InputDefinition("files", iobasictypes.PathList())
    include_empty = iograft.InputDefinition("include_empty",
                                            iobasictypes.Bool(),
                                            default_value=False)


    sequences = iograft.OutputDefinition("sequences",
                                         iosequencetypes.FileSequenceList())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("find_sequences_in_list", "fileseq")
        node.SetMenuPath("File Sequence")
        node.AddInput(cls.files)
        node.AddInput(cls.include_empty)
        node.AddOutput(cls.sequences)
        return node

    @staticmethod
    def Create():
        return FindSequencesInList()

    def Process(self, data):
        files = iograft.GetInput(self.files, data)
        include_empty = iograft.GetInput(self.include_empty, data)

        # Extract the sequences from the list of paths.
        sequences = fileseq.findSequencesInList(files,
                                                pad_style=fileseq.PAD_STYLE_HASH1)

        if not include_empty:
            sequences = [s for s in sequences if s.frameSet() is not None]

        iograft.SetOutput(self.sequences, data, sequences)


def LoadPlugin(plugin):
    node = FindSequencesInList.GetDefinition()
    plugin.RegisterNode(node, FindSequencesInList.Create)
