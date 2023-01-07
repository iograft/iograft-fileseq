# Copyright 2023 Fabrica Software, LLC

import iograft
import fileseq

import iobasictypes
import iosequencetypes


class CreateFileSequence(iograft.Node):
    """
    Create a new file sequence.
    """
    file_pattern = iograft.InputDefinition("file_pattern",
                                           iobasictypes.Path())
    frame_set = iograft.InputDefinition("frame_set",
                                        iosequencetypes.FrameSet(),
                                        default_value=fileseq.FrameSet(""))
    sequence = iograft.OutputDefinition("sequence",
                                        iosequencetypes.FileSequence())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("create_file_sequence", "file_seq")
        node.SetMenuPath("File Sequence")
        node.AddInput(cls.file_pattern)
        node.AddInput(cls.frame_set)
        node.AddOutput(cls.sequence)
        return node

    @staticmethod
    def Create():
        return CreateFileSequence()

    def Process(self, data):
        file_pattern = iograft.GetInput(self.file_pattern, data)
        frame_set = iograft.GetInput(self.frame_set, data)

        # Build the sequence.
        sequence = fileseq.FileSequence(file_pattern,
                                        pad_style=fileseq.PAD_STYLE_HASH1)
        sequence.setFrameSet(frame_set)
        iograft.SetOutput(self.sequence, data, sequence)


def LoadPlugin(plugin):
    node = CreateFileSequence.GetDefinition()
    plugin.RegisterNode(node, CreateFileSequence.Create)
