"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""
import pandas as pd

def clean_data():
    #se abre el dataframe y se elimina la columna inicial que es por un espacio antes del separador
    df=pd.read_csv('solicitudes_credito.csv',sep=';').drop('Unnamed: 0',axis=1)
    # se eliminan los valores nulos que hay en la columnas barrio y tipo de emprendimiento
    df.drop(list(df[df['barrio'].isnull()==True].index),axis=0, inplace=True)
    df.drop(list(df[df['tipo_de_emprendimiento'].isnull()==True].index),axis=0, inplace=True)
    #convertimos en minusculas todas las columnas tipo texto, ya que esto ayuda a que no se tomen como diferentes solo por su diferencia de formato valores iguales.
    for i in ['tipo_de_emprendimiento','idea_negocio','barrio','sexo','línea_credito']:
       df[i]=df[i].apply(lambda x: x.lower())
    #convertimos a entero la columna comuna_cidudadano
    df['comuna_ciudadano']=df['comuna_ciudadano'].astype(int)
    #Debido a que hay fechas que tienen diferente formato, unas se escriben  en el formato yyyy/mm/dd y otras dd/mm/yyyy, entonces unificamos en un solo formato
    #las fechas yyyy-mm-dd y le damos el formato de fechas
    lista=df['fecha_de_beneficio'].apply(lambda x: x.split('/'))
    lista_temp=[]
    for i in lista:
        if len(i[0])==4:
           lista_temp.append('/'.join([i[-1],i[1],i[0]]))
        else:
           lista_temp.append('/'.join(i))
    df['fecha_de_beneficio']=lista_temp
    df['fecha_de_beneficio']=pd.to_datetime(df['fecha_de_beneficio'],format="%d/%m/%Y")
    #eliminamos de la columna barrio y idea de negocio los caracteres, y espacios. Debido a que por los errores de escritura puede identificarse como barrios distintos
    #o ideas distintas, datos que representan el mismo barrio o misma idea de negocio.
    chars = ['.', ' ', '_','-','  ','   ','¿','?']
    df['idea_negocio']=df['idea_negocio'].apply(lambda x: x.strip().translate(str.maketrans('', '', ''.join(chars))))
    df['barrio']=df['barrio'].apply(lambda x: x.strip().translate(str.maketrans('', '', ''.join(chars))))
    #La columna monto de credito tiene varios valores en diferente formato, por lo tanto se depura.
    df['monto_del_credito']=df['monto_del_credito'].apply(lambda x: int(round(float(x[2:].replace(',','')),0)) if x.isnumeric()==False else int(x))
    #la linea del credito tiene varios campos de empresalial_ed que están escritos diferentes, por lo tanto se les asigna el mismo valor
    df['línea_credito']=df['línea_credito'].apply(lambda x: 'empresarial_ed' if (('empresarial' in x ) and ('ed' in x)) else x)
    #eliminamos todos los duplicados.Para que nuestro dataframe quede limpio de valores faltantes y duplicados, además que queden con el correcto formato.
    df.drop(list(df[df.duplicated()==True].index),axis=0, inplace=True)
    for i in [1173,2028,2255]:
       df.loc[i, ('barrio')]='sanjosedelacima'
    for j in [702,1200,2038,2942]:
        df.loc[j, ('barrio')]='versalles2'
    for k in [3314,8012]:
        df.loc[k, ('barrio')]='versallesno'
    df.reset_index(inplace=True,drop=True)
    return df
