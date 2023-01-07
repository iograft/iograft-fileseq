# Copyright 2023 Fabrica Software, LLC

import iograft
import iosequencetypes


class GetFrameSet(iograft.Node):
    """
    Given an fileseq.FileSequence, extract the frame set the sequence object
    represents.
    """
    sequence = iograft.InputDefinition("sequence",
                                       iosequencetypes.FileSequence())
    frame_set = iograft.OutputDefinition("frame_set",
                                         iosequencetypes.FrameSet())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("get_frame_set", "fileseq")
        node.SetMenuPath("File Sequence")
        node.AddInput(cls.sequence)
        node.AddOutput(cls.frame_set)
        return node

    @staticmethod
    def Create():
        return GetFrameSet()

    def Process(self, data):
        sequence = iograft.GetInput(self.sequence, data)
        frame_set = sequence.frameSet()
        iograft.SetOutput(self.frame_set, data, frame_set)


def LoadPlugin(plugin):
    node = GetFrameSet.GetDefinition()
    plugin.RegisterNode(node, GetFrameSet.Create)
