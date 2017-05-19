import s3fs
import os
import ast
import boto3
from botocore.client import Config
from flask import request, blueprints, current_app, jsonify
from .dynamodb_models import FileModel

api_blueprint = blueprints.Blueprint('api_blueprint',
                                     import_name=__name__,
                                     static_folder='static',
                                     template_folder='templates')

@api_blueprint.route('/list-files')
def list_files():
    """
    Expects arg of 'username' and optionally 'path' to filter paths.
    :return: JSON object of file locations
    """
    username = request.args.get('username')
    path = request.args.get('path')
    if not username:
        return jsonify({'error': 1, 'reason': 'No username supplied.'})

    fs = s3fs.S3FileSystem(key=os.environ.get('AWS_ACCESS_KEY_ID'),
                           secret=os.environ.get('AWS_SECRET_ACCESS_KEY')
                           )
    return jsonify({'error': 0,
                    'files': fs.ls(os.environ.get('S3_BUCKET') + '/{}'.format(username))})


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
                          'eu-west-1',
                          config=Config(s3={'addressing_style': 'path'}),
                          aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
                          )
        current_app.logger.info('Got env var credentials!')
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
        Key='milesg/{}'.format(file_name),
        Fields={'acl': 'public-read', 'Content-Type': file_type},
        Conditions=[
            {'acl': 'public-read'},
            {'Content-Type': file_type},
        ],
        ExpiresIn=expiresIn
    )

    current_app.logger.info(presigned_post)

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
