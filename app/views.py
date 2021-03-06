from flask import render_template,request , redirect
from flask import send_file , render_template, request, session, redirect, url_for
from app import app
import os
from pandas.io.json import json_normalize as norm
import pandas as pd
import glob
import os
import pandas as pd
from pandas import read_csv , merge
from pandas import read_excel
from pandas import concat
from glob import iglob

app.config["SECRET_KEY"] = 'FEfUCijY_DbgJS4reeiD0Q'



@app.route('/')
def index():
	#return render_template('index.html')
	session.pop("USERNAME", None)
	return redirect(url_for("sign_in"))



import os
Path_here = os.path.dirname(os.path.abspath(__file__))
print(Path_here)
from os import path , makedirs
if not path.exists(Path_here+'/templates/upload_csv/'):
	makedirs(Path_here+'/templates/upload_csv/')
	print("Done")

app.config["IMAGE_UPLOADS"] =os.path.join(Path_here+ "/templates/upload_csv/")
print(app.config["IMAGE_UPLOADS"])

print(app.config["IMAGE_UPLOADS"])
@app.route('/before', methods=["GET", "POST"])

def before_testing():
	if not session.get("USERNAME") is None:
		if request.method == "POST":
			if request.files:
				image = request.files["xlsx"]
				if image.filename == "":
					print("No filename")
					return redirect(request.url )

				else:
					excel_file =os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
					image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
					csv = str(image.filename).replace('.xlsx','_To_Be_Tested.csv' )
					csv_file  = excel_file.replace('.xlsx','_To_Be_Tested.csv' )
					df1=pd.read_excel(excel_file ,encoding='utf8' )
					df2 =  pd.read_excel(excel_file ,encoding='utf8' )
					del df1['Email']
					df1 = df1.rename(index=str, columns={"Personal Email": "Email"})
					del df2['Personal Email']
					df1['WP_ID'] = [str(x).zfill(5) +"P" for x  in range(1, len(df1)+1)]
					df1 = df1.reset_index(drop=True)
					df2['WP_ID'] = [str(x).zfill(5) +"W" for x  in range(1, len(df2)+1)]
					df2 = df2.reset_index(drop=True)
					df = pd.concat([df1, df2] )
					df = df.sort_values(by=['WP_ID'])
					df = df[~df['Email'].isnull()] 
					df.to_csv(csv_file , index = False , encoding='utf8' )
					return send_file(csv_file,
									mimetype='text/csv',
									attachment_filename=csv,
									as_attachment=True)
					#print('csv saved')
					return redirect(request.url )


		return render_template('before_testing.html')
	else:
		return redirect(url_for("sign_in"))

@app.route('/after', methods=["GET", "POST"])
def after_testing():
	if not session.get("USERNAME") is None:

		if request.method == "POST":
			if request.files:
				image = request.files["csv"]
				if image.filename == "":
					print("No filename")
					return redirect(request.url)

				else:
					csv_file =os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
					image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
					excel=str(image.filename).replace('.csv','_Filter_Done.xlsx')
					excel_file=csv_file.replace('.csv','_Filter_Done.xlsx')

					df=read_csv(csv_file ,encoding='utf8' )
					df_all = read_csv(csv_file ,encoding='utf8' )
					df_all['WP_ID'] = df_all['WP_ID'].map(lambda x: str(x)[:-1])
					df_all = df_all.drop_duplicates(['WP_ID'], keep='last')
					del df_all['Email']
					del df_all['Status']
					del df_all['Details']
					try:
						del df_all['num']
					except:pass
					df1 = df[df['WP_ID'].str.contains("P")]
					aaP=df1[df1['Details'].str.contains("The address passed all tests.")]
					bbP=df1[df1['Details'].str.contains("None.")]
					ccP=df1[df1['Details'].str.contains("Greylisting is active on this server.")]
					df1 = pd.concat([aaP,bbP,ccP] )
					df1 = df1.rename(index=str, columns={"Email": "Personal Email" ,'Status':'Status_P','Details':'Details_P'})
					df1['WP_ID'] = df1['WP_ID'].map(lambda x: str(x)[:-1])
					df1 = df1[['WP_ID','Personal Email','Status_P','Details_P']]
					df2 = df[df['WP_ID'].str.contains("W")]
					aaW=df2[df2['Details'].str.contains("The address passed all tests.")]
					bbW=df2[df2['Details'].str.contains("None.")]
					ccW=df2[df2['Details'].str.contains("Greylisting is active on this server.")]
					df2 = pd.concat([aaW, bbW,ccW] )
					df2 = df2.rename(index=str, columns={'Status':'Status_W','Details':'Details_W'})
					df2['WP_ID'] = df2['WP_ID'].map(lambda x: str(x)[:-1])
					df2 = df2[['WP_ID','Email','Status_W','Details_W']]
					df_final = pd.merge(pd.merge(df_all,df1,on='WP_ID' , how = 'left'),df2,on='WP_ID' , how = 'left')
					df_final = df_final.sort_values(by=['WP_ID'])
					df_final = df_final[(~df_final['Email'].isnull())|(~df_final['Personal Email'].isnull())]
					df_final.to_excel(excel_file ,encoding='utf8' )
					

					return send_file(excel_file,
									mimetype='text/csv',
									attachment_filename=excel,
									as_attachment=True)
					#print('csv saved')
					return redirect(request.url )

		return render_template('after_testing.html')
	else:
		return redirect(url_for("sign_in"))

users = {
    "basem": {
        "username": "basem",
        "email": "julian@gmail.com",
        "password": "basem22",
        "bio": "Some guy from the internet"
    },
    "hesham": {
        "username": "hesham",
        "email": "clarissa@icloud.com",
        "password": "hesham10",
        "bio": "Sweet potato is life"
    }
}


@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
	if request.method == "POST":
		req = request.form
		username = req.get("username")
		password = req.get("password")
		if not username in users:
			print("Username not found")
			return redirect(request.url)
		else:
			user = users[username]

		if not password == user["password"]:
			print("Incorrect password")
			return redirect(request.url)
		else:
			session["USERNAME"] = user["username"]
			print("session username set")
			return redirect(url_for("before_testing"))

	return render_template("sign_in.html")

@app.route("/sign-out")
def sign_out():

	session.pop("USERNAME", None)

	return redirect(url_for("sign_in"))
