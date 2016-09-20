# coding = ISO-8859-7
# -*- coding: ISO-8859-7 -*-
eps="wget http://epsana.gr/results/display_schedule.php?league_id="
id_from=70
id_to=115
import os,sys
import codecs

def show_ref(refgames,name_of_ref,only_board=False):
	main=0
	second=0
	third=0
	a=0
	b=0
	g=0
	kathgories={"alfa":[0,0,0],"bita":[0,0,0],"gama":[0,0,0],"cup":[0,0,0],"other":[0,0,0]}
	cup=0
	other=0
	with_suprior=0
	if len(refgames)==0:
		if only_board==False: print "No games for referee with name:|"+name_of_ref+"|"
		return
	for a_game in refgames:
		kathgoria=""
		i=0
		if u"A Κατηγορία" in a_game["kathgoria"] or u"Ά Κατηγορία" in a_game["kathgoria"]:
			kathgoria="alfa"
			a=a+1
		elif u"Β Κατηγορία" in a_game["kathgoria"]:
			kathgoria="bita"
			b=b+1
		elif u"Γ Κατηγορία" in a_game["kathgoria"]:
			kathgoria="gama"
			g=g+1
		elif u"Κύπελλο" in a_game["kathgoria"]:
			kathgoria="cup"
			cup=cup+1
		else:
			kathgoria="other"
			other=other+1
		if only_board==False: print "%s  %s %s" % (a_game["kathgoria"], a_game["hmerominia"],a_game["agonistikh"])
		if only_board==False: print "%-45s %-5s " % (a_game["omades"],a_game["score"]),
		i=0
		for one_refere in a_game["refs"]:
			if name_of_ref==one_refere:
				kathgories[kathgoria][i]=kathgories[kathgoria][i]+1
				if i==0:
					main=main+1
				if i==1:
					second=second+1
				if i==2:
					third=third+1
			if i==3:
				with_suprior=with_suprior+1
			if only_board==False: print "  %-15s," % one_refere,
			i=i+1
		if only_board==False: print "\n"
	main_1=kathgories["alfa"][0]+kathgories["bita"][0]+kathgories["gama"][0]+kathgories["cup"][0]
	main_2=kathgories["alfa"][1]+kathgories["bita"][1]+kathgories["gama"][1]+kathgories["cup"][1]
	main_3=kathgories["alfa"][2]+kathgories["bita"][2]+kathgories["gama"][2]+kathgories["cup"][2]

	print u'''\
---------------%24s-------------
|-------------------|----------------------------|
|  1st referee:%3d  |Α Κατηγορια:%3d(%3d-%3d-%3d)|
|  2nd referee:%3d  |Β Κατηγορια:%3d(%3d-%3d-%3d)|
|  3rd referee:%3d  |Γ Κατηγορια:%3d(%3d-%3d-%3d)|
|                   |  Κυπελλο  :%3d(%3d-%3d-%3d)|
|-------------------|----------------------------|
|  Total of   :%3d  |Total of   :%3d(%3d-%3d-%3d)|
|            With observator:%3d                 |
|-------------------|----------------------------|'''\
% (name_of_ref,\
main,a,kathgories["alfa"][0],kathgories["alfa"][1],kathgories["alfa"][2],\
second,b,kathgories["bita"][0],kathgories["bita"][1],kathgories["bita"][2],\
third,g,kathgories["gama"][0],kathgories["gama"][1],kathgories["gama"][2],\
cup,kathgories["cup"][0],kathgories["cup"][1],kathgories["cup"][2],\
main+second+third,a+b+g+cup,main_1,main_2,main_3,\
with_suprior)

def download_league(league_id):#change -nc(don't update) with -N(update) 
	if type(league_id) is not int:
		print "League_id is not a number|"+str(league_id)+"|"
		exit()
	file_name="display_schedule.php?league_id="+str(league_id)
	os.system(eps+str(league_id)+" -nc")
	return codecs.open(file_name,"r","ISO-8859-7")

def get_league_from_line(line):
	_league_name=""
	_season=""
	words=line.split()
	i=3
	for i in range(3,len(words)):
		_league_name=_league_name+words[i]+" "
	return _league_name

def string_clear(word_to_clear):
	is_clear=False
	while is_clear==False:
		(word_to_clear,is_clear)=string_clear_rec(word_to_clear)
	return word_to_clear

def string_clear_rec(word_to_clear):#was clear?
	a=word_to_clear.find("<")
	b=word_to_clear.find(">")
	if (a!=-1 and b!=-1 and b<a) or (b==-1 and a!=-1):
		word_to_clear=word_to_clear[b+1:]
		return word_to_clear,False


	html_start=word_to_clear.find("<")
	if html_start==-1:
		html_end=word_to_clear.find(">",html_start)
		if html_end==-1:
			return word_to_clear,True
	
	html_end=word_to_clear.find(">",html_start)
	if(html_end==-1):
		word_to_clear=word_to_clear[1:]
		return word_to_clear,True
	word_to_clear=word_to_clear[:html_start]+word_to_clear[html_end+1:]
	return word_to_clear,False


ref_games_1=[]
name1=raw_input(u'What is your name?')
name1=name1.decode("utf-8")
print name1
name1=name1.strip()

#ref_games_2=[]
#name2=u'ΚΩΤΣΑΙΝΑΣ Ε.a'


for num in range(id_from,id_to):
	current_leaugue_file=download_league(num)
	league_name=""
	agonistikh=0
	for line in current_leaugue_file:
		if league_name=="":#an den exeis brei to onoma ths kathgorias
			if "<title>" in line:
				league_name=get_league_from_line(line)
				league_name=string_clear(league_name)

		if '<div class="table" >' in line:
			agones=line.split("</tr>")
			agones=agones[:-1]
			for agonas in agones:
				game_info={}
				if "<h2>" in agonas:
					h2_start=agonas.find("h2")
					h2_end=agonas.find("/h2")
					title=agonas[h2_start+3:h2_end-1]
					title=string_clear(title)
				tr_start=agonas.find("<tr")
				
				td_start=agonas.find("<td",tr_start)
				td_end=agonas.find("</td>",td_start)
				omades=agonas[td_start+4:td_end]
				omades=string_clear(omades)
				game_info["omades"]=omades
				
				td_start=agonas.find("<td",td_end)#apo to telos tou prohgoumenou
				td_end=agonas.find("</td>",td_start)#apo thn arxh auto tou td
				ghpedo=agonas[td_start+4:td_end]
				ghpedo=string_clear(ghpedo)
				game_info["ghpedo"]=ghpedo
				
				td_start=agonas.find("<td",td_end)#apo to telos tou prohgoumenou
				td_end=agonas.find("</td>",td_start)#apo thn arxh auto tou td
				hmera=agonas[td_start+4:td_end]
				game_info["hmera"]=hmera
				
				td_start=agonas.find("<td",td_end)#apo to telos tou prohgoumenou
				td_end=agonas.find("</td>",td_start)#apo thn arxh auto tou td
				hmerominia=agonas[td_start+4:td_end]
				game_info["hmerominia"]=hmerominia
				
				td_start=agonas.find("<td",td_end)#apo to telos tou prohgoumenou
				td_end=agonas.find("</td>",td_start)#apo thn arxh auto tou td
				ora=agonas[td_start+4:td_end]
				game_info["ora"]=ora
	#########################				
				td_start=agonas.find("<td",td_end)#apo to telos tou prohgoumenou
				td_end=agonas.find("</td>",td_start)#apo thn arxh auto tou td
				refs=agonas[td_start+4:td_end]
	#########################
				names=refs.split(',')				
				game_info["refs"]=[]
				
				for name in names:
					game_info["refs"].append(name.strip())
				if game_info["refs"][-1].find("(")!=-1 :#an uparxei paratiritis
					temp_refs=game_info["refs"][-1].split("(")
					del game_info["refs"][-1]
					game_info["refs"].append(temp_refs[0].strip())

					game_info["refs"].append(temp_refs[1][0:11].strip()+" "+temp_refs[1][22:-1].strip()) #parathrhths
	#########################
				td_start=agonas.find("<td",td_end)#apo to telos tou prohgoumenou
				td_end=agonas.find("</td>",td_start)#apo thn arxh auto tou td
				score=agonas[td_start+4:td_end]
				score=string_clear(score)
				if score=="align='center'":
					score=u'Δ.Ε.Π'
				game_info["score"]=score
				
				game_info["kathgoria"]=league_name
				game_info["agonistikh"]=title
				for referee in game_info["refs"]:
					if referee==name1:
						ref_games_1.append(game_info)
#					if referee==name2:
#						ref_games_2.append(game_info)
					
				del game_info
	current_leaugue_file.close()
	print "--------------------------------------------------------------------"

show_ref(ref_games_1,name1)
#show_ref(ref_games_2)
