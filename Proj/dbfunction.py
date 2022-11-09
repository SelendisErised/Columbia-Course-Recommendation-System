import pymysql
import json

class Tools:
    def substring(self, course_id):
        return course_id[0:8]

    def print_time(self, course_string):
        """
        Interpret abstract time info to readable time info
        input_type: a string which contains the time info with format like '15@10001200'
            before '@': 1, 5 represent the dates
            behind '@' the first 4 digit represents the starting time and the other four represent the ending time, 
                    all in 24-hour clock
        return_type: a string which is readable time info
        """

        course_time = ''
        tinydict = {'1': 'Mon ', '2': 'Tu ', '3': 'Wed ', '4': 'Thu ', '5': 'Fri ', '6': 'Sat ', '7': 'Sun '}

        for date in course_string.split('@')[0]:
            course_time += tinydict[date] 
        
        sub_time = course_string[len(course_string) - 8 : len(course_string)]
        
        if (int(sub_time[0:2])) < 12:
            zone1 = 'AM'
        else:
            zone1 = 'PM'

        if (int(sub_time[4:6])) < 12:
            zone2 = 'AM'
        else:
            zone2 = 'PM'

        course_time = course_time + sub_time[0:2] + ':' + sub_time[2:4] + zone1 + '-' + sub_time[4:6] + ':' + sub_time[6:8] + zone2

        return course_time


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

class SearchFunction(Tools):
    def __init__(self, default_scheme, table_name, cur):
        self.database_name = default_scheme
        self.table_name = table_name
        self.db_cursor = cur
        self.current_term = '20223'

    def ambiguous_search(self, string):
        """
        input_type: a string contain search_key to make ambiguous search
        return_type: a json format file which is the returned data
        """
        mysql = "select * from {0}.{1} where (Course like '%{2}%' or CourseTitle like '%{2}%' or CourseSubtitle like '%{2}%' or Instructor1Name like '%{2}%' or Tag like '%{2}%') and Term = '{3}' ".format(self.database_name, self.table_name, string, self.current_term)
        self.db_cursor.execute(mysql)
        query_output = self.db_cursor.fetchall()
        json_out = json.dumps([{'Course': course[2], 
                        'Number': course[0], 
                        'Term': course[4], 
                        'Instructor': str.title(course[5]) if course[5] else None, 
                        'Time': self.print_time(course[7]), 
                        'Location': course[8]} for course in query_output])

        json_out = json.loads(json_out)
        
        return json_out

    def qualify_search(self, qualify_list):
        """"
        input_type: a list contains all unique key we add to make qualifying search
        return_type: a json format file which is the returned data
        """

        mysql = "select * from {0}.{1} where ".format(self.database_name, self.table_name) 
        qul_list = []
        for course in qualify_list:
            qul_list.append("concat(Course, Term) != '{}'".format(course))
        mysql += ' and '.join(qul_list) if qul_list else ''
        mysql += " and Term = {}".format(self.current_term)
        self.db_cursor.execute(mysql)
        query_tuple = self.db_cursor.fetchall()

        uid_time_list = []
        for registered_course in qualify_list:
            if registered_course[-5:] != self.current_term:
                continue
            mysql = "select * from {0}.{1} where concat(Course, Term) = '{2}'".format(self.database_name, self.table_name, registered_course)
            self.db_cursor.execute(mysql)
            course_time = self.db_cursor.fetchall()[0][7]
            uid_time_list.append((registered_course, course_time))

        _, time_dict = CheckConstraint().generate_time_dict(uid_time_list)

        course_list = []

        for course_available in query_tuple:
            
            course_number, time = course_available[0], course_available[7]
            dates, start_time, end_time = time.split('@')[0], time.split('@')[1][:4], time.split('@')[1][4:]
            
            flag = True
            
            for date in dates:
                if not flag:
                    break

                check_course_list = time_dict[date]
                
                for check_course in check_course_list:
                    if not CheckConstraint().check_time_overlap(start_time, end_time, check_course[0], check_course[1]):
                        flag = False
                    
            if flag:
                course_list.append(course_available)
                
        json_data = json.dumps([{'Course': course[2], 
                                 'Number': course[0], 
                                 'Term': course[4], 
                                 'Instructor': str.title(course[5]) if course[5] else None, 
                                 'Time': self.print_time(course[7]), 
                                 'Location': course[8], 
                                 'Tag': course[9]} for course in course_list], indent=4)
        
        json_out = json.loads(json_data)
    
        return json_out


class CheckConstraint:
    def check_time_overlap(self, start_time1, end_time1, start_time2, end_time2):
        """"
        Check if two courses overlap in time
        input_type: 
            start_time1: a string which is the starting time course1 
            end_time1: a string which is the ending time course1 
            start_time2: a string which is the starting time course2
            end_time2: a string which is the ending time course2
        return_type: Boolean
        """
        
        if end_time1 <= start_time2:
            return True
        
        elif end_time2 <= start_time1:
            return True
        
        else:
            return False

    def generate_time_dict(self, uid_time_list):
        """
        input_type: a list of tuples in format of (uid, time).
            uid format: 'COMS6156E00120223' -> COMS6516E001 Fall 2022.
            time format: '12@08001000' -> Monday, Tuesday 8:00 AM to 10:00 PM
        return_type: (Boolean, a tuple in format of (if_overlap, data_dict))
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
        Check if registered course satisfy the department requirement
        input_type: a list contains all courses in format of 'COMS6156E00120223' -> COMS6516E001 Fall 2022
            Example input format: ['COMS6156E00120223', 'COMS4111E00120221']
        return_type: Boolean 
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


# if __name__ == "__main__":
#     # check_ee_requirement_fulfillment test
#     course_list1 = ['COMS6111E00120221', 'ELEN6885E00120223', 'COMS4705WH0120223', 'COMS6156E00120223']

#     host = 'localhost'
#     database_user_id = 'root'
#     database_user_password = 'hx687099'
#     default_scheme = '6156_project'
#     table_name = 'Course_info'

#     db = DatabaseConnection(host, database_user_id, database_user_password, default_scheme)
#     cur = db.connection()

#     search_engine = SearchFunction(default_scheme, 'Course_info', cur)
#     # print(search_engine.ambiguous_search('6885'))
#     res = search_engine.qualify_search(course_list1)
#     print(res, len(res))