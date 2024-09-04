import numpy as np
import re
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer


def scaling(dataframe):
    # print("Input dataframe:", dataframe.shape)
    extracted_data = dataframe.iloc[:, 6:15]
    # print("Extracted data using iloc:", extracted_data.shape)
    scaler = StandardScaler()
    prep_data = scaler.fit_transform(extracted_data.to_numpy())
    # print("Scaling: Preprocessed data shape:", prep_data.shape)
    return prep_data, scaler

def nn_predictor(prep_data):
    # print("NN Predictor: Fitting nearest neighbors model...")
    neigh = NearestNeighbors(metric='cosine',algorithm='brute')
    neigh.fit(prep_data)
    # print("NN Predictor: Nearest neighbors model fitted successfully.")
    return neigh

def build_pipeline(neigh,scaler,params):
    # print("Building Pipeline...")
    transformer = FunctionTransformer(neigh.kneighbors,kw_args=params)
    pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
    # print("Pipeline built successfully.")
    return pipeline

def extract_data(dataframe,ingredients):
    # print("Extracting data...")
    extracted_data=dataframe.copy()
    extracted_data=extract_ingredient_filtered_data(extracted_data,ingredients)
    # print("Data extracted successfully.",extracted_data)
    return extracted_data
    
def extract_ingredient_filtered_data(dataframe,ingredients):
    # print("Extracting ingredient filtered data...")
    extracted_data=dataframe.copy()
    regex_string=''.join(map(lambda x:f'(?=.*{x})',ingredients))
    extracted_data=extracted_data[extracted_data['RecipeIngredientParts'].str.contains(regex_string,regex=True,flags=re.IGNORECASE)]
    # print("Ingredient filtered data extracted successfully.")
    return extracted_data

def apply_pipeline(pipeline,_input,extracted_data):
    # print("Applying Pipeline...")
    _input=np.array(_input).reshape(1,-1)
    # print("Input data for pipeline:", _input)
    #return extracted_data.iloc[pipeline.transform(_input)[0]]
    result = extracted_data.iloc[pipeline.transform(_input)[0]]
    # print("Pipeline applied successfully.")
    # print("Result:\n", result)
    return result

def recommend(dataframe,_input,ingredients=[],params={'n_neighbors':5,'return_distance':False}):
        # print("Recommending...")
        extracted_data=extract_data(dataframe,ingredients)
        if extracted_data.shape[0]>=params['n_neighbors']:
            prep_data,scaler=scaling(extracted_data)
            neigh=nn_predictor(prep_data)
            pipeline=build_pipeline(neigh,scaler,params)
            return apply_pipeline(pipeline,_input,extracted_data)
            print("Recommendation completed.")
            return result
        else:
            # print("Not enough data for recommendation.")
            return None

def extract_quoted_strings(s):
    # print("Extracting quoted strings...")
    # Find all the strings inside double quotes
    strings = re.findall(r'"([^"]*)"', s)
    # print("Quoted strings extracted successfully.")
    # Join the strings with 'and'
    return strings

def output_recommended_recipes(dataframe):
    # print("Outputting recommended recipes...")
    if dataframe is not None:
        output=dataframe.copy()
        output=output.to_dict("records")
        for recipe in output:
            recipe['RecipeIngredientParts']=extract_quoted_strings(recipe['RecipeIngredientParts'])
            recipe['RecipeInstructions']=extract_quoted_strings(recipe['RecipeInstructions'])
        # print("Recipes outputted successfully.")
        return output
    else:
        # print("No recommended recipes.")
        output=None
    

