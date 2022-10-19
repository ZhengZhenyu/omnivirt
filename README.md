# OmniVirt

## What is OmniVirt

OmniVirt is a lightweight and powerful virtualization management platform aimed to provide uniformed openEuler vm/container experience for Win/Mac/Linux users. 

## Usage

OmniVirt currently support Windows platform.

### Install on Windows

Clone the project:
``` Shell
git clone https://github.com/ZhengZhenyu/omnivirt.git && cd omnivirt
```

Open a `Terminal` or `Powershell` Console with Administrative permission and run:

``` Shell
Python3 setup.py install --user
```

### Run OmniVirt

#### OmniVirtd Daemon

Open a `Terminal` or `Powershell` Console with Administrative permission and run:

``` Shell
python3 omnivirt/omnivirtd.py --config-file etc/omnivirt-win.conf
```

#### OmniVirt CLI

``` Shell
python3 omnivirt/cli.py [command] [option]
```

OmniVirt CLI Currently supports actions to control images and instances, check the following details:

Images
------

1. List available images:
``` Shell
python3 cli.py images

+-----------+----------+--------------+
|   Images  | Location |    Status    |
+-----------+----------+--------------+
| 22.03-LTS |  Remote  | Downloadable |
|   21.09   |  Remote  | Downloadable |
| 2203-load |  Local   |    Ready     |
+-----------+----------+--------------+
```
There are two types of images: 1) Remote and 2) Local, only images with `Local` location and `Ready` status can be used to create instances. For remote images, you have to download it before use. You can also load pre-downloaded images to the system, please check the following commands for details.

2. Download a remote image:
``` Shell
python3 cli.py download-image 22.03-LTS

Downloading: 22.03-LTS, this might take a while, please check image status with "images" command.
```

As you can see, the downloading call is an async call, since the whole downloading process includes downloading, decompressing and transforming sub-processes, this might take up to 10 minutes according to the image size and network speed. While downloading, you can check the status of the image with image list command:

``` Shell
python3 cli.py images

+-----------+----------+--------------+
|   Images  | Location |    Status    |
+-----------+----------+--------------+
| 22.03-LTS |  Remote  | Downloadable |
|   21.09   |  Remote  | Downloadable |
| 22.03-LTS |  Local   | Downloading  |
+-----------+----------+--------------+
```

When your newly downloaded image status turned into `Ready` status, then you are good to go:

``` Shell
python3 cli.py images

+-----------+----------+--------------+
|   Images  | Location |    Status    |
+-----------+----------+--------------+
| 22.03-LTS |  Remote  | Downloadable |
|   21.09   |  Remote  | Downloadable |
| 22.03-LTS |  Local   |    Ready     |
+-----------+----------+--------------+
```

3. Load a local image

User can also load pre-downloaded or custom images to the system, currently the supported format is `xxx.qcow2.xz`:

``` Shell
python3 cli.py load-image --path {image_file_path} IMAGE_NAME
```

For example:
``` Shell
python3 cli.py load-image --path D:\openEuler-22.03-LTS-x86_64.qcow2.xz 2203-load

Loading: 2203-load, this might take a while, please check image status with "images" command.
```
The above command will load the `D:\openEuler-22.03-LTS-x86_64.qcow2.xz` file to the system and name it `2203-load`. Similar to download command, this command is also async, you can check loading status with:

``` Shell
python3 cli.py images

+-----------+----------+--------------+
|   Images  | Location |    Status    |
+-----------+----------+--------------+
| 22.03-LTS |  Remote  | Downloadable |
|   21.09   |  Remote  | Downloadable |
| 2203-load |  Local   |   Loading    |
+-----------+----------+--------------+
```

When it turned to `Ready` status, you are good to go, the `loading` proress is much faster than the `downloading` process.
``` Shell
python3 cli.py images

+-----------+----------+--------------+
|   Images  | Location |    Status    |
+-----------+----------+--------------+
| 22.03-LTS |  Remote  | Downloadable |
|   21.09   |  Remote  | Downloadable |
| 2203-load |  Local   |     Ready    |
+-----------+----------+--------------+
```

4. Delete image

Remove an image from the system by:

``` Shell
python3 cli.py delete-image 2203-load

Image: 2203-load has been successfully deleted.
```

Instances
---------

1. List all exixting instances:
``` Shell
python3 cli.py list

+----------+-----------+---------+---------------+
|   Name   |   Image   |  State  |       IP      |
+----------+-----------+---------+---------------+
|   test1  | 2203-load | Running | 172.22.57.220 |
+----------+-----------+---------+---------------+
|   test2  | 2203-load | Running |      N/A      |
+----------+-----------+---------+---------------+
```

Instances with `N/A` IP address means the IP address is not available yet, if the  `State` of the instance is `Running` then you should wait a while as the instance must be newly created and it takes serveral seconds before it can get an IP assigned.

If the instance has an IP address, you can directly SSH to that instance:

``` Shell
ssh root@{instance_ip}
```
The default password for `root` user of openEuler instances is `openEuler12#$`.

2. Create an instance:

``` Shell
python3 cli.py launch --image {image-name} {instance-name}
```

3. Delete instance:

``` Shell
python3 cli.py delete-instance {instance-name}
```
