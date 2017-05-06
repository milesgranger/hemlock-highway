import boto3
import os
import sys
from flask.blueprints import Blueprint
from flask import render_template, request, flash, jsonify, current_app

home_blueprint = Blueprint(name='home_blueprint',
                           import_name=__name__,
                           template_folder='templates',
                           static_folder='static',
                           )

@home_blueprint.route('/')
def home_page():
    return render_template('home_index.html')

@home_blueprint.route('/sign_s3')
def sign_s3():
    """
    Given a request, returns a presigned_post request to upload a file to AWS S3 
    """


    S3_BUCKET = os.environ.get('S3_BUCKET')

    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    current_app.logger.info('Got filename: {} and filetype: {}'.format(file_name, file_type))

    # Connect to client
    s3 = boto3.client('s3',
                      aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
                      )

    current_app.logger.info('Established boto3 connection!')

    # Get the presigned_post data to be used on the front-end
    presigned_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=file_name,
        Fields={'acl': 'public-read', 'Content-Type': file_type},
        Conditions=[
            {'acl': 'public-read'},
            {'Content-Type': file_type},
        ],
        ExpiresIn=3600
    )

    current_app.logger.info('Got presigned_post data: {}'.format(presigned_post))

    return jsonify({'data': presigned_post,
                    'url': 'https://{}.s3.amazonaws.com/{}'.format(S3_BUCKET, file_name)
                    })
