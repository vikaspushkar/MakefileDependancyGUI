import os
#import Queue
import matplotlib.pyplot as plt
import pylab
import subprocess
import networkx as nx

w = 2500;
file_relation = [[0 for x in range(w)] for y in range(w)] 
files=[None]*w
file_env=[dict() for x in range(w)]
file_parent=[ 0 for x in range(w)]
#parse_q=Queue.Queue()
makefile_index=0
G=nx.DiGraph()
def initial_list():
        absolute_path=os.popen('pwd ').read()
	abs=absolute_path.rstrip()
	cmd= 'find '+ abs+ ' -iname Makefile'
        initlist=os.popen(cmd).read()
        return initlist
def complete_list(initiallists ):
        splitted=initiallists.split('\n')	
	global files
	global file_relation
	global makefile_index
	#files=splitted
	print files
	files = [x for x in splitted if x != '']
	#makefile_index=1
	
        for id in files :
		print 'Analysing ' +id
		try:
        		with open(id, "rt") as ins :
        			for line_ in ins :
					line=line_.rstrip()
					if '=' in line and '==' not in line : 
						strip_the_value_and_store(line, makefile_index) 
                			if 'include' in line[0:8]:
                        			analyze_line(line,makefile_index)
		except IOError: # proc has already terminated
		       continue
		makefile_index=makefile_index+1
		print makefile_index
	x=0
	while x < makefile_index :
	#	print ' Environment of '
	#	print files[x]
	#	print '\n' 
#		print file_env[x]		
		x=x+1
	x=0
	while x < len(files):
	#	print files[x]
		x=x+1

	x=0
	#print file_relation
	local_files=files
	print files
	G.add_nodes_from(files)
	while x< 2500 :
		y=0
		while y< 2500 :
			if file_relation[x][y] == 1 :
				G.add_edge(x,y)
				print files[x] + ' depends on ' + files[y]
			y=y+1
		x=x+1
	#edge_labels=dict([(u,v,)for u,v in G.edges()])
	pos=nx.spring_layout(G)
	#nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
	#d_files =dict((0,el) for el in files)
	d_files ={k: v for k, v in enumerate(files)}
	print files
	print d_files
	nx.draw_networkx_labels(G,pos,None,font_size=6, font_color='k', font_family='sans-serif', font_weight='normal', alpha=1.0, bbox=None, ax=None)
	nx.draw(G)
	pylab.show()

def strip_the_value_and_store(line, index):
	separate_key_value=line.index('=')
	if separate_key_value >= 1:
		key_end=separate_key_value 
		key= line[0:key_end]
		value_start=separate_key_value +1
		value= line[value_start:]
		#print key +' : ' + value
		file_env[index][key]=value
		print files[index] + ' and the value '+ value +' for key '+ key
def analyze_line(line ,makefile_index):
	strt=0
	end=0
	value=' '
	global files
	global file_relation
	if '$(' in line :
		strt=line.index('$')
		strt=strt+2 #skip '$('
		end= line.index(')')
	if '${' in line :
		strt=line.index('$')
		strt=strt+2 #skip '${'
		end= line.index('}')
	if strt > 1 and end > strt :
		#print 'look in Makefile for '+ line[strt:end]
		if line[strt:end] in file_env[makefile_index] :
			value=file_env[makefile_index][line[strt:end]]
		else:
		#	print file_env[makefile_index]
		#	print 'look in enviroment for '+ line[strt:end]
			value= look_in_env(line[strt:end])
	
	if '..' in value:
		back_step=value.count('..')
		file=files[makefile_index]
		total_slashes=file.count('/')
		print file +' the value is '+ value
		print back_step 
		print total_slashes
		if back_step <= total_slashes :
			path= split_at(file,'/',total_slashes - back_step)
			t1=line.index(line[strt:end])
			t1=t1+ len(line[strt:end])+1
			if t1 >0 :
				new_path= path[0] + line[t1:]
				new_path=normalizing(new_path)
				print 'New Path is ' + new_path
				if new_path not in files:
					files.append(new_path)	
					print files
				file_relation[makefile_index][files.index(new_path)]=1
				#print file_relation[makefile_index][files.index(new_path)]
	
	#if '=' in line :
	#	print 'get the value ' +line 
	#	indx=line.index('=')
	#	indx=indx+1 # to skip the '=' sign
	#	if indx > 1 :
	#		print 'value '+ line[indx:] 
	
def normalizing(path):
	new=path.replace('/./','/')
	return new.replace('//','/')

def look_in_env(token):
	#print 'looking for ' + token
        env=os.popen('env ').read()
	if token in env:
		env_list=env.rstrip()
		for env_line in env_list:
			if token in env_line:
				value_indx=env_line.index('=')
				value_indx= value_indx + 1 #skip '='
				if value_indx > 0 :
	#				print ' value in env is ' + env_line[value_indx:]
					return env_line[value_indx:]
	return ''

def split_at(s, delim, n):
    r = s.split(delim, n)[n]
    return s[:-len(r)-len(delim)], r

def main():
        complete_list(initial_list())
  
if __name__== "__main__":
  main()
