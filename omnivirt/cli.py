import click
import prettytable as pt

from omnivirt import omnivirtd
from omnivirt.grpcs import client


omnivirt_client = client.Client()

# List all instances on the host
@click.command()
def list():

    ret = omnivirt_client.list_instances()
    tb = pt.PrettyTable()

    tb.field_names = ["Name", "Image", "State", "IP"]

    for instance in ret['instances']:
        tb.add_row(
            [instance['name'],
            instance['image'],
            instance['vmState'],
            instance['ipAddress']])

    print(tb)


# List all usable images
@click.command()
def images():

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

    ret = omnivirt_client.download_image(name)
    print(ret['msg'])


@click.command()
@click.argument('name')
@click.option('--path', help='Image file to load')
def load_image(name, path):

    ret = omnivirt_client.load_image(name, path)
    print(ret['msg'])


@click.command()
@click.argument('name')
def delete_image(name):

    ret = omnivirt_client.delete_image(name)
    print(ret['msg'])


@click.command()
@click.argument('vm_name')
@click.option('--image', help='Image to build vm')
def launch(vm_name, image):

    ret = omnivirt_client.create_instance(vm_name, image)

    if ret['ret'] == 1:
        tb = pt.PrettyTable()
        tb.field_names = ["Name", "Image", "State", "IP"]
        tb.add_row(
            [ret['instance']['name'],
            ret['instance']['image'],
            ret['instance']['vmState'],
            ret['instance']['ipAddress']])

        print(tb)
    
    else:
        print(ret['msg'])


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