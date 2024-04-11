import os
import pandas as pd

from src.pre_processing import merge_columns, sum_merge_strategy, zero_nan_strategy, mean_merge_strategy, \
    mode_nan_strategy, histogram_plot
from src.pre_processing.macros import (
    column_groups,
    DATA_PATH,
    DATA_SPLIT_PATH,
    ORIGINAL_DATASET_NAME,
)


def main():

    # Loading student questionnaire
    df = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "principal_questionnaire.csv"), low_memory=False
    )
    df = df.set_index("id_student")

    # Load identifiers and change float columns to int
    ids = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "identifiers.csv"), low_memory=False
    )
    ids = ids.set_index("id_student")
    int_identifiers = [col for col in ids.columns if col not in ["id_class_group"]]
    ids[int_identifiers] = ids[int_identifiers].astype("Int64")

    ############################################################################
    # Delete rows with all NaN values (823 rows)
    ############################################################################
    nan_rows = df.isnull().all(axis=1)
    df = df[~nan_rows]

    ############################################################################
    # Delete rows with all NaN values but island, capital_island and public_private (7227 rows)
    ############################################################################
    nan_rows = df.drop(columns=["island", "capital_island", "public_private"]).isnull().all(axis=1)
    df = df[~nan_rows]

    ############################################################################
    # Merge from d16an to d16fn (values from 0 to 2000).
    # Merge function: sum.
    # Treat missing values as 0.
    # Drop columns after merging.
    # d16an: School resources. Available computers
    # d16bn: School resources. Available computers to students
    # d16cn: School resources. Available computers to teachers
    # d16dn: School resources. Computers for the administrative management of the school
    # d16en: School resources. Tablets/laptops available to students
    # d16fn: School resources. Interactive digital whiteboards or touch screens in classrooms
    ############################################################################

    d16_columns = [f"d16{n}n" for n in "abcdef"]
    df = merge_columns(df, d16_columns, sum_merge_strategy, zero_nan_strategy, "school_resources")

    ############################################################################
    # Merge from d17a to d17h (values from 1 to 4).
    # Merge function: mean.
    # Treat missing values as mode.
    # Drop columns after merging.
    # d17a: Factors that limit the effectiveness of my management. Lack of budget and resources
    # d17b: Factors that limit the effectiveness of my management. Lack of attendance of the teachers
    # d17c: Factors that limit the effectiveness of my management. Lack of participation and support of families
    # d17d: Factors that limit the effectiveness of my management. Lack of teacher training plan in my school for teachers
    # d17e: Factors that limit the effectiveness of my management. Lack of opportunities/support for professional development of the management team
    # d17f: Factors that limit the effectiveness of my management. Lack of agility to cover teacher absences
    # d17g: Factors that limit the effectiveness of my management. Lack of coordination between members of the management team
    # d17h: Factors that limit the effectiveness of my management. Lack of autonomy to make decisions
    ############################################################################

    d17_columns = [f"d17{n}" for n in "abcdefgh"]
    df = merge_columns(df, d17_columns, mean_merge_strategy, mode_nan_strategy, "factors_limiting_effectiveness")

    ############################################################################
    # Merge from d18a to d18n (values from 1 to 4).
    # Merge function: mean.
    # Treat missing values as mode.
    # Drop columns after merging.
    # d18a: It is an inconvenience in your school: Lack of good/qualified teachers
    # d18b: It is an inconvenience in your school: Lack of teachers trained to teach students with special educational needs
    # d18c: It is an inconvenience in your school: Lack or inadequate teaching material
    # d18d: It is an inconvenience in your school: Lack or inadequacy of technological devices for teaching
    # d18e: It is an inconvenience in your school: Poor internet connection
    # d18f: It is an inconvenience in your school: Lack or inadequacy of software for teaching
    # d18g: It is an inconvenience in your school: Lack or inadequacy of library materials
    # d18h: It is an inconvenience in your school: Lack of support teachers
    # d18i: It is an inconvenience in your school: Lack of administrative staff
    # d18j: It is an inconvenience in your school: Lack of adequate infrastructure
    # d18k: It is an inconvenience in your school: Lack of teacher collaboration
    # d18l: It is an inconvenience in your school: Lack of collaboration from families
    # d18m: It is an inconvenience in your school: Administrative bureaucracy
    # d18n: It is an inconvenience in your school: Lack of computers in the classroom or for students.
    ############################################################################

    d18_columns = [f"d18{n}" for n in "abcdefghijklmn"]
    df = merge_columns(df, d18_columns, mean_merge_strategy, mode_nan_strategy, "inconveniences")

    ############################################################################
    # Merge from d19a to d19r (values from 1 to 4).
    # Merge function: sum.
    # Treat missing values as 0.
    # Drop columns after merging.
    # d19a: It is a problem in your school because of the students: Arriving late to the school
    # d19b: It is a problem in your school because of the students: Absenteeism (unexcused absences)
    # d19c: It is a problem in your school because of the students: Disruption of order in class
    # d19d: It is a problem in your school because of the students: Vandalism and theft
    # d19e: It is a problem in your school because of the students: Inappropriate or profanity language
    # d19f: It is a problem in your school because of the students: Intimidation or insults between students or another type of bullying
    # d19g: It is a problem in your school because of the students: Physical aggressions between students
    # d19h: It is a problem in your school because of the students: Lack of respect to teachers
    # d19i: It is a problem in your school because of the students: Intimidation or insults to the teachers or staff of the school
    # d19j: It is a problem in your school because of the teachers: Arriving late to the school
    # d19k: It is a problem in your school because of the teachers: absenteeism (unexcused absences)
    # d19l: It is a problem in your school because of the teachers: Lack of respect towards the students
    # d19m: It is a problem in your school because of the teachers: Lack of respect between teachers
    # d19n: It is a problem in your school because of the teachers: Discrimination based on sex
    # d19o: It is a problem in your school because of the families: Lack of collaboration with the school
    # d19p: It is a problem in your school because of the families: Criticism and opposition to the rules of the school
    # d19q: It is a problem in your school because of the families: Lack of respect towards the teachers and staff of the school
    # d19r: It is a problem in your school because of the families: Lack of respect or discrimination towards other families
    ############################################################################

    d19_columns = [f"d19{n}" for n in "abcdefghijklmnopqr"]
    df = merge_columns(df, d19_columns, mean_merge_strategy, mode_nan_strategy, "problems")

    ############################################################################
    # Merge from d20a to d20l (values from 1 to 4).
    # Merge function: mean.
    # Treat missing values as mode.
    # Drop columns after merging.
    # d20a: To what extent does the management of the school: Helps to establish good relations between teachers
    # d20b: To what extent does the management of the school: Take into account the opinions of the teaching staff
    # d20c: To what extent does the management of the school: Stimulate teachers to develop innovative ideas
    # d20d: To what extent does the management of the school: Create a strong sense of identity in the community with the objectives of the school
    # d20e: To what extent does the management of the school: Promote teamwork among teachers
    # d20f: To what extent does the management of the school: Promotes the maximum use of capacities and teacher knowledge
    # d20g: To what extent does the management of the school: Generates procedures for teacher training courses
    # d20h: To what extent does the management of the school: Uses student educational outcomes/achievement to set school goals
    # d20i: To what extent does the management of the school: Checks that the work of teachers is in accordance with the objectives of the school
    # d20j: To what extent does the management of the school: Encourage that teaching practice is based on recent research developments
    # d20k: To what extent does the management of the school: Follow up on disruptive problems in the classrooms
    # d20l: To what extent does the management of the school: Discuss the educational objectives of the school with teachers
    ############################################################################

    d20_columns = [f"d20{n}" for n in "abcdefghijkl"]
    df = merge_columns(df, d20_columns, mean_merge_strategy, mode_nan_strategy, "management")

    ############################################################################
    # Merge from d21a to d21f (values from 1 to 4).
    # Merge function: mean.
    # Treat missing values as mode.
    # Drop columns after merging.
    # d21a: Satisfaction level: With teachers
    # d21b: Satisfaction level: With students
    # d21c: Satisfaction level: With families
    # d21d: Satisfaction level: With CEP associates
    # d21e: Satisfaction level: With guidance teams (EOEP)
    # d21f: Satisfaction level: With educational inspection
    ############################################################################

    d21_columns = [f"d21{n}" for n in "abcdef"]
    df = merge_columns(df, d21_columns, mean_merge_strategy, mode_nan_strategy, "satisfaction")

    ############################################################################
    # Drop columns with all missing values
    ############################################################################

    df.dropna(axis=1, how="all", inplace=True)

    ############################################################################
    # Select columns with just one value other than NaN and fill it with value 2
    # These are columns from d301 to d308
    ############################################################################

    one_value_columns = df.columns[df.nunique() == 1]
    df[one_value_columns] = df[one_value_columns].fillna(2)

    ############################################################################
    # Column d1 (sex) has:
    # - 26.224 1 (male)
    # - 40.816 2 (female)
    # - 8.767 (NaN)
    # Fill NaN values with 0 (unknown)
    df["d1"].fillna(0, inplace=True)
    ############################################################################
    # Column d2n (age) has 354 NaN values
    # Fill NaN values with the mode
    df["d2n"].fillna(df["d2n"].mode()[0], inplace=True)
    ############################################################################
    # Column d3n (year of teaching experience) has 601 NaN values
    # Considering that the minimum is 2 could be reasonable to assume that even 0 years is a valid value.
    # However, the histogram of the column shows a simil double Gaussian distribution, with 30 as the mode.
    # Solution: create bins of 5 years and fill the NaN values with the mode (max is 50 years)
    bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    df["d3n"] = pd.cut(df["d3n"], bins, labels=bins[1:])
    df["d3n"].fillna(df["d3n"].mode()[0], inplace=True)
    ############################################################################
    # Column d4n (years in the current school) has 407 NaN values
    # Column d5n (years of experience as a principal) has 741 NaN values
    # Column d6n (years of experience as a principal in the current school) has 420 NaN values
    #
    # For sure d4n >= d6n!
    # But 476 rows have d4n < d6n -> discard them
    ############################################################################
    df = df[df["d4n"] >= df["d6n"]]
    ############################################################################
    # Still 364 NaN values in d5n remain
    # d5n should be greater than d6n
    # But 2117 rows have d5n < d6n -> discard them
    ############################################################################
    df = df[df["d5n"] >= df["d6n"]]
    ############################################################################


    


    ############################################################################
    # The remaining NaN values are filled with 0
    ############################################################################

    df.fillna(0, inplace=True)

    # Merge identifiers and student questionnaire
    df = pd.merge(ids, df, left_index=True, right_index=True)


if __name__ == "__main__":
    main()
