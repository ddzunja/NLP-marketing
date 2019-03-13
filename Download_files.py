# Datasets inherit from:
# 
# R. He, J. McAuley. Modeling the visual evolution of fashion trends
# with one-class collaborative filtering. WWW, 2016
# J. McAuley, C. Targett, J. Shi, A. van den Hengel. Image-based
# recommendations on styles and substitutes. SIGIR, 2015


import argparse
import time
from argparse import RawTextHelpFormatter
from pathlib import Path
try:
	import wget
except:
	print('\n')
	print('\033[91m'+ 'You don\'t have wget package for using this downloader.\nYou need to install the package first in order to use this downloader.'+'\033[0m')
	print('\033[93m'+ '\nInstall \'wget\' using conda:\n' +'\033[0m')
	print('\033[92m' + 'conda install -c conda-forge python-wget'+'\033[0m')
	print('\033[93m'+ '\n\nInstalling \'wget\' using pip:\n' +'\033[0m')
	print('\033[92m' +'pip install wget'+'\033[0m' + '\n\n')
	raise;


running_loc = Path().resolve()

parser = argparse.ArgumentParser(description='Process download files',formatter_class=RawTextHelpFormatter)

parser.add_argument('-f','--file',metavar='name',type=str,default=['all'],nargs='*',
	help='''
	You need to specify required files to download

	default value is %(default)s to download all datasets

	'book' : for «Books»                       datasets
	'elec' : for «Electronics»                 datasets
	'mvtv' : for «Movies and TV»               datasets
	'cdvi' : for «CDs and Vinyl»               datasets
	'clsh' : for «Clothing, Shoes and Jewelry» datasets
	'hmkt' : for «Home and Kitchen»            datasets
	'kind' : for «Kindle Store»                datasets
	'sprt' : for «Sports and Outdoors»         datasets
	'cell' : for «Cell Phones and Accessories» datasets
	'heal' : for «Health and Personal Care»    datasets
	'toys' : for «Toys and Games»              datasets
	'vidg' : for «Video Games»                 datasets
	'tool' : for «Tools and Home Improvement»  datasets
	'beau' : for «Beauty»                      datasets
	'apps' : for «Apps for Android»            datasets
	'offc' : for «Office Products»             datasets
	'pets' : for «Pet Supplies»                datasets
	'auto' : for «Automotive»                  datasets
	'food' : for «Grocery and Gourmet Food»    datasets
	'grdn' : for «Patio, Lawn and Garden»      datasets
	'baby' : for «Baby»                        datasets
	'dgmu' : for «Digital Music»               datasets
	'muin' : for «Musical Instruments»         datasets
	'amvi' : for «Amazon Instant Video»        datasets

	you can specify multiple choices for download 
	(e.g. '-f book elec pets apps')
	''')

parser.add_argument('-dt','--dataset-type',metavar='dataset_type',default=['all'],nargs='*',
	help='''
	The default value is %(default)s

	'r' : for donwload review datasets
	'm' : for download metadata datasets
	'i' : for download image features

	Mutiple choice is available for this arg again 
	(e.g. '-dt r i')
	''')

parser.add_argument('-l','--loc',type=Path,metavar='location', default=running_loc,
	help='''
	Specify the location of saved folder.
	By default it will store data in the root location of running code.
	default : '%(default)s'
	''')



args = parser.parse_args()

location = args.loc
loc_down= {}

if location.exists():
	print('\nDatasets will be downloaded in the followinig address:\n \'{}\'\n'.format(args.loc))
	if not Path(location.as_posix()+'/data').exists():
		Path(location.as_posix()+'/data').mkdir()
	if not Path(location.as_posix()+'/data/img_features').exists():
		Path(location.as_posix()+'/data/img_features').mkdir()
	if not Path(location.as_posix()+'/data/reviews').exists():
		Path(location.as_posix()+'/data/reviews').mkdir()
	if not Path(location.as_posix()+'/data/meta').exists():
		Path(location.as_posix()+'/data/meta').mkdir()

	loc_down['i'] = Path(location.as_posix()+'/data/img_features/').as_posix();
	loc_down['r'] = Path(location.as_posix()+'/data/reviews/').as_posix();
	loc_down['m'] = Path(location.as_posix()+'/data/meta/').as_posix()
	pass
else:
	raise ValueError ('The requested location is not valid {}'.format(args.loc))



main_url='http://snap.stanford.edu/data/amazon/productGraph'


files_name_dic={
	'book' :'_Books',
	'elec' :'_Electronics',
	'mvtv' :'_Movies_and_TV',
	'cdvi' :'_CDs_and_Vinyl',
	'clsh' :'_Clothing_Shoes_and_Jewelry',
	'hmkt' :'_Home_and_Kitchen',
	'kind' :'_Kindle_Store',
	'sprt' :'_Sports_and_Outdoors',
	'cell' :'_Cell_Phones_and_Accessories',
	'heal' :'_Health_and_Personal_Care',
	'toys' :'_Toys_and_Games',
	'vidg' :'_Video_Games',
	'tool' :'_Tools_and_Home_Improvement',
	'beau' :'_Beauty',
	'apps' :'_Apps_for_Android',
	'offc' :'_Office_Products',
	'pets' :'_Pet_Supplies',
	'auto' :'_Automotive',
	'food' :'_Grocery_and_Gourmet_Food',
	'grdn' :'_Patio_Lawn_and_Garden',
	'baby' :'_Baby',
	'dgmu' :'_Digital_Music',
	'muin' :'_Musical_Instruments',
	'amvi' :'_Amazon_Instant_Video',
}
files_type_dic = {
	'r':['/categoryFiles/reviews','.json.gz','reviews'],
	'm':['/categoryFiles/meta','.json.gz','meta'],
	'i':['/image_features/categoryFiles/image_features','.b','image_features']
}

download_list =[]

req_files = args.file
req_types = args.dataset_type


if type(req_files)=='str':
	print('hit')
	req_files = [req_files]
if type(req_types)=='str':
	req_types = [req_types]

if len(req_files)==1:
	if req_files[0]=='all':
		req_files = files_name_dic.keys()
if len(req_types)==1:
	if req_types[0]=='all':
		req_types = files_type_dic.keys()

for dt_name in req_files:
	if dt_name not in files_name_dic:
		print('The requested file ({}) does not exist in the datasets.\n For more information check help'.format(dt_name))
	else:
		for dt_type in req_types:
			dl_name = files_type_dic[dt_type][0] + files_name_dic[dt_name] + files_type_dic[dt_type][1]
			fl_name = files_type_dic[dt_type][2] + files_name_dic[dt_name] + files_type_dic[dt_type][1]
			download_list.append([main_url + dl_name,loc_down[dt_type] + '/' + fl_name,fl_name])

for i in download_list:
	print('\033[93m' + 'Beginning file download with wget module' +'\033[0m')
	print('\033[92m' + 'File name: {}'.format(i[2]) +'\033[0m')
	url = i[0]
	if not Path(i[1]).exists():
		st = time.time()
		wget.download(url, i[1])
		print('\nDownload fninished in: {}s'.format(round(time.time()-st,3)))
	else:
		print('\033[94m' + 'File already downloaded' + '\033[0m')
	print('\033[92m' + '\n--------------------------------------------------------------\n' + '\033[0m')

print('\033[5;1;34m' + 'Finished' + '\033[0m')
