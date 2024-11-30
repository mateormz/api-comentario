import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    s3_bucket_ingesta = os.environ["S3_BUCKET_INGESTA"]
    
    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    
    # Guardar el comentario en DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)
    
    # Guardar el comentario en S3
    s3 = boto3.client('s3')
    comentario_json = json.dumps(comentario)
    s3_key = f'comentarios/{uuidv1}.json'  # Usamos el uuid para crear un nombre único para el archivo

    # Subir el archivo JSON al bucket S3
    s3.put_object(Bucket=s3_bucket_ingesta, Key=s3_key, Body=comentario_json)
    
    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response
    }
