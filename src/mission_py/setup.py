from setuptools import find_packages, setup

package_name = 'mission_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'mission_brain_node = mission_py.mission_brain_node:main',
            'sensor_reporter_node = mission_py.status_reporter_node:main',
        ],
    },
)
