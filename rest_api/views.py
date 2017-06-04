import s3fs
import os
import boto3
from botocore.client import Config
from flask import request, blueprints, current_app, jsonify
from .models import get_redis_con

api_blueprint = blueprints.Blueprint('api_blueprint',
                                     import_name=__name__,
                                     static_folder='static',
                                     template_folder='templates')


@api_blueprint.route('/list-files')
def list_files(username=None, path=None):
    """
    Expects arg of 'username' and optionally 'path' to filter paths.
    :return: JSON object of file locations
    """

    # TODO: Protect this view; not just anyone should be able to list files: verify user is logged in and matches.

    username = request.args.get('username')
    path = request.args.get('path', '')
    if not username:
        return jsonify({'error': 1, 'reason': 'No username supplied.'})

    fs = s3fs.S3FileSystem(key=os.environ.get('AWS_ACCESS_KEY_ID'),
                           secret=os.environ.get('AWS_SECRET_ACCESS_KEY')
                           )
    return jsonify({'error': 0,
                    'files': fs.ls('{bucket}/{username}/{path}'.format(bucket=os.environ.get('S3_BUCKET'),
                                                                       username=username,
                                                                       path=path),
                                   detail=True)
                    })


@api_blueprint.route('/sign-s3')
def sign_s3():
    """
    Given a request, returns a presigned_post request to upload a file to AWS S3 
    """
    file_name = request.args.get('file-name')
    file_type = request.args.get('file-type')
    file_size = float(request.args.get('file-size'))

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
        Key='milesg/test-folder/{}'.format(file_name),
        Fields={'acl': 'public-read', 'Content-Type': file_type},
        Conditions=[
            {'acl': 'public-read'},
            {'Content-Type': file_type},
        ],
        ExpiresIn=expiresIn
    )

    current_app.logger.info(presigned_post)

    return jsonify({'data': presigned_post,
                    'url': 'https://{}.s3.amazonaws.com/test-folder/{}/'.format(os.environ.get('S3_BUCKET'),
                                                                   file_name)
                    })

@api_blueprint.route('/successful-upload')
def successful_upload():
    """
    Notify of successful upload
    :return: 
    """
    pass

