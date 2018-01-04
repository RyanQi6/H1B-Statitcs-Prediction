# coding: utf-8
import MySQLdb
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from models import H1B
#import predict_h1b2 as pr
import numpy as np
from sklearn.externals import joblib


def index(request): 
   #db = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost')    #cursor = db.cursor()  
    #cursor.execute('SELECT EMPLOYER_NAME FROM h1b ORDER BY CASE_ID')  
    #names = [row[0] for row in cursor.fetchall()
    #casesInstance = h1b.objects.all()[5:10]
    #caseInstance = H1B.objects.filter(year=2016).order_by('?').first()
    #db.close()
    return render(request,"index.html")


def MyCase(request):
      return render(request,"MyCase.html")

def Statistics(request):
      return render(request,"Statistics.html")

def Prediction(request):
      return render(request,"Prediction.html")

def visual(request):
      return render(request,"Visual.html")

def visual2(request):
      return render(request,"Visual2.html")

def visual3(request):
      return render(request,"Visual3.html")

def about(request):
      return render(request,"about.html")

def findid(request):
	caseid = request.GET.get("casenum",0)
	db = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost') 
	cursor=db.cursor()
	sqlstmt = ('SELECT * FROM h1b WHERE case_id = %s')
	chamsql = ('SELECT * FROM People_In_Champaign_rich WHERE case_id = %s')
	cursor.execute(sqlstmt,(caseid,))
	report = cursor.fetchall()
	cursor.execute(chamsql,(caseid,))
	cham = cursor.fetchall()
	db.close()
#	return HttpResponse(strreport)
	if len(report) < 1:
		return render(request,"MyCase.html",{"result":"Error! Case not found!"})
	if len(cham) > 0:
		return render(request,"MyCase.html",{"result":"Welcome, applicant "+str(report[0][0])+"! Your employer is : "+report[0][2]+".  Your workplace is : "+report[0][8]+".  Your wage is : "+str(report[0][6])+".  Your job title is : "+report[0][4]+". "+"Your current status : "+report[0][1]+".", "Champaign":"Wow!You are a Champaign Rich! Greetings! Hope you can share more with us about how to be a rich like you in Champaign, and how is it feel to live here with a wage of over 100k! "})
	return render(request,"MyCase.html",{"result":"Welcome, applicant "+str(report[0][0])+"! Your employer is : "+report[0][2]+".  Your workplace is : "+report[0][8]+".  Your wage is : "+str(report[0][6])+".  Your job title is : "+report[0][4]+". "+"Your current status : "+report[0][1]+"."})

def insert(request):
  	caseid = request.GET.get("addcasenum", -1)
  	employer = request.GET.get("addemployer","default")
 	jobtitle = request.GET.get("addjobtitle","default")
  	workplace = request.GET.get("addworkplace","default")
  	wage = request.GET.get("addwage", -1)
	status = request.GET.get("addstatus","DENIED")
	code = request.GET.get("admin1")
	if code != "lovekevin":
		return render(request,"MyCase.html", {"addalert": "Permission Denied! Only administrators are allowed to make this action."})
	if caseid=='' or employer=='' or jobtitle=='' or workplace=='' or wage=='' or status=='':
       		return render(request,"MyCase.html", {"addalert": "Invalid input! Please fill in all the forms."})
	db = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost') 
	cursor=db.cursor()
	#sqlstmt = ('INSERT INTO h1b VALUES (%s,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)')
	#data=(1212123,)
	sqlstmt = ('INSERT INTO h1b (case_id,soc_name,full_time_position,year,lon,lat,employer_name,job_tile,worksite,prevailing_wage,case_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
	dftsoc = "UNKNOWN"
	dftfulltime = "Y"
	dftyear = 2017
	dftlon = 0.0
	dftlat = 0.0
	data = (caseid,dftsoc,dftfulltime,dftyear,dftlon,dftlat,employer,jobtitle,workplace,wage,status)
	sqlcheck = ('SELECT * FROM h1b WHERE case_id = %s')
	cursor.execute(sqlcheck,(caseid,))
	report = cursor.fetchall()
	if len(report) > 0 :
		return render(request,"MyCase.html", {"addalert": "Error! Case already exists."})
	#sqlstmt = ('INSERT INTO h1b VALUES (%s,NULL, %s,NULL, %s,NULL,%s,NULL, %s, NULL,NULL)')
        #data = (caseid, employer, jobtitle, wage, workplace)
	cursor.execute(sqlstmt, data)
	db.commit()
	db.close()
	#return HttpResponse(str(report))
	return render(request,"MyCase.html", {"addalert": "Successfully added your data. Thank you for providing instance to H1B-Statistics."}) 

def update(request):
        caseid = request.GET.get("editcasenum", 0)
        employer = request.GET.get("editemployer","default")
        jobtitle = request.GET.get("editjobtitle","default")
        workplace = request.GET.get("editplace","default")
        wage = request.GET.get("editwage", 100000)
        status = request.GET.get("editstatus","DENIED")
	code = request.GET.get("admin2")
        if code != "lovekevin":
                return render(request,"MyCase.html", {"updatealert": "Permission Denied! Only administrators are allowed to make this action."})
        dbb = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost')
        cursor=dbb.cursor()
	if caseid=='':
		return render(request,"MyCase.html", {"updatealert": "Invalid Input! Please enter your case ID."})
        #sqlstmt = ('INSERT INTO h1b VALUES (%s,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)')
        #data=(1212123,)
	sql = ('SELECT * FROM h1b WHERE case_id=%s')
	cursor.execute(sql, (caseid,))
	original = cursor.fetchall()
	if len(original)==0:
		return render(request,"MyCase.html", {"updatealert": "This case is not in the database, please add it to database first."})
	if employer=='':
		employer=original[0][2]
	if jobtitle=='':
		jobtitle=original[0][4]
	if workplace=='':
		workplace=original[0][8]
	if wage=='':
		wage=original[0][6]
	if status=='':
		status=original[0][1]
        sqlstmt = ('UPDATE h1b SET employer_name=%s,job_tile=%s,worksite=%s,prevailing_wage=%s,case_status=%s WHERE case_id=%s')
        data = (employer, jobtitle, workplace, wage, status, caseid)
        #sqlstmt = ('INSERT INTO h1b VALUES (%s,NULL, %s,NULL, %s,NULL,%s,NULL, %s, NULL,NULL)')
        #data = (caseid, employer, jobtitle, wage, workplace)
        cursor.execute(sqlstmt, data)
        dbb.commit()
        dbb.close()
        return render(request,"MyCase.html", {"updatealert": "Successfully updated your data. Thank you for providing instance to H1B-Statistics."})

def deleteid(request):
        caseid = request.GET.get("delcasenum",0)
	code = request.GET.get("admin3")
        if code != "lovekevin":
                return render(request,"MyCase.html", {"delresult": "Permission Denied! Only administrators are allowed to make this action."})
        db = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost')
        cursor=db.cursor()
        sqlstmt = ('DELETE FROM h1b WHERE case_id = %s')
        cursor.execute(sqlstmt,(caseid,))
	db.commit()
        db.close()
	return render(request, "MyCase.html", {"delresult": "Deleted your case successfully. Thank you for using H1B_Statistics."})

def statstate(request):
	state = request.GET.get('state')
	regstate = "%"+state+"%"
	db = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost')
        cursor=db.cursor()
	cursor.execute('SET @state = %s', (regstate,))
	cursor.execute('SET @status = %s',("CERTIFIED",))
	cursor.execute('CALL selectstate(@state, @status)',())
	sc = cursor.fetchall()
	cursor.close()
	cursor2 = db.cursor()
	#cursor.execute('SET @state2 = %s', (regstate,))
        cursor2.execute('SET @status2 = %s',("CERTIFIED-WITHDRAWN",))
        cursor2.execute('CALL selectstate(@state, @status2)',())
        scw = cursor2.fetchall()
	cursor2.close()
	cursor3 = db.cursor()
	#cursor.execute('SET @state3 = %s', (regstate,))
        cursor3.execute('SET @status3 = %s',("WITHDRAWN",))
        cursor3.execute('CALL selectstate(@state, @status3)',())
        sw = cursor3.fetchall()
	cursor3.close()
	cursor4 = db.cursor()
	#cursor.execute('SET @state4 = %s', (regstate,))
        cursor4.execute('SET @status4 = %s',("DENIED",))
        cursor4.execute('CALL selectstate(@state, @status4)',())
        sdr = cursor4.fetchall()
        '''countc = ('SELECT COUNT(CASE_ID) FROM h1b WHERE WORKSITE LIKE %s AND CASE_STATUS = "CERTIFIED"') 
	cursor.execute(countc,("%"+state+"%",))
	sc = cursor.fetchall()
	countcw = ('SELECT COUNT(CASE_ID) FROM h1b WHERE WORKSITE LIKE %s AND CASE_STATUS = "CERTIFIED-WITHDRAWN"')
	cursor.execute(countcw,("%"+state+"%",))
        scw = cursor.fetchall()
	countw = ('SELECT COUNT(CASE_ID) FROM h1b WHERE WORKSITE LIKE %s AND CASE_STATUS = "WITHDRAWN"')
	cursor.execute(countw,("%"+state+"%",))
        sw = cursor.fetchall()
	countdr = ('SELECT COUNT(CASE_ID) FROM h1b WHERE WORKSITE LIKE %s AND CASE_STATUS = "DENIED" OR CASE_STATUS = "REJECTED"')
        cursor.execute(countdr,("%"+state+"%",))
	sdr = cursor.fetchall()'''
	stateres = [sc[0][0], scw[0][0], sw[0][0], sdr[0][0]]
	#return HttpResponse(str(stateres))
	state = str(state)
	return render(request, "Statistics.html", {"stateres":stateres, "state":state, "statcmpres":[-1,0,0,0,0], "colleaguestat":[-1,0,0,0,0], "likemeres": [-1,0,0,0,0]})
	



def statlikeme(request):
	mycaseid = request.GET.get("caseid", 0)
	db = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost')
        cursor=db.cursor()
	if request.GET.get("likemestat") == "chart":
		countc = ('SELECT COUNT(h2.CASE_ID) FROM h1b h1, h1b h2 WHERE h1.CASE_ID=%s AND h1.WORKSITE=h2.WORKSITE AND h1.SOC_NAME=h2.SOC_NAME AND h1.CASE_ID <> h2.CASE_ID AND h1.PREVAILING_WAGE < h2.PREVAILING_WAGE+15000 AND h1.PREVAILING_WAGE > h2.PREVAILING_WAGE-15000 AND h2.CASE_STATUS=%s')
		countcw = ('SELECT COUNT(h2.CASE_ID) FROM h1b h1, h1b h2 WHERE h1.CASE_ID=%s AND h1.WORKSITE=h2.WORKSITE AND h1.SOC_NAME=h2.SOC_NAME AND h1.CASE_ID <> h2.CASE_ID AND h1.PREVAILING_WAGE < h2.PREVAILING_WAGE+15000 AND h1.PREVAILING_WAGE > h2.PREVAILING_WAGE-15000 AND h2.CASE_STATUS=%s' )
		countw = ('SELECT COUNT(h2.CASE_ID) FROM h1b h1, h1b h2 WHERE h1.CASE_ID=%s AND h1.WORKSITE=h2.WORKSITE AND h1.SOC_NAME=h2.SOC_NAME AND h1.CASE_ID <> h2.CASE_ID AND h1.PREVAILING_WAGE < h2.PREVAILING_WAGE+15000 AND h1.PREVAILING_WAGE > h2.PREVAILING_WAGE-15000 AND h2.CASE_STATUS=%s' )
		countdr = ('SELECT COUNT(h2.CASE_ID) FROM h1b h1, h1b h2 WHERE h1.CASE_ID=%s AND h1.WORKSITE=h2.WORKSITE AND h1.SOC_NAME=h2.SOC_NAME AND h1.CASE_ID <> h2.CASE_ID AND h1.PREVAILING_WAGE < h2.PREVAILING_WAGE+15000 AND h1.PREVAILING_WAGE > h2.PREVAILING_WAGE-15000 AND (h2.CASE_STATUS=%s OR h2.CASE_STATUS=%s)')
		#countc = ('SELECT h2.CASE_ID,h2.EMPLOYER_NAME, h2.PREVAILING_WAGE, h2.SOC_NAME, h2.WORKSITE, h2.CASE_STATUS FROM h1b h1, h1b h2 WHERE h1.CASE_ID=%s AND h1.WORKSITE=h2.WORKSITE AND h1.SOC_NAME=h2.SOC_NAME AND h1.CASE_ID <> h2.CASE_ID AND h1.PREVAILING_WAGE < h2.PREVAILING+15000 AND h1.PREVAILING_WAGE > h2.PREVAILING_WAGE-15000 AND CASE_STATUS=%s' )
		cursor.execute(countc,(mycaseid, "CERTIFIED"))
                cc = cursor.fetchall()
                cursor.execute(countcw,(mycaseid, "CERTIFIED-WITHDRAWN"))
                ccw = cursor.fetchall()
                cursor.execute(countw, (mycaseid, "WITHDRAWN"))
                cw = cursor.fetchall()
                cursor.execute(countdr, (mycaseid, "DENIED","REJECTED"))
                cdr = cursor.fetchall()
		likemeres = [cc[0][0], ccw[0][0], cw[0][0], cdr[0][0]]
		mycaseid = str(mycaseid)
		return render(request, "Statistics.html", {"likemeres":likemeres, "mycaseid":mycaseid, "statcmpres":[-1,0,0,0,0], "colleaguestat":[-1,0,0,0,0], "stateres":[-1,0,0,0,0]})
	else:
        	sqlstmt = ('SELECT h2.CASE_ID,h2.EMPLOYER_NAME, h2.PREVAILING_WAGE, h2.SOC_NAME, h2.WORKSITE, h2.CASE_STATUS FROM h1b h1, h1b h2 WHERE h1.CASE_ID=%s AND h1.WORKSITE=h2.WORKSITE AND h1.SOC_NAME=h2.SOC_NAME AND h1.CASE_ID <> h2.CASE_ID AND h1.PREVAILING_WAGE < h2.PREVAILING_WAGE+15000 AND h1.PREVAILING_WAGE > h2.PREVAILING_WAGE-15000')
		cursor.execute(sqlstmt,(mycaseid,))
		qresult = cursor.fetchall()
		if len(qresult) == 0:
			return render(request, "Statistics.html",{"result":"No similar applicants found."})
		db.close()
		return render(request, "Statistics.html",{"qresult":qresult})

def statcolleague(request):
        mycaseid = request.GET.get("caseid2", 0)
        db = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost')
        cursor=db.cursor()
	if request.GET.get("colleaguestat") == "chart":
		countc = ('SELECT COUNT(h2.CASE_ID) FROM h1b h1, h1b h2 WHERE h1.CASE_ID=%s AND h1.WORKSITE=h2.WORKSITE AND h1.EMPLOYER_NAME = h2.EMPLOYER_NAME AND h1.CASE_ID <> h2.CASE_ID AND h2.CASE_STATUS=%s')
                countcw = ('SELECT COUNT(h2.CASE_ID) FROM h1b h1, h1b h2 WHERE h1.CASE_ID=%s AND h1.WORKSITE=h2.WORKSITE AND h1.EMPLOYER_NAME = h2.EMPLOYER_NAME AND h1.CASE_ID <> h2.CASE_ID AND h2.CASE_STATUS=%s')
		countw = ('SELECT COUNT(h2.CASE_ID) FROM h1b h1, h1b h2 WHERE h1.CASE_ID=%s AND h1.WORKSITE=h2.WORKSITE AND h1.EMPLOYER_NAME = h2.EMPLOYER_NAME AND h1.CASE_ID <> h2.CASE_ID AND h2.CASE_STATUS=%s')
		countdr = ('SELECT COUNT(h2.CASE_ID) FROM h1b h1, h1b h2 WHERE h1.CASE_ID=%s AND h1.WORKSITE=h2.WORKSITE AND h1.EMPLOYER_NAME = h2.EMPLOYER_NAME AND h1.CASE_ID <> h2.CASE_ID AND (h2.CASE_STATUS=%s OR h2.CASE_STATUS=%s)')
		cursor.execute(countc,(mycaseid, "CERTIFIED"))
                cc = cursor.fetchall()
                cursor.execute(countcw,(mycaseid, "CERTIFIED-WITHDRAWN"))
                ccw = cursor.fetchall()
                cursor.execute(countw, (mycaseid, "WITHDRAWN"))
                cw = cursor.fetchall()
                cursor.execute(countdr, (mycaseid, "DENIED","REJECTED"))
                cdr = cursor.fetchall()
		colleaguestat = [cc[0][0], ccw[0][0], cw[0][0], cdr[0][0]]
		mycaseid = str(mycaseid)
		return render(request, "Statistics.html", {"colleaguestat":colleaguestat, "mycaseid":mycaseid, "statcmpres":[-1,0,0,0,0], "likemeres":[-1,0,0,0,0], "stateres":[-1,0,0,0,0]})
	else:
        	sqlstmt = ('SELECT h2.CASE_ID,h2.EMPLOYER_NAME, h2.PREVAILING_WAGE, h2.SOC_NAME, h2.WORKSITE, h2.CASE_STATUS FROM h1b h1, h1b h2 WHERE h1.CASE_ID=%s AND h1.WORKSITE=h2.WORKSITE AND h1.EMPLOYER_NAME = h2.EMPLOYER_NAME AND h1.CASE_ID <> h2.CASE_ID')
       		cursor.execute(sqlstmt,(mycaseid,))
       		cresult = cursor.fetchall()
        	if cresult is None:
                	return render(request, "Statistics.html",{"result2":"No similar applicants found."})
        	db.close()
        	return render(request, "Statistics.html",{"cresult":cresult})

def statcompany(request):
	keyword = request.GET.get("cmpname", 0)
	db = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost')
	cursor=db.cursor()
	if request.GET.get("cmpstat") == "chart":
		countc = ('SELECT COUNT(CASE_ID) FROM h1b WHERE (EMPLOYER_NAME LIKE %s OR EMPLOYER_NAME LIKE %s) AND CASE_STATUS = %s')
		countcw = ('SELECT COUNT(CASE_ID) FROM h1b WHERE (EMPLOYER_NAME LIKE %s OR EMPLOYER_NAME LIKE %s) AND CASE_STATUS = %s')
		countw = ('SELECT COUNT(CASE_ID) FROM h1b WHERE (EMPLOYER_NAME LIKE %s OR EMPLOYER_NAME LIKE %s) AND CASE_STATUS = %s')
		countdr = ('SELECT COUNT(CASE_ID) FROM h1b WHERE (EMPLOYER_NAME LIKE %s OR EMPLOYER_NAME LIKE %s) AND CASE_STATUS = %s')
		cursor.execute(countc,(keyword+" %",keyword+",%", "CERTIFIED"))
		cc = cursor.fetchall()
		cursor.execute(countcw, (keyword+" %",keyword+",%", "CERTIFIED-WITHDRAWN"))
		ccw = cursor.fetchall()
		cursor.execute(countw, (keyword+" %",keyword+",%", "WITHDRAWN"))
		cw = cursor.fetchall()
		cursor.execute(countdr, (keyword+" %",keyword+",%", "DENIED"))
		cdr = cursor.fetchall()
		statcmpres = [cc[0][0], ccw[0][0], cw[0][0], cdr[0][0]]
		keyword=str(keyword)		
		return render(request, "Statistics.html", {"statcmpres":statcmpres, "keyword":keyword, "colleaguestat":[-1,0,0,0,0], "likemeres":[-1,0,0,0,0], "stateres":[-1,0,0,0,0]})
	else:
		sqlstmt = ('SELECT CASE_ID, EMPLOYER_NAME, PREVAILING_WAGE, SOC_NAME, WORKSITE, CASE_STATUS FROM h1b WHERE EMPLOYER_NAME LIKE %s OR EMPLOYER_NAME LIKE %s')
		cursor.execute(sqlstmt,(keyword+" %",keyword+",%",))
		cmpresult = cursor.fetchall()
		if cmpresult is None:
			return render(request, "Statistics.html", {"result3": "No similar applicants found."})
		db.close()
		return render(request, "Statistics.html",{"cmpresult": cmpresult})

def citybubble(request):
	db = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost')
        cursor=db.cursor()
	if request.GET.get("partition") == "0":
		sql = ('select c,worksite from (select count(worksite) as c,worksite from h1bBubble where case_status= %s group by worksite) t order by c desc limit 10')
		cursor.execute(sql,("CERTIFIED",))
	elif request.GET.get("partition") == "1":
		sql = ('select c,worksite from (select count(worksite) as c,worksite from h1bTest where case_status= %s AND year=%s group by worksite) t order by c desc limit 10')
                cursor.execute(sql,("CERTIFIED",2016))
	elif request.GET.get("partition") == "2":
		sql = ('select c,worksite from (select count(worksite) as c,worksite from h1bTest where case_status= %s AND year=%s group by worksite) t order by c desc limit 10')
		cursor.execute(sql,("CERTIFIED",2015))
	res = cursor.fetchall()
	res = list(res)
	j = 0
	for j in range(10):
		res[j] = list(res[j])
	i = 0
	for i in range(10):
		res[i][0] = str(res[i][0])
		res[i][1] = str(res[i][1])
	k = 0
	for k in range(10):
		res[k] = tuple(res[k])
	res = tuple(res)	
	#res = str(res)
	return render(request, "Visual.html", {"res": res})

def jobbubble(request):
        db = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost')
        cursor=db.cursor()
	if request.GET.get("partition")=="0":
        	sql = ('select c,soc_name from (select count(soc_name) as c,soc_name from h1bBubble where case_status=%s group by soc_name) t order by c desc limit 10')
        	cursor.execute(sql,("CERTIFIED",))
        elif request.GET.get("partition") == "1":
                sql = ("select c,soc_name from (select count(soc_name) as c,soc_name from h1bTest where case_status=%s AND year = %s group by soc_name) t order by c desc limit 10")
                cursor.execute(sql,("CERTIFIED",2016))
        elif request.GET.get("partition") == "2":
                sql = ("select c,soc_name from (select count(soc_name) as c,soc_name from h1bTest where case_status=%s AND year = %s group by soc_name) t order by c desc limit 10")
                cursor.execute(sql,("CERTIFIED", 2015))

	res = cursor.fetchall()
        res = list(res)
        j = 0
        for j in range(10):
                res[j] = list(res[j])
        i = 0
        for i in range(10):
                res[i][0] = str(res[i][0])
                res[i][1] = str(res[i][1])
        k = 0
        for k in range(10):
                res[k] = tuple(res[k])
        res = tuple(res)
        #res = str(res)
        return render(request, "Visual2.html", {"res": res})

def companybubble(request):
        db = MySQLdb.connect(user='root', db='H1B_DB', passwd='', host='localhost')
        cursor=db.cursor()
	if request.GET.get("partition") == "0":
        	sql = ('select c,employer_name from (select count(employer_name) as c,employer_name from h1bBubble where case_status=%s group by employer_name) t order by c desc limit 10')
		cursor.execute(sql,("CERTIFIED",))
	elif request.GET.get("partition") == "1":
		sql = ("select c,employer_name from (select count(employer_name) as c,employer_name from h1bTest where case_status=%s AND year = %s group by employer_name) t order by c desc limit 10")
		cursor.execute(sql,("CERTIFIED",2016))
	elif request.GET.get("partition") == "2":
		sql = ("select c,employer_name from (select count(employer_name) as c,employer_name from h1bTest where case_status=%s AND year = %s group by employer_name) t order by c desc limit 10")
		cursor.execute(sql,("CERTIFIED", 2015))
        # cursor.execute(sql,("CERTIFIED",))
        res = cursor.fetchall()
        res = list(res)
        j = 0
        for j in range(10):
                res[j] = list(res[j])
        i = 0
        for i in range(10):
                res[i][0] = str(res[i][0])
                res[i][1] = str(res[i][1])
        k = 0
        for k in range(10):
                res[k] = tuple(res[k])
        res = tuple(res)
        return render(request, "Visual3.html", {"res": res})


def MakePredictions(request):
	soc=request.GET.get("jobtitle",None)
	#year=request.GET.get("year",None)
	state=request.GET.get("state",None)
	#city=request.GET.get("city",None)
	wage=request.GET.get("wage",None)
	fulltime=request.GET.get("fulltime",None)
	degree = request.GET.get("degree")
	#soc = soc.upper()
	val = 0
	if degree == "1":
		val = 0.06
	elif degree == "2":
		val = 0.30
	elif degree == "6":
		val = 0.24
	else:
		val = 0.56	
	
	if len(soc)==0 or soc is None:
                return render(request,"Prediction.html",{"SocNotFound":"Sorry, you are not supposed to enter empty job title."})
	if len(wage)==0 or wage is None:
		return render(request,"Prediction.html",{"WageNotFound":"Sorry, please enter your wage."})
	wg=float(str(wage))
	ft=float(str(fulltime))
	#input=np.zeros(shape=(1,5),dtype=float)
	#X=np.array([50000,2016,1,100,100]).reshape(1,5)
	
	#lr = joblib.load("/opt/djangoproject/H1B_DB/H1B_DB/lr.pkl")
	#preds_lr = lr.predict_proba(X)
	#random forest
	#rfc = joblib.load("/opt/djangoproject/H1B_DB/H1B_DB/rfc.pkl")
	#preds_rfc = rfc.predict_proba(X)
	#NN
	#nnc = joblib.load("/opt/djangoproject/H1B_DB/H1B_DB/nn.pkl")
	#preds_nnc = nnc.predict_proba(X)

	#XGB

    	#gbc = joblib.load("/opt/djangoproject/H1B_DB/H1B_DB/gbc.pkl")
	#preds_gbc = gbc.predict_proba(X)
	state_name = np.load('/opt/djangoproject/H1B_DB/H1B_DB/state_name.npy')
	soc_name = np.load('/opt/djangoproject/H1B_DB/H1B_DB/soc_name.npy')

	#'full time','soc_id','state_id','wage'
	#X = np.array([sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	#soc_use = int(np.where(soc_name == soc)[0])
	
	checkSoc=np.where(soc_name == soc)[0]
	checkState=np.where(state_name == state)[0]
	
	if len(checkSoc)==0:
		return render(request,"Prediction.html",{"SocNotFound":"Sorry, your input job title is not valid, please replace it with a correct one."})
	else:
                soc_use = float(checkSoc)
       		state_use = float(checkState)

		X = np.array([ft, soc_use,  state_use, wg]).reshape((1, 4))

	#logistic Regression
		lr = joblib.load("/opt/djangoproject/H1B_DB/H1B_DB/lr.pkl")
		preds_lr = lr.predict_proba(X)

	#NN
		nnc = joblib.load("/opt/djangoproject/H1B_DB/H1B_DB/nn.pkl")
		preds_nnc = nnc.predict_proba(X)

	#print(statistics.mode([preds_lr, preds_rfc, preds_nnc, preds_gbc]))

		result=np.zeros(shape=(1,5),dtype=float)

	#result=(preds_lr + preds_rfc + preds_nnc + preds_gbc)/4
		result=(preds_lr+preds_nnc)/2
		output=np.zeros(shape=(1,5),dtype=float)

		for i in range(4):

			output[0][i]=result[0][i+1];

		output[0][0]+=result[0][0];
	#result=pr.calculation(input)
		out=[0.0,0.0,0.0,0.0,1-val]
		out2 = [0.0,0.0,0.0,0.0]
		for i in range(4):
			out[i]=output[0][i]*val
			out2[i]=output[0][i]
		return render(request,"Prediction.html",{"predResult":out, "Afterlottery":out2})
	#return HttpResponse(str(out))




