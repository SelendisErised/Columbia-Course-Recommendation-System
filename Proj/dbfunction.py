import pymysql

class DatabaseConnection:
    def __init__(self, host, database_user_id, database_user_password, default_scheme):
        self.host = host
        self.database_user_id = database_user_id
        self.database_user_password = database_user_password
        self.default_scheme = default_scheme

    def connection(self):
        conn = pymysql.connect(
        host = self.host,
        user = self.database_user_id, 
        password = self.database_user_password,
        db = self.default_scheme,
        )
        cur = conn.cursor()
        return cur

class SearchFunction:
    def __init__(self, default_scheme, table_name):
        self.database_name = default_scheme
        self.table_name = table_name

    def ambiguous_search(self, string):
        """
        input_type: a string contain search_key to make ambiguous search
        return_type: a string which is a executable MySQL query
        """
        mysql = "select * from {0}.{1} where Course like '%{2}%' or CourseTitle like '%{2}%' or CourseSubtitle like '%{2}%' or Instructor1Name like '%{2}%' or Tag like '%{2}%'".format(self.database_name, self.table_name, string)
        return mysql

    def qualify_search(self, qualify_list):
        """"
        input_type: a list contains all unique key we add to make qualifying search
        return_type: a string which is a executable MySQL query
        """
        check = CheckConstraint()

        mysql = "select * from {0}.{1} where ".format(self.database_name, self.table_name) 

        qul_list = []
        for course in qualify_list:
            qul_list.append("concat(Course, Term) != '{}'".format(course))

        mysql += ' and '.join(qul_list)

        if not check.check_requirement_fulfillment(qualify_list):
            mysql += "and substring(Course, 5, 1) = '6'" 
            
        return mysql

class CheckConstraint:
    def check_time_overlap(self, uid_time_list):
        """
        input_type: a list of tuples in format of (uid, time).
        uid format: 'COMS6156E00120223' -> COMS6516E001 Fall 2022.
        time format: '12@08001000' -> Monday, Tuesday 8:00 AM to 10:00 PM
        return_type: a tuple in format of (if_overlap, data_dict).
        data_dict format: {'Day': [(start_time, end_time, uid), ...], ...}
        """
        data_dict = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': []}
        empty_data_dict = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': []}

        for uid, course_time in uid_time_list:
            assert course_time != ''
            date, specific_time = course_time.split('@')
            interval = (specific_time[0:4], specific_time[4:8], uid)
            for n in range(len(date)):
                data_dict[date[n]].append(interval)

        for date, intervals in data_dict.items():
            if len(intervals) <= 1:
                continue

            intervals.sort(key=lambda x: x[0])

            prev = '0000'
            for interval in intervals:
                if interval[0] < prev:
                    return False, empty_data_dict
                prev = interval[1]
        
        return True, data_dict

    def check_ee_requirement_fulfillment(self, course_list):
        """
        input_type: a list contains all courses in format of 'COMS6156E00120223' -> COMS6516E001 Fall 2022
        return_type: Boolean 
        ['COMS6156E00120223', 'COMS4111E00120221']
        """
        # Rmv duplicate courses
        course_list = list(set([course_list[i][:12] for i in range(len(course_list))]))
        number_of_level6000_course = 0
        number_of_level4000_course = 0
        number_of_ee_course = 0
        check_ee_related = ('ELEN', 'CSEE', 'EECS', 'BLME', 'ECBM', 'EEBM', 'EEME', 'EEOR')

        for course in course_list:
            number_of_level4000_course += (course[4] == '4')
            number_of_level6000_course += (course[4] == '6')
            number_of_ee_course += (course[:4] in check_ee_related)

        return False if number_of_level6000_course < 5 or number_of_ee_course < 5 else True
        # return False if number_of_level4000_course > 5 or number_of_level6000_course < number_of_level4000_course else True
        # return number_of_level4000_course, number_of_level6000_course


if __name__ == "__main__":
    # check_ee_requirement_fulfillment test
    course_list1 = ['COMS6111E00120221', 'COMS4111W00120221', 'ELEN6883E00120221', 'ELEN6883E00120231', 'COMS4112W00120221', 'COMS4705W00120221', 'ECBM4040E00120223']
    # print(CheckConstraint().check_ee_requirement_fulfillment(course_list1))
#         print(SearchFunction('6156_project', 'Course_info').qualify_search(course_list1))

    # check_time_overlap test
    # True case (No overlap, sort)
    uid_course_list1 = [('COMS6111E00120221', '12@08001000'), ('ELEN6885E00120223', '5@08001000'),
                        ('ELEN6883E00120223', '2@10101230')]
    print(CheckConstraint().check_time_overlap(uid_course_list1))
    # False Case (Overlap)
    uid_course_list2 = [('COMS6111E00120221', '12@08001000'), ('ELEN6885E00120223', '5@08001000'),
                        ('ELEN6883E00120223', '2@08001000')]
    print(CheckConstraint().check_time_overlap(uid_course_list2))
