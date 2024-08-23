import unittest

from ..helpers.calendar_entries import count_slots_available

class TestCountSlotsAvailable(unittest.TestCase):

    def test_count_one_when_full(self):
        new_members = 'Agatha C.,William T.,Robin H.,FREE'
        old_members = 'Robin H.,William T.,Agatha C.,Donald D.'
        self.assertEqual(count_slots_available(new_members, old_members), 1)

    def test_count_one_when_some_cancelled(self):
        new_members = 'William T.,Robin H.,FREE'
        old_members = 'Robin H.,William T.,Agatha C.,CANCELLED'
        self.assertEqual(count_slots_available(new_members, old_members), 1)

    def test_count_one_when_more_free(self):
        new_members = 'Donald D.,FREE,FREE,FREE'
        old_members = 'FREE,FREE,Agatha C.,Donald D.'
        self.assertEqual(count_slots_available(new_members, old_members), 1)

    def test_count_zero_when_some_reserved(self):
        new_members = 'Agatha C.,William T.,Robin H.,Donald D.'
        old_members = 'Robin H.,William T.,Agatha C.,FREE'
        self.assertEqual(count_slots_available(new_members, old_members), 0)

    def test_count_zero_when_members_changed(self):
        new_members = 'Michael J.,Femke B.,Isina I.,Michael P.'
        old_members = 'Robin H.,William T.,Agatha C.,Donald D.'
        self.assertEqual(count_slots_available(new_members, old_members), 0)

    def test_count_two_when_more_free(self):
        new_members = 'FREE,FREE,FREE,FREE'
        old_members = 'Robin H.,William T.,FREE,FREE'
        self.assertEqual(count_slots_available(new_members, old_members), 2)
