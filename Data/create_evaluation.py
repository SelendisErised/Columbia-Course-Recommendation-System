import pandas as pd
import numpy as np
import os


COURSE_VALUATE_PATH = './course_evaluation.csv'


def main():
    df = pd.DataFrame(pd.read_csv('course.csv'))
    df = df.drop(columns=['CourseTitle', 'CourseSubtitle', 'CallNumber',
                          'Term', 'NumFixedUnits', 'Time', 'Location', 'Tag'])

    df['Course'] = df['Course'].map(lambda string: string[0:8])
    df.loc[284] = ['ELEN6882', 'Xiaodong Wang']
    df.loc[313] = ['COMS4705', 'BENAJIBA, YASSINE']
    df = df.drop_duplicates()

    num = len(df['Course'])
    df['Workload'], df['Accessibility'] = np.random.randint(1, 6, num), np.random.randint(1, 6, num)
    df['Delivery'], df['Difficulty'] = np.random.randint(1, 6, num), np.random.randint(1, 6, num)
    # print(df.info())

    if not os.path.exists(COURSE_VALUATE_PATH):
        df.to_csv(COURSE_VALUATE_PATH, index=None)
        df_new = pd.DataFrame(pd.read_csv(COURSE_VALUATE_PATH))
        print(df_new.info())
    else:
        df_new = pd.DataFrame(pd.read_csv(COURSE_VALUATE_PATH))
        print(df_new.info())


if __name__ == '__main__':
    main()