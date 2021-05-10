from tkinter import *
from functools import partial
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

#-------------------------------------------------GUI-------------------------------------------------------------------#
df = []
col_name = []
combosA = []
combosB = []
buttons = []
labels = []
i = 1

window = Tk()
window.resizable(False, False)

fontStyle = tkFont.Font(family="Lucida Grande", size=12)
fontStyle1 = tkFont.Font(family="Lucida Grande", size=10)



window.geometry("550x700")
window.title("Monopolistic Market Predictor")
txt = Entry(window,width=70)

txt.place(x = 10, y =10)
def browseFiles():
    filename = filedialog.askopenfilename(title = "Select a File",
                                          filetypes = (("Excel files",
                                                        "*.xls*"),
                                                       ))
    txt.insert(END,filename)

    global df
    global col_name
    inputvalue = txt.get()
    df = pd.read_excel(inputvalue, sheet_name='Orders')
    df.drop(['Order ID','Row ID','Ship Date','Customer ID','Customer Name','Shipping Cost','Postal Code'],axis =1, inplace=True)
    col_name = list(df.columns)
    initialize_dmbi()
    
    
    
#Browse Files Button
button1 = Button(window,text = "Browse Files", command = browseFiles)
button1.place(x = 440, y = 10)#browse button

button2 = Button(window, text = "Add Label", command=lambda: new_label())
button2.place(x = 100, y = 45)#add label button

button3 = Button(window, text = "Check", command=lambda: calculate_result())
button3.place(x = 310, y = 45)#add label button


labelz = Label(window, text = '|| Probablity of Sales will be ||',font = fontStyle)
labelz.place(x = 120, y=80)
labelz1 = Label(window, text = '1. Naive Bayes Classification :  ',font = fontStyle1)
labelz1.place(x = 120, y=100)
labelz2 = Label(window, text = '2. K - Nearest Neighbours      :  ',font = fontStyle1)
labelz2.place(x = 120, y=120)


  
def selected_value(index):
    global df
    
    selectvalue = globals()['combo%sA',str(index)].get()
    unique_value = list(df[selectvalue].unique())
    globals()['combo%sB',str(index)]['values'] = unique_value
    


def new_label():
    global i
    global col_name
    globals()['labels%s',str(i)] = Label(window, text = 'Label' + str(i))
    labels.append('lables'+str(i))
    globals()['labels%s',str(i)].place(x = 40, y = (140*i)+(20*(i-1)))
    
    globals()['combo%sA',str(i)] = Combobox(window)
    combosA.append('combo'+str(i)+'A')
    globals()['combo%sA',str(i)].place(x = 40, y = 160*i)
    globals()['combo%sA',str(i)]['values'] = col_name

    globals()['buttons%s',str(i)] = Button(window, text = "Done", command= partial(selected_value,i))
    buttons.append('buttons'+str(i))
    globals()['buttons%s',str(i)].place(x = 200, y = 160*i)

    globals()['combo%sB',str(i)] = Combobox(window)
    combosB.append('combo'+str(i)+'B')
    globals()['combo%sB',str(i)].place(x = 300, y = 160*i)
    
    i= i+1


#-------------------------------------------------DMBI-------------------------------------------------------------------#
def initialize_dmbi():

    global df
    global sp_ctrl
    global sp_r

    
    quantity = ctrl.Antecedent(np.arange(df['Quantity'].min(), df['Quantity'].max()+1, 1), 'Quantity')
    discount = ctrl.Antecedent(np.arange(df['Discount'].min(), df['Discount'].max()+0.05, 0.05), 'Discount')
    sp = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'SalesPerformance')


    quantity['low'] = fuzz.trimf(quantity.universe, [df['Quantity'].min(), df['Quantity'].min(),int((df['Quantity'].min()+df['Quantity'].max())/2)])
    quantity['medium'] = fuzz.trimf(quantity.universe, [df['Quantity'].min(), int((df['Quantity'].min()+df['Quantity'].max())/2), df['Quantity'].max()])
    quantity['high'] = fuzz.trimf(quantity.universe, [int((df['Quantity'].min()+df['Quantity'].max())/2), df['Quantity'].max(), df['Quantity'].max()])
        
    
    discount['low'] = fuzz.trimf(discount.universe, [df['Discount'].min(), df['Discount'].min(),int((df['Discount'].min()+df['Discount'].max())/2)])
    discount['medium'] = fuzz.trimf(discount.universe, [df['Discount'].min(), int((df['Discount'].min()+df['Discount'].max())/2), df['Discount'].max()])
    discount['high'] = fuzz.trimf(discount.universe, [int((df['Discount'].min()+df['Discount'].max())/2), df['Discount'].max(), df['Discount'].max()])

    sp['low'] = fuzz.trimf(sp.universe, [0, 0, 0.5])
    sp['medium'] = fuzz.trimf(sp.universe, [0, 0.5, 1])
    sp['high'] = fuzz.trimf(sp.universe, [0.5, 1, 1])

    rule1 = ctrl.Rule(quantity['low'] & discount['low'], sp['low'])
    rule11 = ctrl.Rule(quantity['low'] & discount['medium'], sp['low'])
    rule12 = ctrl.Rule(quantity['low'] & discount['high'], sp['medium'])

    rule2 = ctrl.Rule(quantity['medium'] & discount['low'], sp['medium'])
    rule21 = ctrl.Rule(quantity['medium'] & discount['medium'], sp['medium'])
    rule22 = ctrl.Rule(quantity['medium'] | discount['high'], sp['high'])

    rule3 = ctrl.Rule(quantity['high'], sp['high'])
    
    
    sp_ctrl = ctrl.ControlSystem([rule1, rule11, rule12, rule2, rule21, rule22, rule3])
    
    sp_r = ctrl.ControlSystemSimulation(sp_ctrl)
        
    df['Sales Performance'] = df.apply(calc_performance,axis = 1)

    #writer = ExcelWriter('Pandas-Example2.xlsx')
    #df.to_excel(writer,'Sheet1',index=False)
    #writer.save()


def calc_performance(x):

    global sp_ctrl
    global sp_r

    
    sp_r.input['Quantity'] = x['Quantity']
    sp_r.input['Discount'] = x['Discount']
    sp_r.compute()
    if sp_r.output['SalesPerformance'] < (1/3):
        return 'Poor'
    elif sp_r.output['SalesPerformance'] < (2/3):
        return 'Average'
    else:
        return 'Good'

def calculate_result():
    val1 = calculate_NBC_result()
    val2 = calculate_kMeans_result()
    labelz1.configure(text ="1. Naive Bayes Classification :  "+val1)
    labelz2.configure(text ="2. K - Nearest Neighbours     :  "+val2)

def calculate_NBC_result():
    global df
    global i

    good_prob = len(df[df['Sales Performance'] == 'Good'])/len(df)
    avg_prob = len(df[df['Sales Performance'] == 'Average'])/len(df)
    poor_prob = len(df[df['Sales Performance'] == 'Poor'])/len(df)

    print(good_prob,avg_prob,poor_prob)


    for x in range(1,i):
        good_prob = good_prob * ((len(df[(df[globals()['combo%sA',str(x)].get()] == globals()['combo%sB',str(x)].get()) & (df['Sales Performance'] == 'Good')]))/len(df[df['Sales Performance'] == 'Good']))
        avg_prob = avg_prob * ((len(df[(df[globals()['combo%sA',str(x)].get()] == globals()['combo%sB',str(x)].get()) & (df['Sales Performance'] == 'Average')]))/len(df[df['Sales Performance'] == 'Average']))
        poor_prob = poor_prob * ((len(df[(df[globals()['combo%sA',str(x)].get()] == globals()['combo%sB',str(x)].get()) & (df['Sales Performance'] == 'Poor')]))/len(df[df['Sales Performance'] == 'Poor']))

    if good_prob > avg_prob and good_prob > poor_prob:
        return "Good"
    elif avg_prob > poor_prob:
        return "Average"
    else:
        return "Poor"

def calculate_kMeans_result():

    global df
    global i

    cols = list(df.columns)
    d = {}



    for x in range(1,i):
        cols.remove(globals()['combo%sA',str(x)].get())
        d[globals()['combo%sA',str(x)].get()] = globals()['combo%sB',str(x)].get()
        #cols.remove([globals()['combo%sA',str(x)].get()])
    cols.remove("Sales Performance")
    # print(cols)
    # print(d)
    temp_df = df.drop(cols, axis = 1)
    print(temp_df.shape)
    temp_df = temp_df.append(d, ignore_index=True)
    print(temp_df.shape)
    object_cols = list(temp_df.select_dtypes(['object']).columns)

    le = LabelEncoder()

    for x in object_cols:
        if x == 'Sales Performance':
            d = temp_df.tail(1)
            d.drop('Sales Performance', axis = 1, inplace = True)
            print(d)
            temp_df = temp_df[:-1]
        temp_df[x] = le.fit_transform(temp_df[x])
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(temp_df.iloc[:,:-1],temp_df.iloc[:,-1])
    y = knn.predict(d)
    print(y)
    d['Sales Performance'] = y
    temp_df = temp_df.append(d, ignore_index=True)
    temp_df['Sales Performance'] = le.inverse_transform(temp_df['Sales Performance'])

    d = temp_df.tail(1)['Sales Performance']
    print(d.iloc[0])

    return d.iloc[0]
        
#-------------------------------------------------DMBI-------------------------------------------------------------------#


#-------------------------------------------------GUI-------------------------------------------------------------------#

window.mainloop()

#-------------------------------------------------GUI-------------------------------------------------------------------#
