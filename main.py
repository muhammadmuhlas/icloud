import os
import click
import sys

from pyicloud import PyiCloudService

print('Setup Time Zone')
os.environ['TZ'] = 'Asia/Jakarta'

print('Py iCloud Services')
api = PyiCloudService('email@lalala.com', 'password!!!')

if api.requires_2sa:
    print("Two-factor authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print("  %s: %s" % (i, device.get('deviceName', "SMS to %s" %
                                          device.get('phoneNumber'))))

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)


def exist(filename):
    for root, dirs, files in os.walk(os.path.join("photos")):
        if filename in files and not os.stat(
                'photos/' + filename).st_size == 0:
            print("Skipping: already exist " + filename)
            return True
    return False


for photo in api.photos.all:
    filename, ext = os.path.splitext(photo.filename)
    output_filename = str.format("{0}__{1}{2}", photo.asset_date.strftime(
        "%Y-%m-%d__%H-%M-%S"), filename, ext)

    if exist(output_filename):
        os.rename('photos/' + output_filename, 'photos/' + output_filename)
        continue

    print("Writing: to photos/" + output_filename)
    download = photo.download('original')
    with open("photos/" + output_filename, 'wb') as opened_file:
        for chunk in download.iter_content(chunk_size=8192):
            print("Iterating content of " + output_filename + "...")
            opened_file.write(chunk)
