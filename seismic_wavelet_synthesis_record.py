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
                self.col = 0
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
                t_list = []
                dt = 0.01
                for i in range(self.row-1):
                        if i == 0:

                                t_list.append(self.depth[i]/self.velocity[i])
                        else:
                                t_list.append((self.depth[i]-self.depth[i-1])/self.velocity[i]+t_list[-1])
                reflection_c_s=np.zeros(round(t_list[-1]/dt)+1)
                for i in range(len(self.reflection_coefficient_sequence)):
                        reflection_c_s[round(t_list[i]/dt)] = self.reflection_coefficient_sequence[i]
                fm = 50
                r = 6
                ricker = []
                result = []
                for i in range(200):
                        ricker.append(math.exp(-(2*math.pi*fm/r)**2*(i*dt)**2)*math.sin(2*math.pi*fm*i*dt))
                result = np.convolve(reflection_c_s,ricker)
                T = np.array(range(len(result)))
                power = np.array(result)
                xnew = np.linspace(T.min(),T.max(),300) 
                power_smooth = spline(T,power,xnew)
                plt.plot(xnew,power_smooth)
                plt.title("ricker_synthesis_graph")
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
                t_list = []
                dt = 0.01
                for i in range(self.row-1):
                        if i == 0:

                                t_list.append(self.depth[i]/self.velocity[i])
                        else:
                                t_list.append((self.depth[i]-self.depth[i-1])/self.velocity[i]+t_list[-1])
                reflection_c_s=np.zeros(round(t_list[-1]/dt)+1)
                for i in range(len(self.reflection_coefficient_sequence)):
                        reflection_c_s[round(t_list[i]/dt)] = self.reflection_coefficient_sequence[i]
                fm = 50
                r = 6
                ricker = []
                result = []
                for i in range(200):
                        ricker.append(math.exp(-(2*math.pi*fm/r)**2*(i*dt)**2)*math.sin(2*math.pi*fm*i*dt))
                result = np.convolve(reflection_c_s,ricker)
                T = np.array(range(len(result)))
                power = np.array(result)
                xnew = np.linspace(T.min(),T.max(),300) 
                power_smooth = spline(T,power,xnew)


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
                plt.subplot(121)
                plt.plot(v1,d1,'r')
                plt.subplot(122)
                plt.plot(xnew,power_smooth,'b')
                plt.show()



        



if __name__ == "__main__":
        a=synthetic_seismic_record("/home/xxx/documents/data.xlsx")
        # a.depth_velocity_graph()
        # a.ricker_synthesis_graph()
        a.all_graph()
