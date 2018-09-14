from unittest import TestCase
from os.path import abspath, dirname, join

import numpy as np

from ..fasttext import FastText
from ..oov_error import OOVError


ROOT_DIR = dirname(abspath(__file__))


class FastTextTestCase(TestCase):

    def setUp(self):
        self.embedder = FastText(
            path=join(ROOT_DIR, 'data/fasttext.vec'))

    def test_correctly_create_instance(self):
        self.assertEqual(
            set(['_embedding_size', '_vocab_size',
                 '_word_vectors', '_vocab_list']),
            set(self.embedder.__dict__.keys()),
        )
        self.assertEqual(
            ['薄餡', '隼興', 'gb', 'en', 'Alvin'],
            self.embedder._vocab_list,
        )
        self.assertEqual(
            np.array(
                [
                    [0.1, 0.2, 0.3],
                    [0.4, 0.5, 0.6],
                    [0.7, 0.8, 0.9],
                    [0.11, 0.12, 0.13],
                    [0.14, 0.15, 0.16],
                ],
            ).astype(np.float32).tolist(),
            self.embedder._word_vectors.tolist(),
        )

    def test_vocab_size(self):
        self.assertEqual(5, self.embedder.n_vocab)

    def test_n_dim(self):
        self.assertEqual(3, self.embedder.n_dim)
        self.assertEqual(
            self.embedder._embedding_size,
            self.embedder.n_dim,
        )

    def test_get_index(self):
        self.assertEqual(2, self.embedder.get_index('gb'))

    def test_get_index_oov(self):
        self.assertEqual(-1, self.embedder.get_index('haha'))

    def test_get_word(self):
        self.assertEqual('薄餡', self.embedder.get_word(0))

    def test_get_word_oov(self):
        self.assertIsNone(self.embedder.get_word(10))

    def test_getitem_string(self):
        self.assertEqual(
            np.array([0.14, 0.15, 0.16]).astype(np.float32).tolist(),
            self.embedder['Alvin'].tolist(),
        )

    def test_getitem_int(self):
        self.assertEqual(
            np.array([0.14, 0.15, 0.16]).astype(np.float32).tolist(),
            self.embedder[4].tolist(),
        )

    def test_getitem_string_oov(self):
        with self.assertRaises(OOVError):
            self.embedder['kerker']

    def test_getitem_int_oov(self):
        with self.assertRaises(OOVError):
            self.embedder[100]

    def test_getitem_wrong_type(self):
        with self.assertRaises(TypeError):
            self.embedder[12.3]
            self.embedder[[123]]
