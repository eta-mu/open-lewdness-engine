from setuptools import setup

def readme():
	with open('README.rst') as f:
		return f.read()

setup(name='open_lewdness_engine',
	version='0.0.9',
	description='Easily-moddable open-licence text adventure',
	long_description=open("README.txt").read(),
	classifiers=[
		'Development Status :: Alpha',
		'License :: MIT License',
		'Programming Language :: Python :: 3.6.0',
		'Topic :: Game :: Text Adventure :: Erotic',
	],
	keyowrds='open lewdness engine lewd game',
	author='OLEDev',
	license='MIT',
	packages=['open_lewdness_engine'],
	install_requires=[],
	zip_safe=False,
	gui_scripts={
		'console_scripts': [
			'open_lewdness_engine = open_lewdness_engine.__main__:main'
		]
	},
)