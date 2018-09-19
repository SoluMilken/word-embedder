from unittest import TestCase
from os.path import abspath, dirname, join

import numpy as np

from ..fasttext_light import FastTextLight
from .test_fasttext import FastTextTestTemplate

ROOT_DIR = dirname(abspath(__file__))


class FastTextLightTestCase(FastTextTestTemplate, TestCase):

    def setUp(self):
        self.embedder = FastTextLight(
            path=join(ROOT_DIR, 'data/fasttext.vec'))
        self.words = ['薄餡', '隼興', 'gb', 'en', 'Alvin']
        self.vectors = np.array(
            [
                [0.1, 0.2, 0.3],
                [0.4, 0.5, 0.6],
                [0.7, 0.8, 0.9],
                [0.11, 0.12, 0.13],
                [0.14, 0.15, 0.16],
            ],
        ).astype(np.float32)

    def test_correctly_create_instance(self):
        self.assertEqual(
            set(['_path', '_is_built']),
            set(self.embedder.__dict__.keys()),
        )
        self.assertEqual(
            join(ROOT_DIR, 'data/fasttext.vec'),
            self.embedder._path,
        )
        self.assertFalse(self.embedder._is_built)

    def test_build(self):
        self.embedder.build()
        self.assertTrue(self.embedder._is_built)
        self.assertEqual(
            set(['_path', '_is_built',
                 '_embedding_size', '_vocab_size',
                 '_vocab_list', '_byte_pos',
                 '_vloader']),
            set(self.embedder.__dict__.keys()),
        )
        self.assertEqual(
            ['薄餡', '隼興', 'gb', 'en', 'Alvin'],
            self.embedder._vocab_list,
        )