#!/usr/bin/env python

import unittest
import sys, os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
import jsoncompare

class TestJSONCompare(unittest.TestCase):

    def setUp(self):
        pass

    def test_list_of_hashes(self):
        a = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        b = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        self.assertTrue(jsoncompare.are_same(a, b)[0])

    def test_list_of_hashes_unordered(self):
        a = [
            {"wtf1": "omg1"},
            {"wtf": "omg"}
        ]
        b = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        self.assertTrue(jsoncompare.are_same(a, b, True)[0])

    def test_list_of_hashes_unordered_fail(self):
        a = [
            {"wtf1": "omg1"},
            {"wtf": "omg"}
        ]
        b = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        self.assertFalse(jsoncompare.are_same(a, b)[0])

    def test_list_of_hashes_ignore_key(self):
        a = [
            {"wtf1": "omg1"},
            {"wtf2": "omg"}
        ]
        b = [
            {"wtf1": "omg1"},
            {"wtf2": "omg3"}
        ]
        self.assertTrue(jsoncompare.are_same(a, b, True, ["wtf2"])[0])

    def test_hash_list_of_hashes_unordered(self):
        a = {
            "wtf": [
                {"wtf1": "omg1"},
                {"wtf": "omg"}
            ]
        }
        b = {
            "wtf": [
                {"wtf": "omg"},
                {"wtf1": "omg1"}
            ]
        }
        self.assertTrue(jsoncompare.are_same(a, b, True)[0])

    def test_hash_list_of_hashes_unordered_fail(self):
        a = {
            "wtf": [
                {"wtf1": "omg1"},
                {"wtf": "omg"}
            ]
        }
        b = {
            "wtf": [
                {"wtf": "omg"},
                {"wtf1": "omg1"}
            ]
        }
        self.assertFalse(jsoncompare.are_same(a, b)[0])

    def test_hash_vs_list_fail(self):
        a = {
            "wtf": [
                {"wtf1": "omg1"},
                {"wtf": "omg"}
            ]
        }
        b = [
            {"wtf1": "omg1"}
        ]
        self.assertFalse(jsoncompare.are_same(a, b)[0])

    def test_list_vs_hash_fail(self):
        a = [
            {"wtf1": "omg1"}
        ]
        b = {
            "wtf": [
                {"wtf1": "omg1"},
                {"wtf": "omg"}
            ]
        }
        self.assertFalse(jsoncompare.are_same(a, b)[0])

    def test_hash_vs_list_size_fail(self):
        a = {
            "wtf": [
                {"wtf1": "omg1"},
                {"wtf": "omg"}
            ]
        }
        b = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        self.assertFalse(jsoncompare.are_same(a, b)[0])

    def test_nested_list_order_sensitivity_false(self):
        a = {
            "failureReason" : "Invalid request entity",
            "fieldValidationErrors" : [
                {
                    "field" : "Catalog.catalogOwner",
                    "reason" : "may not be null"
                },
                {
                    "field" : "Catalog.name",
                    "reason" : "may not be null"
                }
            ]
        }
        b = {
            "failureReason" : "Invalid request entity",
            "fieldValidationErrors" : [
                {
                    "field" : "Catalog.name",
                    "reason" : "may not be null"
                },
                {
                    "field" : "Catalog.catalogOwner",
                    "reason" : "may not be null"
                }
            ]
        }
        self.assertFalse(jsoncompare.are_same(a, b)[0])

    def test_nested_list_order_sensitivity(self):
        a = {
            "failureReason" : "Invalid request entity",
            "fieldValidationErrors" : [
                {
                    "field" : "Catalog.catalogOwner",
                    "reason" : "may not be null"
                },
                {
                    "field" : "Catalog.name",
                    "reason" : "may not be null"
                }
            ]
        }
        b = {
            "failureReason" : "Invalid request entity",
            "fieldValidationErrors" : [
                {
                    "field" : "Catalog.name",
                    "reason" : "may not be null"
                },
                {
                    "field" : "Catalog.catalogOwner",
                    "reason" : "may not be null"
                }
            ]
        }
        self.assertTrue(jsoncompare.are_same(a, b, True)[0])

    def test_inner_val_sensitivity_false(self):
        a = {
            "failureReason" : "Invalid request entity",
            "fieldValidationErrors" : [
                {
                    "field" : "Catalog.catalogOwner",
                    "reason" : "may not be smelly"
                },
                {
                    "field" : "Catalog.name",
                    "reason" : "may not be null"
                }
            ]
        }
        b = {
            "failureReason" : "Invalid request entity",
            "fieldValidationErrors" : [
                {
                    "field" : "Catalog.catalogOwner",
                    "reason" : "may not be null"
                },
                {
                    "field" : "Catalog.name",
                    "reason" : "may not be null"
                }
            ]
        }
        self.assertFalse(jsoncompare.are_same(a, b, True)[0])

    def test_nested_list_order_inner_val_sensitivity_false(self):
        a = {
            "failureReason" : "Invalid request entity",
            "fieldValidationErrors" : [
                {
                    "field" : "Catalog.catalogOwner",
                    "reason" : "may not be smelly"
                },
                {
                    "field" : "Catalog.name",
                    "reason" : "may not be null"
                }
            ]
        }
        b = {
            "failureReason" : "Invalid request entity",
            "fieldValidationErrors" : [
                {
                    "field" : "Catalog.name",
                    "reason" : "may not be null"
                },
                {
                    "field" : "Catalog.catalogOwner",
                    "reason" : "may not be null"
                }
            ]
        }
        self.assertFalse(jsoncompare.are_same(a, b, True)[0])

    def test_giant_json_ignores_reordering(self):
        a = open("testing-data/jsonbloba.json").read()
        b = open("testing-data/jsonblobb.json").read()
        self.assertTrue(jsoncompare.json_are_same(a, b, True)[0])


    def test_giant_json_finds_reordering(self):
        a = open("testing-data/jsonbloba.json").read()
        b = open("testing-data/jsonblobb.json").read()
        self.assertFalse(jsoncompare.json_are_same(a, b)[0])

    # Test two json that are same size and keys/values match
    def test_contains_same_size(self):
        actual = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        expected = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        self.assertTrue(jsoncompare.contains(expected, actual)[0])
        #same, error_message = jsoncompare.contains(expected, actual)
        #assert same, error_message

    # Test two json that are same size and keys/values match with ignore_order
    def test_contains_same_size2(self):
        actual = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        expected = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        self.assertTrue(jsoncompare.contains(expected, actual, True)[0])

    # Test two json that are same size but values do not match
    def test_contains_same_size3(self):
        actual = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        expected = [
            {"wtf": "omg"},
            {"wtf1": "omg999999"}
        ]
        self.assertFalse(jsoncompare.contains(expected, actual)[0])
        #same, error_message = jsoncompare.contains(expected, actual)
        #assert same, error_message

    # Test two json that are same size but keys do not match
    def test_contains_same_size4(self):
        actual = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        expected = [
            {"wtf": "omg"},
            {"wtf999": "omg1"}
        ]
        self.assertFalse(jsoncompare.contains(expected, actual)[0])
        #same, error_message = jsoncompare.contains(expected, actual)
        #assert same, error_message
	
    # Test two json where Actual is larger - it can (potentialy) contain all of the expected attributes
    def test_contains_actual_bigger(self):
        actual = [
            {"wtf": "omg"},
            {"wtf1": "omg1"},
            {"wtf3": "omg3"}
        ]
        expected = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        self.assertTrue(jsoncompare.contains(expected, actual)[0])

    # Test two json where Actual is smaller - it can NOT contain all of expected attributes
    def test_contains_actual_smaller(self):
        actual = [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
        expected = [
            {"wtf": "omg"},
            {"wtf1": "omg1"},
            {"wtf2": "omg2"}
        ]
        self.assertFalse(jsoncompare.contains(expected, actual)[0])


if __name__ == '__main__':
    unittest.main()
