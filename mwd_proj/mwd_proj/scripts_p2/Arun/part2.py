import scipy.io
import tensorly.backend as T
import tensorly.decomposition
import numpy as np
from sklearn.preprocessing import normalize
from time import time
import sys, os
from datetime import datetime
import django
import traceback
os.environ['DJANGO_SETTINGS_MODULE']="mwd_proj.settings"
django.setup()
from mwd_proj.utils.utils2 import *
import traceback
from django.db.models import Sum
import operator
import math
from django.db.models.functions import Lower
from mwd_proj.phase2.models import *
from django.db.models import Q
from mwd_proj.scripts_p2 import (print_genreactor_vector, print_genre_vector, print_user_vector, print_actor_vector)

def compute_Semantics_2d():
	"""Tensor decomposition on actor,movie,year and put actor into non-overlapping bins of latent semantics"""
	tag_dict = {}
	taglist = MlTags.objects.values_list('tagid', flat=True).distinct()
	tag_count = taglist.count()

	for n, each in enumerate(taglist):
		tag_dict[n] = each

	rating_dict = {}
	rate = MlRatings.objects.values_list('rating', flat=True).distinct()
	rating_count = rate.count()
	for n, each in enumerate(rate):
		rating_dict[n] = each

	movie_dict = {}
	mov = MlMovies.objects.values_list('movieid', flat=True).distinct()
	movie_count = mov.count()
	for n, each in enumerate(mov):
		movie_dict[n] = each

	tagobjs = GenomeTags.objects.values_list('tagid','tag')
	tag_mapping = {x[0]:x[1] for x in tagobjs}
	
	movieobjs = MlMovies.objects.values_list('movieid','moviename')
	movie_mapping = {x[0]:x[1] for x in movieobjs}
	

	print(tag_count)
	print(rating_count)
	print(movie_count)

	print tag_dict
	print rating_dict
	print movie_dict	

	# with open('tag_space_matrix/actor_dict.csv', 'wb') as csv_file:
	#     writer = csv.writer(csv_file)
	#     for key, value in sorted(actor_dict.items(),key=operator.itemgetter(1)):
	#        writer.writerow([value, key])
	# with open('tag_space_matrix/year_dict.csv', 'wb') as csv_file:
	#     writer = csv.writer(csv_file)
	#     for key, value in sorted(year_dict.items(),key=operator.itemgetter(1)):
	#        writer.writerow([value, key])
	# with open('tag_space_matrix/movie_dict.csv', 'wb') as csv_file:
	#     writer = csv.writer(csv_file)
	#     for key, value in sorted(movie_dict.items(),key=operator.itemgetter(1)):
	#        writer.writerow([value, key])

	results = [[[0]*rating_count for i in range(movie_count)] for i in range(tag_count)]
	# print(len(results))
	# print(len(results[0]))
	# print(len(results[0][0]))
	tags = MlRatings.objects.select_related().all()
	#break
	inv_t = {v: k for k, v in tag_dict.iteritems()}
	inv_m = {v: k for k, v in movie_dict.iteritems()}
	inv_r = {v: k for k, v in rating_dict.iteritems()}
	for row in tags:
		row1 = MlRatings.objects.filter(userid=row1.userid.userid)
		results[inv_t[row.tagid.tagid]][inv_m[row.movieid.movieid]][inv_r[row.movieid.rating]]=1.0
		
	tensor = T.tensor(np.array(results))
	print(tensor)
	factors = tensorly.decomposition.parafac(tensor,5)

	#ACTOR SEMANTICS
	print(factors[0])
	print("AFTER")
	#col_sums = factors[0].asnumpy().sum(axis=0)
	x=factors[0]
	factors[0] = (x.asnumpy() - x.asnumpy().min(0)) / x.asnumpy().ptp(0)
	print(factors[0])
	ls_1 = []
	ls_2 = []
	ls_3 = []
	ls_4 = []
	ls_5 = []
	# with open('tag_space_matrix/actor_dict.csv', mode='r') as infile:
	# 	reader = csv.reader(infile)
	# 	actor_dict = {rows[0]:rows[1] for rows in reader}


	for i in range(len(factors[0])):
	 row = factors[0][i]
	 #print(row)
	 num = np.ndarray.argmax(row)
	 val = max(row)
	 if num==0:
	   ls_1.append([tag_mapping[tag_dict[i]],val])
	if num==1:
	   ls_2.append([tag_mapping[tag_dict[i]],val])
	if num==2:
	   ls_3.append([tag_mapping[tag_dict[i]],val])
	if num==3:
	   ls_4.append([tag_mapping[tag_dict[i]],val])
	if num==4:
	   ls_5.append([tag_mapping[tag_dict[i]],val])
	  # for row in query:
	  #  ls_5.append([row['name'],val])

	print("LATENT SEMANTIC 1")
	for i in reversed(sorted(ls_1,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 2")
	for i in reversed(sorted(ls_2,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 3")
	for i in reversed(sorted(ls_3,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 4")
	for i in reversed(sorted(ls_4,key=lambda x: x[1])):
	 print(i)


	print("LATENT SEMANTIC 5")
	for i in reversed(sorted(ls_5,key=lambda x: x[1])):
	 print(i)


	# MOVIE SEMANTICS
	x=factors[2]
	factors[2] = (x.asnumpy() - x.asnumpy().min(0)) / x.asnumpy().ptp(0)
	ls_1 = []
	ls_2 = []
	ls_3 = []
	ls_4 = []
	ls_5 = []
	# with open('tag_space_matrix/movie_dict.csv', mode='r') as infile:
	# 	reader = csv.reader(infile)
	# 	actor_dict = {rows[0]:rows[1] for rows in reader}
	for i in range(len(factors[2])):
	 row = factors[2][i]
	 #print(row)
	 num = np.ndarray.argmax(row)
	 val = max(row)
	 if num==0:
	   ls_1.append([movie_mapping[movie_dict[i]],val])
	 if num==1:
	   ls_2.append([movie_mapping[movie_dict[i]],val])
	 if num==2:
	   ls_3.append([movie_mapping[movie_dict[i]],val])
	 if num==3:
	   ls_4.append([movie_mapping[movie_dict[i]],val])
	 if num==4:
	   ls_5.append([movie_mapping[movie_dict[i]],val])



	print("LATENT SEMANTIC 1")
	for i in reversed(sorted(ls_1,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 2")
	for i in reversed(sorted(ls_2,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 3")
	for i in reversed(sorted(ls_3,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 4")
	for i in reversed(sorted(ls_4,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 5")
	for i in reversed(sorted(ls_5,key=lambda x: x[1])):
	 print(i)

	# YEAR SEMANTICS
	x=factors[1]
	factors[1] = (x.asnumpy() - x.asnumpy().min(0)) / x.asnumpy().ptp(0)
	ls_1 = []
	ls_2 = []
	ls_3 = []
	ls_4 = []
	ls_5 = []
	for i in range(len(factors[1])):
	 row = factors[1][i]
	 #print(row)
	 num = np.ndarray.argmax(row)
	 val = max(row)
	 if num==0:
	  ls_1.append([rating_dict[i],val])
	 if num==1:
	  ls_2.append([rating_dict[i],val])
	 if num==2:
	  ls_3.append([rating_dict[i],val])
	 if num==3:
	  ls_4.append([rating_dict[i],val])
	 if num==4:
	  ls_5.append([rating_dict[i],val])


	print("LATENT SEMANTIC 1")
	for i in reversed(sorted(ls_1,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 2")
	for i in reversed(sorted(ls_2,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 3")
	for i in reversed(sorted(ls_3,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 4")
	for i in reversed(sorted(ls_4,key=lambda x: x[1])):
	 print(i)


	print("LATENT SEMANTIC 5")
	for i in reversed(sorted(ls_5,key=lambda x: x[1])):
	 print(i)

def compute_Semantics_2c():
	"""Tensor decomposition on actor,movie,year and put actor into non-overlapping bins of latent semantics"""
	actor_dict = {}
	act = MovieActor.objects.values_list('actorid', flat=True).distinct()
	actor_count = act.count()

	for n, each in enumerate(act):
		actor_dict[n] = each

	year_dict = {}
	yr = MlMovies.objects.values_list('year', flat=True).distinct()
	year_count = yr.count()
	for n, each in enumerate(yr):
		year_dict[n] = each

	movie_dict = {}
	mov = MlMovies.objects.values_list('movieid', flat=True).distinct()
	movie_count = mov.count()
	for n, each in enumerate(mov):
		movie_dict[n] = each

	actorobjs = ImdbActorInfo.objects.values_list('actorid','name')
	actor_mapping = {x[0]:x[1] for x in actorobjs}
	
	movieobjs = MlMovies.objects.values_list('movieid','moviename')
	movie_mapping = {x[0]:x[1] for x in movieobjs}
	

	print(actor_count)
	print(year_count)
	print(movie_count)

	print actor_dict
	print year_dict
	print movie_dict	

	# with open('tag_space_matrix/actor_dict.csv', 'wb') as csv_file:
	#     writer = csv.writer(csv_file)
	#     for key, value in sorted(actor_dict.items(),key=operator.itemgetter(1)):
	#        writer.writerow([value, key])
	# with open('tag_space_matrix/year_dict.csv', 'wb') as csv_file:
	#     writer = csv.writer(csv_file)
	#     for key, value in sorted(year_dict.items(),key=operator.itemgetter(1)):
	#        writer.writerow([value, key])
	# with open('tag_space_matrix/movie_dict.csv', 'wb') as csv_file:
	#     writer = csv.writer(csv_file)
	#     for key, value in sorted(movie_dict.items(),key=operator.itemgetter(1)):
	#        writer.writerow([value, key])

	results = [[[0]*movie_count for i in range(year_count)] for i in range(actor_count)]
	# print(len(results))
	# print(len(results[0]))
	# print(len(results[0][0]))

	whole_table = MovieActor.objects.select_related('movieid').all()
	print("#################")
	print(whole_table.count())
	inv_a = {v: k for k, v in actor_dict.iteritems()}
	inv_m = {v: k for k, v in movie_dict.iteritems()}
	inv_y = {v: k for k, v in year_dict.iteritems()}
	for row in whole_table:
		results[inv_a[row.actorid.actorid]][inv_y[row.movieid.year]][inv_m[row.movieid.movieid]]=1.0
		
	tensor = T.tensor(np.array(results))
	print(tensor)
	factors = tensorly.decomposition.parafac(tensor,5)

	#ACTOR SEMANTICS
	print(factors[0])
	print("AFTER")
	#col_sums = factors[0].asnumpy().sum(axis=0)
	x=factors[0]
	factors[0] = (x.asnumpy() - x.asnumpy().min(0)) / x.asnumpy().ptp(0)
	print(factors[0])
	ls_1 = []
	ls_2 = []
	ls_3 = []
	ls_4 = []
	ls_5 = []
	# with open('tag_space_matrix/actor_dict.csv', mode='r') as infile:
	# 	reader = csv.reader(infile)
	# 	actor_dict = {rows[0]:rows[1] for rows in reader}


	for i in range(len(factors[0])):
	 row = factors[0][i]
	 #print(row)
	 num = np.ndarray.argmax(row)
	 val = max(row)
	 if num==0:
	   ls_1.append([actor_mapping[actor_dict[i]],val])
	if num==1:
	   ls_2.append([actor_mapping[actor_dict[i]],val])
	if num==2:
	   ls_3.append([actor_mapping[actor_dict[i]],val])
	if num==3:
	   ls_4.append([actor_mapping[actor_dict[i]],val])
	if num==4:
	   ls_5.append([actor_mapping[actor_dict[i]],val])
	  # for row in query:
	  #  ls_5.append([row['name'],val])

	print("LATENT SEMANTIC 1")
	for i in reversed(sorted(ls_1,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 2")
	for i in reversed(sorted(ls_2,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 3")
	for i in reversed(sorted(ls_3,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 4")
	for i in reversed(sorted(ls_4,key=lambda x: x[1])):
	 print(i)


	print("LATENT SEMANTIC 5")
	for i in reversed(sorted(ls_5,key=lambda x: x[1])):
	 print(i)


	# MOVIE SEMANTICS
	x=factors[2]
	factors[2] = (x.asnumpy() - x.asnumpy().min(0)) / x.asnumpy().ptp(0)
	ls_1 = []
	ls_2 = []
	ls_3 = []
	ls_4 = []
	ls_5 = []
	# with open('tag_space_matrix/movie_dict.csv', mode='r') as infile:
	# 	reader = csv.reader(infile)
	# 	actor_dict = {rows[0]:rows[1] for rows in reader}
	for i in range(len(factors[2])):
	 row = factors[2][i]
	 #print(row)
	 num = np.ndarray.argmax(row)
	 val = max(row)
	 if num==0:
	   ls_1.append([movie_mapping[movie_dict[i]],val])
	 if num==1:
	   ls_2.append([movie_mapping[movie_dict[i]],val])
	 if num==2:
	   ls_3.append([movie_mapping[movie_dict[i]],val])
	 if num==3:
	   ls_4.append([movie_mapping[movie_dict[i]],val])
	 if num==4:
	   ls_5.append([movie_mapping[movie_dict[i]],val])



	print("LATENT SEMANTIC 1")
	for i in reversed(sorted(ls_1,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 2")
	for i in reversed(sorted(ls_2,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 3")
	for i in reversed(sorted(ls_3,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 4")
	for i in reversed(sorted(ls_4,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 5")
	for i in reversed(sorted(ls_5,key=lambda x: x[1])):
	 print(i)

	# YEAR SEMANTICS
	x=factors[1]
	factors[1] = (x.asnumpy() - x.asnumpy().min(0)) / x.asnumpy().ptp(0)
	ls_1 = []
	ls_2 = []
	ls_3 = []
	ls_4 = []
	ls_5 = []
	for i in range(len(factors[1])):
	 row = factors[1][i]
	 #print(row)
	 num = np.ndarray.argmax(row)
	 val = max(row)
	 if num==0:
	  ls_1.append([year_dict[i],val])
	 if num==1:
	  ls_2.append([year_dict[i],val])
	 if num==2:
	  ls_3.append([year_dict[i],val])
	 if num==3:
	  ls_4.append([year_dict[i],val])
	 if num==4:
	  ls_5.append([year_dict[i],val])


	print("LATENT SEMANTIC 1")
	for i in reversed(sorted(ls_1,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 2")
	for i in reversed(sorted(ls_2,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 3")
	for i in reversed(sorted(ls_3,key=lambda x: x[1])):
	 print(i)

	print("LATENT SEMANTIC 4")
	for i in reversed(sorted(ls_4,key=lambda x: x[1])):
	 print(i)


	print("LATENT SEMANTIC 5")
	for i in reversed(sorted(ls_5,key=lambda x: x[1])):
	 print(i)

if __name__ == "__main__":
	h=compute_Semantics_2d()
	print h
	pass
