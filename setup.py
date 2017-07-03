from distutils.core import setup
import py2exe
setup(  windows=['main.py'],
		options={
				'py2exe':{
				'excludes':['Image','PIL._imagingagg','PyQt4','PyQt5','_abcoll','_imaging_gif','_util','cffi','lxml','openpyxl.tests','readline','tkinter'],
				'includes':['tkinter','os','sys']
				}
			},
		data_files=['img\folder.png','img\file.png']
	)