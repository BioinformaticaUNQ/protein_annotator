import pandas as pd 
import json

def annotate_site_biolip(path, uniprot_id, position) -> object:

    #validacion de paramtetros
    if(path != None and uniprot_id != None and position != None):
        #cargo los datos de biolip en un dataframe
        df = pd.read_csv('/home/mauro/Documentos/BioLiP.txt.gz', sep='\t', lineterminator='\n',compression='gzip', usecols=[4,8,17], names=['NAid','NA1','NA2','NA3','ligando','NA4','NA5','NA6','sites','NA7','NA8','NA9','NA10','NA11','NA12','NA13','NA14','UniProt-ID','NA15','NA16','NA17'])        
        # filtro el dataframe por uniprot
        result = df.loc[df['UniProt-ID'] == str(uniprot_id)]
        #validio el resultado de la busqueda
        if(result.empty):
            return json.loads('{ "'+uniprot_id+'": {"biolip": "no se encontro valor para el uniprot id"  }}')
        #divido la posicion 9 original en 2, residuo y la posicion
    
        result = result.assign(sites=df['sites'].str.split()).explode('sites')
        result[['residue', 'position']] = result['sites'].str.extract(r'([A-Z])([000-999].+|[0-9]|[000-999].+|[0000-9999].+)')

        #busco si hay algun ligando para esa posicion
        ret = result.loc[result['position'] == str(position)]

        if(ret.empty):
            return json.loads('{ "'+uniprot_id+'" : {"biolip": "no hay ligandos para la posicion ingresada"}}')            
       
        jsons = ret.to_json(orient='records')
        return json.loads(jsons)[0]
    else:
        raise Exception("Parametros invalidos")

def annotate_biolip(path, uniprot_id) -> object:

    #validacion de paramtetros
    if(path != None and uniprot_id != None):
        #cargo los datos de biolip en un dataframe
        df = pd.read_csv(path, sep='\t', lineterminator='\n',compression='gzip', usecols=[4,8,17], names=['NAid','NA1','NA2','NA3','ligando','NA4','NA5','NA6','sites','NA7','NA8','NA9','NA10','NA11','NA12','NA13','NA14','UniProt-ID','NA15','NA16','NA17'])
        # filtro el dataframe por uniprot
        result = df.loc[df['UniProt-ID'] == str(uniprot_id)]
        #validio el resultado de la busqueda
        if(result.empty):
            return json.loads('{ "'+uniprot_id+'": {"biolip": "no se encontro valor para el uniprot id"  }}')
        #divido la posicion 9 original en 2, residuo y la posicion
    
        result = result.assign(sites=df['sites'].str.split()).explode('sites')
        result[['residue', 'position']] = result['sites'].str.extract(r'([A-Z])([000-999].+|[0-9]|[000-999].+|[0000-9999].+)')

        #busco si hay algun ligando para esa posicion
        
        if(result.empty):
            return json.loads('{ "'+uniprot_id+'" : {"biolip": "no hay ligandos para la posicion ingresada"}}')            
       
        jsons = result.to_json(orient='records')
        return json.loads(jsons)
    else:
        raise Exception("Parametros invalidos")