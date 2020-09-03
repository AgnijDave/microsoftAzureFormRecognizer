import json
import glob
import traceback
import pandas as pd


data = [j for j in glob.glob("*.json")]
for d in data:
    data1 = d
    #print(data1)
    with open(data1,encoding = 'utf8') as f:
        info = json.load(f)
        pages = info['pages']
        tabular_data=[]
        cols = list()
        cols_data = list()
        final_text = ''
        for page in pages:
            text = ''
            text+='\n' 
            lines = page['keyValuePairs']
            
            ##TABULAR DATA
            try:
                table = page['tables']
                for tab in table:
                    table_name = tab['id']
                    #print(table_name)
                    for col in tab['columns']:
                        column_name = col['header'][0]['text']
                        #print(column_name)
                        cols.append(column_name)
                        txt = [i[0]['text'] for i in col['entries']]
                        cols_data.append(txt)
                        
                    #l5,l4,l3,l2,l1 = map(list, zip(*cols_data))
                    #c = [l5,l4,l3,l2,l1]
                    
                    my_lists = list(zip(*cols_data))
                    listy = list(map(list, my_lists))
                    
                    df = pd.DataFrame(listy,columns=cols)
                    tabular_data.append(df)
            except:
                print('No Tables here Sonny')
                print(traceback.format_exc())
                
            ##TEXTUAL DATA
            for line in lines:
                s1 = line['key'][0]['text']
                sentence = line['value']
                if not s1 == '__Tokens__':
                    text+=s1+'\n'
                for sent in sentence:
                    text+=sent['text']
                    text+='\n'
                    
            ##TABLES OF A PAGE ARE ADDED TO THE END OF THE PAGE
            for t in tabular_data:
                result = t.to_string(index = False)
                text+='\n'+result
            final_text+=text+'\n'
    file = d.rstrip('json')
    file = file + 'txt'
    with open(file,'w',encoding='utf-8') as f:
        f.write(final_text)
    f.close()
                
