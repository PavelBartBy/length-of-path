from pathlib import Path
import csv
import math
import functools as func


class IInterface(object):
    """Interface class with usable methods"""
    def read(self):
        """read from some file"""

class CSVReader(IInterface):
    
    def __eq__(self, value):
        if value.isdigit()==True:
            pass
        else:
            print (value)
            raise Exception("One or more wrong coordinates")

    def validation(self,row):
        for i in row:
            self.__eq__(i)

    def read(self, file_name):
        """
        :param file_name: include file location and file name
        :return: array of coordinates from file
        """
        coordinates=[]  
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count==0:
                    line_count+=1
                else:
                    self.validation(row)
                    coordinates.append(([row[0]])+[row[1]])  #gives us array list
                    line_count+=1
        return coordinates


class ReadersFactory (IInterface):
    """ 
    Can choose Reader for file;
    :param file_name: include file location and file name
    :return: array of coordinates from file
    """

    def read(self,file_name):
        readers_dict={ '.csv': CSVReader()
                       #,'.txt': TXTReader()
                       }
        file_extension=Path(file_name).suffix
        for i,j in readers_dict.items():
            if i==file_extension:
                coordinates=j.read(file_name)
        return coordinates

class Point:
    """One point with coordinates"""
    def __init__(self,x,y):
        self.x=int(x)
        self.y=int(y)
    

class Route:

    def __init__(self, array_of_coordinates):
        self.array_of_coordinates=array_of_coordinates

    def create_points(self,array_of_coordinates):
        """ 
        Create list of points: Point object;
        :param array_of coordinates: coordinates from file
        :return: list of points
        """   
        point_list=[]
        for row in array_of_coordinates:
            point_list.append(Point(row[0],row[1]))
        return point_list
    
    @staticmethod
    def section_calculate(point1,point2):
        """ 
        Calculate length one section between two points;
        :param point1: point of start section
        :param point1: point of finish section
        :return: section length
        """   
        section_length=math.sqrt((point1.x-point2.x)**2+(point1.y-point2.y)**2)
        return math.ceil(section_length)
    
    def create_sections(self,point_list):
        """ 
        Create list of length sections: int;
        :param point_list: list of points: Point object
        :return: list of sections
        """   
        section_list=[]
        for point1 in point_list:
            for point2 in point_list[1:]:
                section_list.append(self.section_calculate(point1,point2))
        return section_list

    def __len__(self):
        """ 
        Finally calculate length of the path;
        :return: length
        """
        length=func.reduce(lambda a,x:a+x,
                           self.create_sections(self.create_points(self.array_of_coordinates)))
        return length

temp=Route(ReadersFactory().read(r'C:\Users\BART\length-of-path\coordinates.csv'))
print(len(temp))
