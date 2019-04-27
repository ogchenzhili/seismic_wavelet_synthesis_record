import matplotlib.pyplot as plt
import numpy as np
import xlrd
import math
from scipy.interpolate import spline
class synthetic_seismic_record():


        def __init__(self,filename):
                self.filename=filename
                self.depth = []
                self.density = []
                self.velocity = []
                self.row = 0
                self.reflection_coefficient_sequence = []
                self.acquire_data()


        def acquire_data(self):        
                files = xlrd.open_workbook(self.filename)
                sheet1 = files.sheet_by_name("Sheet1")
                self.row=sheet1.nrows-1
                self.col=sheet1.ncols 
                for i in range(1,self.row+1):            
                        self.depth.append(sheet1.col_values(0)[i])
                        self.density.append(sheet1.col_values(1)[i])
                        self.velocity.append(sheet1.col_values(2)[i])
                for i in range(0,self.row-1):
                        pv2 = self.density[i+1]*self.velocity[i+1]
                        pv1 = self.density[i]*self.velocity[i]
                        self.reflection_coefficient_sequence.append((pv2-pv1)/(pv1+pv2))


        def ricker_synthesis_graph(self):
                #雷克子波抽样
                fm = 50
                dt = 0.001
                r = 4
                ricker = []
                for i in range(100):
                        ricker.append(math.exp(-(2*math.pi*fm/r)**2*(i*dt)**2)*math.cos(2*math.pi*fm*i*dt))
                #反射系数
                t_list = []
                for i in range(self.row-1):
                        if i == 0:
                                t_list.append(2*(self.depth[i]/self.velocity[i]))
                        else:
                                t_list.append(2*((self.depth[i]-self.depth[i-1])/self.velocity[i])+t_list[-1])
                reflection_c_s=np.zeros(round(t_list[-1]/dt)+1)
                for i in range(len(self.reflection_coefficient_sequence)):
                        reflection_c_s[round(t_list[i]/dt)] = self.reflection_coefficient_sequence[i]

                #卷积
                result = np.convolve(reflection_c_s,ricker)
                #作图
                T = np.array(range(len(result)))
                power = np.array(result)
                xnew = np.linspace(T.min(),T.max(),300) 
                power_smooth = spline(T,power,xnew)
                plt.plot(xnew,power_smooth)
                plt.show()

                
        def depth_velocity_graph(self):
                d1 = []
                v1 = []
                for i in range(self.row-1):
                        if i==0:
                                d1.append(0)
                                d1.append(-self.depth[i])
                        else:
                                d1.append(-self.depth[i-1])
                                d1.append(-self.depth[i])                       
                        v1.append(self.velocity[i])
                        v1.append(self.velocity[i])
                plt.plot(v1,d1)
                plt.title("depth-velocity")
                plt.show()

        
        def all_graph(self):
                #速度深度图
                d1 = []
                v1 = []
                for i in range(self.row-1):
                        if i==0:
                                d1.append(0)
                                d1.append(-self.depth[i])
                        else:
                                d1.append(-self.depth[i-1])
                                d1.append(-self.depth[i])                       
                        v1.append(self.velocity[i])
                        v1.append(self.velocity[i])
                #雷克子波抽样
                fm = 50
                dt = 0.001
                r = 4
                ricker = []
                for i in range(100):
                        ricker.append(math.exp(-(2*math.pi*fm/r)**2*(i*dt)**2)*math.sin(2*math.pi*fm*i*dt))
                #反射系数
                t_list = []
                for i in range(self.row-1):
                        if i == 0:

                                t_list.append(2*(self.depth[i]/self.velocity[i]))
                        else:
                                t_list.append(2*((self.depth[i]-self.depth[i-1])/self.velocity[i])+t_list[-1])
                reflection_c_s=np.zeros(round(t_list[-1]/dt)+1)
                for i in range(len(self.reflection_coefficient_sequence)):
                        reflection_c_s[round(t_list[i]/dt)] = self.reflection_coefficient_sequence[i]

                #卷积
                result = np.convolve(reflection_c_s,ricker)
                #作图
                T = np.array(range(len(result)))
                power = np.array(result)
                xnew = np.linspace(T.min(),T.max(),300) 
                power_smooth = spline(T,power,xnew)

                plt.subplot(223)
                plt.plot(v1,d1,'r')
                plt.subplot(221)
                plt.plot(ricker)
                plt.subplot(222)
                plt.stem(ricker)
                plt.subplot(224)
                plt.plot(xnew,power_smooth,'b')
                plt.show()


if __name__ == "__main__":
        a=synthetic_seismic_record("/home/xxx/documnts/data.xlsx")
        # a.depth_velocity_graph()
        # a.ricker_synthesis_graph()
        a.all_graph()
