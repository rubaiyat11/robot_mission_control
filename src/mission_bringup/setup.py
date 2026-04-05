from setuptools import find_packages, setup

package_name = 'mission_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', [
            'launch/mission_dispatcher.launch.py',
        ]),
        ('share/' + package_name + '/config', [
            'config/brain_params.yaml',
            'config/sensor_params.yaml',
        ])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nemo',
    maintainer_email='rubaiyatabdullahrabi71@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
