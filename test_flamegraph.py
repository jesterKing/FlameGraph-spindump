#!/usr/bin/env python

import unittest
import flamegraph


class TakeUntilEmptyLineTestCase(unittest.TestCase):
    def test_trivial(self):
        first, rest = flamegraph.take_until_empty_line(["a", "", "b", "c"])
        self.assertEqual(first, ["a"])
        self.assertEqual(rest, ["b", "c"])

    def test_no_rest(self):
        first, rest = flamegraph.take_until_empty_line(["a", "b"])
        self.assertEqual(first, ["a", "b"])
        self.assertIsNone(rest)

    def test_single_line(self):
        first, rest = flamegraph.take_until_empty_line(["a"])
        self.assertEqual(first, ["a"])
        self.assertIsNone(rest)

    def test_few_empty_lines(self):
        first, rest = flamegraph.take_until_empty_line(["a", "", "", "", "b", "c"])
        self.assertEqual(first, ["a"])
        self.assertEqual(rest, ["b", "c"])

    def test_ends_with_empty_line(self):
        first, rest = flamegraph.take_until_empty_line(["a", "b", ""])
        self.assertEqual(first, ["a", "b"])
        self.assertIsNone(rest)


class SplitOnColonTestCase(unittest.TestCase):
    def test_trivial(self):
        actual = flamegraph.split_on_colon(["a: b"])
        self.assertEqual(actual, [("a", "b")])

    def test_real_example(self):
        actual = flamegraph.split_on_colon([
            "PID:             55811",
            "Event:           hang"])
        self.assertEqual(actual, [("PID", "55811"), ("Event", "hang")])


class FrameSampleTestCase(unittest.TestCase):
    def test_height(self):
        parent = flamegraph.FrameSample("parent + 1 (Foo) [0x7fff80004444]", 9)
        child_a = flamegraph.FrameSample("child_a + 1 (Foo) [0x7fff80004444]", 3)
        child_b = flamegraph.FrameSample("child_b + 1 (Foo) [0x7fff80004444]", 4)
        grand_child_b = flamegraph.FrameSample("grand_child_b + 1 (Foo) [0x7fff80004444]", 2)
        parent.add_child_sample(child_a)
        parent.add_child_sample(child_b)
        child_b.add_child_sample(grand_child_b)
        self.assertEqual(parent.height(), 3)
        self.assertEqual(child_a.height(), 1)
        self.assertEqual(child_b.height(), 2)
        self.assertEqual(grand_child_b.height(), 1)

    def test_iteritems(self):
        parent = flamegraph.FrameSample("parent + 1 (Foo) [0x7fff80004444]", 9)
        child_a = flamegraph.FrameSample("child_a + 1 (Foo) [0x7fff80004444]", 3)
        child_b = flamegraph.FrameSample("child_b + 1 (Foo) [0x7fff80004444]", 4)
        grand_child_b = flamegraph.FrameSample("grand_child_b + 1 (Foo) [0x7fff80004444]", 2)
        parent.add_child_sample(child_a)
        parent.add_child_sample(child_b)
        child_b.add_child_sample(grand_child_b)
        actual_items = [(frame.frame, start, depth) for frame, start, depth in parent.iteritems()]
        expected_items = [("parent + 1 (Foo) [0x7fff80004444]", 0, 0),
                          ("child_a + 1 (Foo) [0x7fff80004444]", 0, 1),
                          ("child_b + 1 (Foo) [0x7fff80004444]", 3, 1),
                          ("grand_child_b + 1 (Foo) [0x7fff80004444]", 3, 2)]
        self.assertEqual(actual_items, expected_items)

if __name__ == '__main__':
    unittest.main()
