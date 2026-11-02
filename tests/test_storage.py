import importlib.util
import tempfile
import unittest
from pathlib import Path
spec = importlib.util.spec_from_file_location('storage', Path(__file__).parents[1] / 'addon/storage.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Repository = module.Repository

class Tests(unittest.TestCase):
    def test_roundtrip_and_isolation(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            repo = Repository(a)
            key = repo.add('日本語', '段落\n<script>literal</script>')
            repo.save(key, {'paragraph': 1, 'fraction': .4})
            repo.close()
            repo = Repository(a)
            self.assertEqual(len(repo.search('日本')), 1)
            self.assertIn('0.4', repo.get(key)['position'])
            other = Repository(b)
            self.assertEqual(other.search(), [])
            with self.assertRaises(ValueError): repo.add('', 'text')
            with self.assertRaises(ValueError): repo.save(key, {'paragraph': -1, 'fraction': 0})
            repo.close()
            other.close()
