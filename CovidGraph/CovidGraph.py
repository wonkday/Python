import covid
import matplotlib.pyplot as plt

#change@1 - show abs value in pie
import numpy

#create instance
cov = covid.Covid()
name = input("Enter Country name:")
virusdata = cov.get_status_by_country_name(name)
active = virusdata['active']
recovered = virusdata['recovered']
deaths = virusdata['deaths']

arr_virusdata = numpy.array([active,recovered,deaths])
arr_labels = ['Active','Recovered','Deaths']
arr_colors=['b','g','r']

#change@1
def absolute_value(val):
    a  = arr_virusdata[ numpy.abs(arr_virusdata - val/100.*arr_virusdata.sum()).argmin() ]
    return a

#change@2
def abs_value_n_perct(val):
    #a  = arr_virusdata[ numpy.abs(arr_virusdata - val/100.*arr_virusdata.sum()).argmin() ]
    #a = '{:.4f}%\n({:.0f})'.format(val, total*val/100)
    a = '{:.1f}%\n({:.0f})'.format(val, absolute_value(val))
    return a

#plt.pie(,labels=arr_lables,colors=arr_colors,explode=(0,0,0.2),startangle=180,autopct='%1.1f%%',shadow=True)

#change@1
#plt.pie(arr_virusdata,labels=arr_labels,colors=arr_colors,explode=(0,0,0.2),startangle=180,autopct=absolute_value,shadow=True)

#change@2
plt.pie(arr_virusdata,labels=arr_labels,colors=arr_colors,explode=(0,0,0.2),startangle=180,autopct=abs_value_n_perct,shadow=True)

plt.title(name)
plt.legend()
plt.show()
