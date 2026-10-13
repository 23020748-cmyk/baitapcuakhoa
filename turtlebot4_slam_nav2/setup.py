from glob import glob
from os.path import isfile
from setuptools import setup

package_name = 'turtlebot4_slam_nav2'

setup(
    name=package_name,
    version='0.1.0',
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/worlds', glob('worlds/*')),
        ('share/' + package_name + '/config', glob('config/*')),
        ('share/' + package_name + '/description', [f for f in glob('description/*') if isfile(f)]),
        ('share/' + package_name + '/maps', glob('maps/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Luc Van Khoa',
    maintainer_email='khoa@example.com',
    description='TurtleBot 4 SLAM Toolbox and Nav2 exercise launch files',
    license='Apache-2.0',
    tests_require=['pytest'],
)


