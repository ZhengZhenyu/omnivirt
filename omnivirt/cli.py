import click
import prettytable as pt

from omnivirt.backends.win import vmops
from omnivirt import omnivirtd
from omnivirt.grpcs import client


# List all instances on the host
@click.command()
def list():

    ret = omnivirtd.list_instances()
    tb = pt.PrettyTable()

    tb.field_names = ["Name", "Image", "IP"]

    for instance in ret:
        tb.add_row(
            [instance['name'],
            instance['image'],
            instance['ip']])

    print(tb)


# List all usable images
@click.command()
def images():

    omnivirt_client = client.Client()
    ret = omnivirt_client.list_images()
    tb = pt.PrettyTable()

    tb.field_names = ["Images", "Location", "Status"]

    for image in ret['images']:
        tb.add_row(
            [image['name'], image['location'], image['status']])

    print(tb)


@click.command()
@click.argument('name')
def download_image(name):
    omnivirt_client = client.Client()
    ret = omnivirt_client.download_image(name)
    print(ret['msg'])


@click.command()
@click.argument('name')
@click.option('--path', help='Image file to load')
def load_image(name, path):
    omnivirt_client = client.Client()
    ret = omnivirt_client.load_image(name, path)
    print(ret['msg'])


@click.command()
@click.argument('name')
def delete_image(name):
    omnivirt_client = client.Client()
    ret = omnivirt_client.delete_image(name)
    print(ret['msg'])


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


if __name__ == '__main__':
    cli.add_command(list)
    cli.add_command(images)
    cli.add_command(download_image)
    cli.add_command(load_image)
    cli.add_command(launch)
    cli.add_command(delete_image)
    cli()