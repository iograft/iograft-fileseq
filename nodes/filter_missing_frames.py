# Copyright 2023 Fabrica Software, LLC

import fileseq
import os

import iograft
import iosequencetypes


class FilterMissingFrames(iograft.Node):
    """
    Given a fileseq.FileSequence, generate a new FileSequence representing
    ONLY the missing frames from the sequence.
    """
    sequence = iograft.InputDefinition("sequence",
                                       iosequencetypes.FileSequence())
    missing_sequence = iograft.OutputDefinition("missing_sequence",
                                                iosequencetypes.FileSequence())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("filter_missing_frames", "fileseq")
        node.SetMenuPath("File Sequence")
        node.AddInput(cls.sequence)
        node.AddOutput(cls.missing_sequence)
        return node

    @staticmethod
    def Create():
        return FilterMissingFrames()

    def Process(self, data):
        sequence = iograft.GetInput(self.sequence, data)
        frame_set = sequence.frameSet()

        # Filter the frames of the sequence to ONLY the frames that are
        # missing and not currently on disk.
        missing_frames = set()
        for index, path in enumerate(sequence):
            if not os.path.exists(path):
                missing_frames.add(frame_set[index])

        # Create a new FrameSet and a new FileSequence
        missing_frame_set = fileseq.FrameSet(missing_frames)
        missing_sequence = sequence.copy()
        missing_sequence.setFrameSet(missing_frame_set)
        iograft.SetOutput(self.missing_sequence, data, missing_sequence)


def LoadPlugin(plugin):
    node = FilterMissingFrames.GetDefinition()
    plugin.RegisterNode(node, FilterMissingFrames.Create)
