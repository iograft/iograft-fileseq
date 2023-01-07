# Copyright 2023 Fabrica Software, LLC

import iograft
import iobasictypes
import iosequencetypes


class EnumerateFrameSet(iograft.Node):
    """
    Given a fileseq.FrameSet object, enumerate a list of the frames in the
    set.
    """
    frame_set = iograft.InputDefinition("frame_set", iosequencetypes.FrameSet())
    frames = iograft.OutputDefinition("frames", iobasictypes.IntList())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("enumerate_frame_set", "fileseq")
        node.SetMenuPath("File Sequence")
        node.AddInput(cls.frame_set)
        node.AddOutput(cls.frames)
        return node

    @staticmethod
    def Create():
        return EnumerateFrameSet()

    def Process(self, data):
        frame_set = iograft.GetInput(self.frame_set, data)

        # Generate the output list of frames.
        frames = list(frame_set)
        iograft.SetOutput(self.frames, data, frames)


def LoadPlugin(plugin):
    node = EnumerateFrameSet.GetDefinition()
    plugin.RegisterNode(node, EnumerateFrameSet.Create)
