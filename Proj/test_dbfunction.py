import unittest
from dbfunction import DatabaseConnection, SearchFunction, CheckConstraint

check = CheckConstraint()

class TestCheckConstraint(unittest.TestCase):
    def setUp(self):
        pass

    def test_check_time_overlap(self):
        time_list1 = ['1@08001000', '13@09301130', '2@10001130']
        time_list2 = ['1@08001000', '13@10301130', '2@10001130', '45@16001730']
        time_list3 = ['1@08001000']
        time_list4 = ['1@08001000', '12@11301400', '3@11001200', '45@16001750']

        self.assertEqual(check.check_time_overlap(time_list1), False)
        self.assertEqual(check.check_time_overlap(time_list2), True)
        self.assertEqual(check.check_time_overlap(time_list3), True)
        self.assertEqual(check.check_time_overlap(time_list4), True)

    def test_check_requirement_fulfillment(self):
        course_list1 = ['COMS6156E00120223', 'COMS4321E00120223', 'EECS4126E00120223', 'ELEN4702E00120223', 'ECMB4040E00120223', 'ELEN4902E00120223']
        course_list2 = ['COMS6156E00120223', 'COMS4321E00120223']
        course_list3 = ['COMS6156E00120223']
        course_list4 = ['COMS4256E00120223']

        self.assertEqual(check.check_requirement_fulfillment(course_list1), False)
        self.assertEqual(check.check_requirement_fulfillment(course_list2), True)
        self.assertEqual(check.check_requirement_fulfillment(course_list3), True)
        self.assertEqual(check.check_requirement_fulfillment(course_list4), False)

class TestSearchFunction(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_ambiguous_search(self):
        pass

    def test_qualify_search(self):
        # course_list1 = ['COMS6111E00120221', 'COMS4111W00120221', 'ELEN6883E00120221', 'ELEN6771E00120231', 'COMS4112W00120221', 'COMS4705W00120221', 'ECBM4040E00120223']
        pass


if __name__ == '__main__':
    unittest.main()