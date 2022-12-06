import pandas as pd
import numpy as np
import os


COURSE_VALUATE_PATH = './course_evaluation.csv'


def main():
    df = pd.DataFrame(pd.read_csv('data_all_raw.csv'))
    df = df.drop(columns=['CourseTitle', 'CallNumber',
                          'Term', 'NumFixedUnits', 'Time', 'Location', 'Tag'])

    df['Course'] = df['Course'].map(lambda string: string[0:8])
    df = df.drop_duplicates()
    df.loc[1] = ['COMS4111', 'INTRODUCTION TO DATABASES', 'FERGUSON, DONALD F']
    df.loc[284] = ['ELEN6882', 'TOPICS IN SIGNAL PROCESSI', 'WANG, XIAODONG']
    df = df.drop_duplicates()
    print(df.info())

    num = len(df['Course'])
    df['Workload'], df['Accessibility'] = 2 * np.random.random(num) + 3, 2 * np.random.random(num) + 3
    df['Delivery'], df['Difficulty'] = 2 * np.random.random(num) + 3, 2 * np.random.random(num) + 3
    df['Cnt'] = np.random.randint(200, 501, num)
    print(df.info())


    df.to_csv(COURSE_VALUATE_PATH, index=None)
    df_new = pd.DataFrame(pd.read_csv(COURSE_VALUATE_PATH))
    print(df_new.info())


if __name__ == '__main__':
    main()