# Copyright 2023 Fabrica Software, LLC

import iograft
import iosequencetypes


class SetFrameSet(iograft.Node):
    """
    Set the frames that a fileseq.FileSequence object should represent.
    """

    sequence = iograft.InputDefinition("sequence",
                                       iosequencetypes.FileSequence())
    frame_set = iograft.InputDefinition("frame_set",
                                        iosequencetypes.FrameSet())

    # Output a *new* sequence with the updated frame range.
    out_sequence = iograft.OutputDefinition("sequence",
                                            iosequencetypes.FileSequence())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("set_frame_set", "fileseq")
        node.SetMenuPath("File Sequence")
        node.AddInput(cls.sequence)
        node.AddInput(cls.frame_set)
        node.AddOutput(cls.out_sequence)
        return node

    @staticmethod
    def Create():
        return SetFrameSet()

    def Process(self, data):
        sequence = iograft.GetInput(self.sequence, data)
        frame_set = iograft.GetInput(self.frame_set, data)

        # Create a copy of the file sequence so that the input is
        # not modifed.
        out_sequence = sequence.copy()
        out_sequence.setFrameSet(frame_set)
        iograft.SetOutput(self.out_sequence, data, out_sequence)


def LoadPlugin(plugin):
    node = SetFrameSet.GetDefinition()
    plugin.RegisterNode(node, SetFrameSet.Create)
