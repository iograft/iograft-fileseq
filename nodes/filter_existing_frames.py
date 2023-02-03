# Copyright 2023 Fabrica Software, LLC

import fileseq
import os

import iograft
import iosequencetypes


class FilterExistingFrames(iograft.Node):
    """
    Given a fileseq.FileSequence, generate a new FileSequence representing
    ONLY the frames that exist on disk.
    """
    sequence = iograft.InputDefinition("sequence",
                                       iosequencetypes.FileSequence())
    existing_sequence = iograft.OutputDefinition("existing_sequence",
                                                iosequencetypes.FileSequence())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("filter_existing_frames", "fileseq")
        node.SetMenuPath("File Sequence")
        node.AddInput(cls.sequence)
        node.AddOutput(cls.existing_sequence)
        return node

    @staticmethod
    def Create():
        return FilterExistingFrames()

    def Process(self, data):
        sequence = iograft.GetInput(self.sequence, data)
        frame_set = sequence.frameSet()

        # Filter the frames of the sequence to ONLY the frames that actually
        # exist on disk.
        existing_frames = set()
        for index, path in enumerate(sequence):
            if os.path.exists(path):
                existing_frames.add(frame_set[index])

        # Create a new FrameSet and a new FileSequence
        existing_frame_set = fileseq.FrameSet(existing_frames)
        existing_sequence = sequence.copy()
        existing_sequence.setFrameSet(existing_frame_set)
        iograft.SetOutput(self.existing_sequence, data, existing_sequence)


def LoadPlugin(plugin):
    node = FilterExistingFrames.GetDefinition()
    plugin.RegisterNode(node, FilterExistingFrames.Create)
