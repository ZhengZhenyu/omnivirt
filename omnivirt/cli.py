from typing import is_typeddict
import click
import prettytable as pt

from omnivirt import vmops
from omnivirt import omnivirtd


# List all instances on the host
@click.command()
def list():

    ret = omnivirtd.list_instances()
    tb = pt.PrettyTable()

    tb.field_names = ["Name", "Image", "IP"]

    for instance in ret:
        tb.add_row(
            [instance.name,
            instance.image,
            instance.ip])

    print(tb)

# List all usable images
@click.command()
def images():

    ret = omnivirtd.list_images()
    tb = pt.PrettyTable()

    tb.field_names = ["Image", "Location"]

    if ret['local']:
        for image in ret['local']:
            tb.add_row(
                [image, 'Local'])

    for image in ret['remote']:
        tb.add_row(
            [image, 'Remote'])

    print(tb)

@click.command()
@click.argument('image_id')
def download_image(image_id):
    omnivirtd.download_image(image_id)

@click.command()
def init():
    omnivirtd.init()

@click.command()
@click.argument('vm_name')
@click.option('--image', help='Image to build vm')
def launch(vm_name, image):
    ret = omnivirtd.create_instance(vm_name, image)
    if ret:
        tb = pt.PrettyTable()
        tb.field_names = ["Name", "Image", "IP Address"]
        tb.add_row([ret['Name'], ret['Image'], ret['IP Address']])
        print(tb)

@click.group()
def cli():
    pass

def main():
    cli.add_command(list)
    cli.add_command(images)
    cli.add_command(download_image)
    cli.add_command(init)
    cli.add_command(launch)
    cli()