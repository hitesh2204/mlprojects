import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.imputer import SimpleImputer
from sklearn.pipeline import Pipeline
from skelarn.preprocessing import OneHotEncoder,StadardScaler

from src.exception import CustomExeception
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.Data_Transformation_Cofig=DataTransformationConfig()

    def get_data_transformaer_obj(self):
        '''
        This function is responsible for data transformation.
        '''
        try:
            numerical_feature=['reading_score','writing_score']
            categorical_feature=['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']

            num_pipeline=Pipeline(
                steps=[
                ('num_pipeline',SimpleImputer(Strategy='median')),
                ('Scaler',StadardScaler())
                ]
            )

            cat_pipeline=Pipeline(
                steps=[
                ('cat_pipeline',SimpleImputer(Strategy='most_frequent')),
                ('encoding',OneHotEncoder()),
                ('Scaler',StadardScaler())
                ]
            )

            logging.info("Numerical column {}".format(numerical_feature))
            logging.info("Categorical column {}".format(categorical_feature))
        
            preprocessor=ColumnTransformer(
                [
                ('num_pipeline',num_pipeline,numerical_feature),
                ('cat_pipeline',cat_pipeline,categorical_feature)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomExeception(e,sys)

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_data=pd.read_csv(train_path)
            test_data=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformaer_obj()

            target_column="math_score"
            numerical_column=['reading_score','writing_score']
            categorical_column=['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']

            input_feature_train_df=train_data.drop(columns=[target_column],axis=1)
            target_feature_train_df=train_data[target_column]

            input_feature_test_df=test_data.drop(columns=[target_column],axis=1)
            target_feature_test_df=test_data[target_column]

            logging.info("Applying preprocessing object on training dataframe and testing dataframe.")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomExeception(e,sys)
        



