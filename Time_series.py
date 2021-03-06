class TimeSeries(object):
    '''Docstrings look like this and describe
    what the class or method does'''
    def __init__(self, data):
        self.data = data
    
    def get(self, x):
        '''Find the corresponding y-value when given an x-value'''
        if x in self.data:
            return self.data[x]
        
        raise Exception("Didn't find the value")
    
    def view(self):
        # blah blah blah
        pass
    

class StepFunctionTimeSeries(TimeSeries):
    def get(self, x):
        '''Given an X value, get the corresponding Y value.
        
        Uses step interpolation (gets the Y value of the nearest X point)'''
        
        if x in self.data: return self.data[x]
        
        closest_point = None
        for (xi, yi) in self.data.items():
            if closest_point is None:
                closest_point = (xi, yi)
            else:
                cx, cy = closest_point
                if abs(xi-x) < abs(cx-x):
                    closest_point = (xi, yi)
        return closest_point[1]
        

class LinearTimeSeries(TimeSeries):
    def __init__(self, data):
        TimeSeries.__init__(self, data)
        self.data.sort()
    
    def get(self, x):
        if x in self.data: return self.data[x]
        
        data_list = self.data.items()
        
        # if it's out of range to the left,
        # return the first value
        if x < data_list[0][0]:
            return data_list[0][1]
        # if it's out of range to the right,
        # return the last value
        elif x > data_list[-1][0]:
            return data_list[-1][1]
        # otherwise, it's within the range
        for (n, (xi, yi)) in enumerate(data_list):
            if xi == x:
                return yi
            elif xi > x:
                n1, n2 = n-1, n
                x1, x2 = data_list[n1][0], data_list[n2][0]
                y1, y2 = data_list[n1][1], data_list[n2][1]
                d1, d2 = abs(x-x1), abs(x-x2)
                total_weight = float(d1 + d2)
                w1 = y1 * (total_weight-d1) / total_weight
                w2 = y2 * (total_weight-d2) / total_weight
                return w1 + w2 