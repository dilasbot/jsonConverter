import pandas as pd
import sqlite3
import sys

def create_file(json_file,db_file):
       
    data = pd.read_json(json_file)
    model = data['models']
    
    df1 = pd.DataFrame()
    for i in range(len(model)):
        frame = model[i]
        make = data['make_name'][i]
    
        for item in frame.values():
            my_dict = item
            my_dict.pop('model_styles')
            df = pd.DataFrame(data = my_dict)
            df['make_name'] = make
            df1 = df1.append(df)
            
    data = data.drop(columns = ['models']) 
    
    new_data = data.merge(df1,on='make_name')
          
    conn = None
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS makes_and_models (first_year int, last_year int, make_id int, make_name varchar(200), make_slug varchar(200), model_id int, model_name varchar(100), vehicle_type char(10), years int)')
    
    for i in range(len(new_data)):
        val = str(str(new_data['first_year'][i]) + ',' 
                  + str(new_data['last_year'][i]) + ',' 
                  + str(new_data['make_id'][i]) + ',"' 
                  + str(new_data['make_name'][i]) + '","'
                  + str(new_data['make_slug'][i]) + '",'
                  + str(new_data['model_id'][i]) + ',"'
                  + str(new_data['model_name'][i]) + '","'
                  + str(new_data['vehicle_type'][i]) + '",'
                  + str(new_data['years'][i]))
        stmt = "INSERT INTO makes_and_models (first_year, last_year, make_id,make_name,make_slug, model_id,model_name,vehicle_type,years) VALUES (" + val + ")"
        c.execute(stmt)
        conn.commit()
           
    conn.close()

   
if __name__ == '__main__':
     create_file(sys.argv[1],sys.argv[2])
 



