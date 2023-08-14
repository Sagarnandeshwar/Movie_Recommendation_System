from tqdm import tqdm
import pandas as pd

def convert(input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
          # print(column)
          output_data[column] = input_data.iloc[:,column]
        with open(output_file, 'w') as fp:
            fp.write('\t'.join([selected_fields[column] for column in output_data.columns]) + '\n')
            for i in tqdm(range(output_data.shape[0])):
                fp.write('\t'.join([str(output_data.iloc[i, j])
                                    for j in range(output_data.shape[1])]) + '\n')
        
            fp.close()
                                  
