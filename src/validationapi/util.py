from validator.validator import ValidationOptions, ValidationResult, ValidationRun
from hashlib import sha1
import hmac
import uuid
import os


def do_validation(json):
    """
    Performs validation based on a json request
    """
    options = ValidationOptions(json['return_file'])
    options.build(json['options'])

    main_filename = os.path.join('work', str(uuid.uuid4()) + ".sbol")
    with open(main_filename, 'a+') as file:
        file.write(json["main_file"])

    if json['options']['test_equality']:
        diff_filename = os.path.join('work', str(uuid.uuid4()) + ".sbol")

        with open(diff_filename, 'a+') as file:
            file.write(json["diff_file"])

        run = ValidationRun(options, main_filename, diff_filename)
    else:
        run = ValidationRun(options, main_filename)

    result = run.execute()
    return result

def validate_update_request(body, signature):
    key = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'DEPLOY_SECRET')

    try:
        with open(key) as secret_file:
            secret = secret_file.readline().strip()
    except OSError:
        return True

    message = hmac.new(bytearray(secret, 'utf8'), msg=body, digestmod=sha1)

    return hmac.compare_digest(message.hexdigest(), signature)
