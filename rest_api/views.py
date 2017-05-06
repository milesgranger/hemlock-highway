import boto3
import os
import ast
from flask import request, blueprints, current_app, jsonify
from .models import FileModel

api_blueprint = blueprints.Blueprint('api_blueprint',
                                     import_name=__name__,
                                     static_folder='static',
                                     template_folder='templates')

@api_blueprint.route('/sign_s3')
def sign_s3():
    """
    Given a request, returns a presigned_post request to upload a file to AWS S3 
    """
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')
    file_size = float(request.args.get('file_size'))

    # Fail if not all data is available.
    if not all([file_type, file_name]):
        return jsonify({'data': False})

    # Connect to client
    if os.environ.get('AWS_ACCESS_KEY_ID'):
        s3 = boto3.client('s3',
                          aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
                          )
    else:
        s3 = boto3.client('s3')

    # Get the presigned_post data to be used on the front-end
    expiresIn = int(file_size / 2e4) if int(file_size / 2e4) > 30 else 30  # Default to 30 sec if really small file.
    current_app.logger.info(
        'UPLOAD REQUEST:\n\tfilename: {}, filesize: {}, filetype: {}\n'
        .format(file_name, file_size, file_type) +
        '\tGiving {} sec until presigned post expires.'
        .format(expiresIn)
    )
    presigned_post = s3.generate_presigned_post(

        Bucket=os.environ.get('S3_BUCKET'),
        Key=file_name,
        Fields={'acl': 'public-read', 'Content-Type': file_type},
        Conditions=[
            {'acl': 'public-read'},
            {'Content-Type': file_type},
        ],
        ExpiresIn=expiresIn
    )

    return jsonify({'data': presigned_post,
                    'url': 'https://{}.s3.amazonaws.com/{}'.format(os.environ.get('S3_BUCKET'),
                                                                   file_name)
                    })

@api_blueprint.route('/user/<path:vardirs>')
def get_files(vardirs=None):

    vardirs = iter(vardirs.split('/'))
    username = next(vardirs, None)

    f = FileModel(hash_key=username,
                  range_key='/path/to/newfile2.log',
                  meta_data={'file_size': 500, 'file_type': 'image/jpg'})
    f.save()

    results = [r._get_json() for r in FileModel.query(hash_key=username,
                                                      file_name__begins_with='/' + '/'.join([dir for dir in vardirs]))]

    #"""
    data = []
    for i, (owner, package) in enumerate(results):
        metadata = package.get('attributes').get('meta_data').get('S')
        metadata = ast.literal_eval(metadata)
        data.append({'owner': owner,
                     'file_metadata': metadata,
                     'path': package.get('range_key')})
    #"""
    return jsonify(data)