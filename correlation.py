
# Add the functions in this file
import json
import math

def load_journal(filename):
	f=open(filename,"r")
	data=json.loads(f.read())
	
	f.close()
	return data

def compute_phi(filename,event):
	n11=n00=n10=n01=n1p=n0p=np1=np0=0
	journal=load_journal(filename)
	for i in range(len(journal)):
		jevents=journal[i].get("events")
		status=journal[i].get("squirrel")
		if(event in jevents and status):
			n11+=1
			n1p+=1
			np1+=1
		elif(event in jevents and (not status)):
			n10+=1 
			n1p+=1
			np0+=1
		elif((not event in jevents) and status):
			n01+=1
			n0p+=1
			np1+=1
		elif((not event in jevents) and (not status)):
			n00+=1
			n0p+=1
			np0+=1
	corr=((n11*n00)-(n10*n01))/(math.sqrt(n1p*n0p*np1*np0))
	return corr

def compute_correlations(filename):
	journal=load_journal(filename)
	jevents=[]
	for i in range(0,len(journal),1):
		for val in journal[i].get('events'):
			if val in jevents:
				continue
			else:
				jevents.append(val)
	dictcorr={}
	for eve in jevents:
		corr=compute_phi(filename,eve)
		dictcorr[eve]=corr
	return dictcorr

def diagnose(filename):
	cdict=compute_correlations(filename)
	max_value=max(cdict.values())
	min_value=min(cdict.values())
	for key,value in cdict.items():
		if max_value==value:
			maxevent= key
	for key,value in cdict.items():
                if min_value==value:
                        minevent=key
	return maxevent,minevent



