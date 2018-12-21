import flask
import numpy as np
from sklearn.externals import joblib 
import pickle 
import pandas as pd
import datetime

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
def init():
	global lb_week,lb_month,ohe_week,ohe_month,model
    # load the pre-trained Keras model
#    model = joblib.load('regressor_13_10_2018')
	lb_week = joblib.load('lb_week_14_10_2018.pkl') 
	lb_month = joblib.load('lb_month_14_10_2018.pkl') 
	ohe_week = joblib.load('ohe_week_14_10_2018.pkl') 
	ohe_month = joblib.load('ohe_month_14_10_2018.pkl') 
	model = joblib.load('RFR_14_10_2018.pkl') 
	app.run(host = '0.0.0.0',threaded=True)

@app.route('/')
async def home(request):
  return web.json_response({'status':'ok'})



# API for prediction
@app.route("/predict", methods=["GET"])
def predict():
#	nameOfTheCharacter = flask.request.args.get('name')
	parameters, formatted_z = getParameters()
	nameOfTheCharacter='Work load for Week:' + str(formatted_z)
	print(type(parameters))
	print(parameters)
	dataframe = pd.DataFrame([parameters], columns=['Week_Number','Mon_Value'])
	print(dataframe)
	dataframe["Week_Number"]  = lb_week.transform(dataframe["Week_Number"])
	dataframe["Mon_Value"]  = lb_month.transform(dataframe["Mon_Value"])
	X = ohe_week.transform(dataframe.Week_Number.values.reshape(-1,1)).toarray()
	print(X.shape)
	Y = ohe_month.transform(dataframe.Mon_Value.values.reshape(-1,1)).toarray()
	print(Y.shape)
	dfOneHot_week = pd.DataFrame(X, columns = ["Week_Number_"+str(int(i)) for i in range(X.shape[1])])
	dfOneHot_mn = pd.DataFrame(Y, columns = ["Month_"+str(int(i)) for i in range(Y.shape[1])])
	df = pd.concat([dataframe, dfOneHot_week], axis=1)
	df = pd.concat([df, dfOneHot_mn], axis=1)
	df =df.drop('Week_Number',axis=1)
	df =df.drop('Mon_Value',axis=1)
	print(df.shape)
	print(list(df))
	t = int(model.predict(df))
#	inputFeature = np.asarray(parameters).reshape(1, 2)
#	print(inputFeature)
#    inputFeature = np.asarray(parameters).reshape(1, 12)
#    scaler = sc.transform(inputFeature)
#    print(inputFeature)
#    print(scaler)
#    print(scaler.shape)
#    from sklearn.preprocessing import StandardScaler
#    sc = StandardScaler()
#    inputFeature = sc.transform(inputFeature)
#    with graph.as_default():
#       raw_prediction = model.predict(scaler)[0][0]
#       print(raw_prediction)
##    if raw_prediction > 0.5:
 #       prediction = 'Delayed'
 #   else:
 #       prediction = 'Not Delayed'
	return sendResponse({nameOfTheCharacter: t})
	
#	return  sendResponse(t)
	
# Getting Parameters
def getParameters():
	global formatted_z
	m = ''
	parameters = []
	intial_t = flask.request.args.get('Date')
	formatted_z = datetime.datetime.strptime(intial_t, '%Y-%m-%d').isocalendar()[1]
	z = "Week_" +str(formatted_z)
	print(type(z))
	parameters.append(z)
	if (z == 'Week_1' or z == 'Week_2' or z=='Week_3' or z == 'Week_4' or z =='Week_5'):
		m = 'Jan'
	elif (z == 'Week_6' or z == 'Week_7' or z=='Week_8' or z == 'Week_9'):
		m = 'Feb'
	elif (z == 'Week_10' or z == 'Week_11' or z=='Week_12' or z == 'Week_13'):
		m = 'Mar'	
	elif (z == 'Week_14' or z == 'Week_15' or z=='Week_16' or z == 'Week_17' or z == 'Week_18'):
		m = 'April'	
	elif (z == 'Week_19' or z == 'Week_20' or z=='Week_21' or z == 'Week_22'):
		m = 'May'	
	elif (z == 'Week_23' or z == 'Week_24' or z=='Week_25' or z == 'Week_26'):
		m = 'June'	
	elif (z == 'Week_27' or z == 'Week_28' or z=='Week_29' or z == 'Week30' or z=='Week_31'):
		m = 'July'	
	elif (z == 'Week_32' or z == 'Week_33' or z=='Week_34' or z == 'Week_35'):
		m = 'Aug'
	elif (z == 'Week_36' or z == 'Week_37' or z=='Week_38' or z == 'Week_39'):
		m = 'Sept'
	elif (z == 'Week_40' or z == 'Week_41' or z=='Week_42' or z == 'Week_43' or z == 'Week_44'):
		m = 'Oct'
	elif (z == 'Week_45' or z == 'Week_46' or z=='Week_47' or z == 'Week_48'):
		m = 'Nov'
	elif (z == 'Week_49' or z == 'Week_50' or z=='Week_51' or z == 'Week_52'):
		m = 'Dec'
#    parameters.append(flask.request.args.get('Month')) 
	parameters.append(m)
	return parameters , formatted_z

# Cross origin support
def sendResponse(responseObj):
    response = flask.jsonify(responseObj)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    response.headers.add('Access-Control-Allow-Headers', 'accept,content-type,Origin,X-Requested-With,Content-Type,access_token,Accept,Authorization,source')
    response.headers.add('Access-Control-Allow-Credentials', True)
    return response

# if this is the main thread of execution first load the model and then start the server
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."        
    "please wait until server has fully started"))
    init()
#    app.run(threaded=True)
