# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pytest
import torch

from nemo.collections.asr.data.audio_to_text import TarredAudioToCharDataset
from nemo.collections.asr.parts.features import WaveformFeaturizer


class TestASRDatasets:
    labels = [
        " ",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "'",
    ]

    @pytest.mark.unit
    def test_tarred_dataset(self):
        batch_size = 4
        manifest_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data/tarred_an4/tarred_audio_manifest.json')
        )
        print(f"**********************{manifest_path}")

        featurizer = WaveformFeaturizer()

        # Test braceexpand loading
        tarpath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/tarred_an4/audio_{0..1}.tar'))
        ds_braceexpand = TarredAudioToCharDataset(
            audio_tar_filepaths=tarpath, manifest_filepath=manifest_path, labels=self.labels, featurizer=featurizer
        )
        assert len(ds_braceexpand) == 32
        count = 0
        for _ in ds_braceexpand:
            count += 1
        assert count == 32

        # Test loading via list
        tarpath = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), f'data/asr/tarred_an4/audio_{i}.tar'))
            for i in range(2)
        ]
        ds_list_load = TarredAudioToCharDataset(
            audio_tar_filepaths=tarpath, manifest_filepath=manifest_path, labels=self.labels, featurizer=featurizer
        )
        count = 0
        for _ in ds_braceexpand:
            count += 1
        assert count == 32
