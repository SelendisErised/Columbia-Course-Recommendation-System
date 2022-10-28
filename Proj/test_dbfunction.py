import unittest
from dbfunction import DatabaseConnection, SearchFunction, CheckConstraint

class TestCheckConstraint(unittest.TestCase):
    def setUp(self):
        pass

    def test_check_time_overlap(self):
        time_list1 = ['1@08001000', '13@09301130', '2@10001130']
        time_list2 = ['1@08001000', '13@10301130', '2@10001130', '45@16001730']
        time_list3 = ['1@08001000']
        time_list4 = ['1@08001000', '12@11301400', '3@11001200', '45@16001750']

        check = CheckConstraint()

        self.assertEqual(check.check_time_overlap(time_list1), False)
        self.assertEqual(check.check_time_overlap(time_list2), True)
        self.assertEqual(check.check_time_overlap(time_list3), True)
        self.assertEqual(check.check_time_overlap(time_list4), True)

    def test_check_requirement_fulfillment(self):
        pass

if __name__ == '__main__':
    unittest.main()