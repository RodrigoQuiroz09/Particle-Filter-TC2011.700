import numpy as np
import cv2
import time
from constants import *
import sys
import getopt

class particleFilter(object):
    def __init__(self,video_input):
        """
            Funcion que inicializa el sistema. Se definen diferentes atributos como color a buscar, propiedades del video y contador de fps

            Returns:
            None
        """
        
        self.height = 0
        self.width = 0
        self.fps = 0
        self.fps_counter = 0
        self.videoName = video_input 
        self.defaultColor =np.array((0,0,0))
        
        for video_name in TEST_VIDEOS:
            if video_name in video_input:
                matchingVals = [x for x in range(len(TEST_VIDEOS)) if video_name == TEST_VIDEOS[x]]
                self.defaultColor = CONCAT[matchingVals]
                break                
             
        self.searchedColor = self.defaultColor #Esto se va a cambiar con color Picker
        self.color_explore = np.zeros((150,200,3), np.uint8) 
        self.color_explore [75:150] = self.searchedColor
        self.tempFrame=[]
        self.rgb_text="RGB(0,0,0)"
        try: 
            self.colorPicker()
        except:
            print("El video proporcionado no se encuentra en la carpeta del proyecto")
            sys.exit(0)

    def applySleep(self):
        """
            Funcion para aplicar un sleep entre el procesamiento de cada frame

            Returns:
            None
        """
        time.sleep(1/self.getFps())

    def set_video_dimensions(self,filename):
        """
            Funcion para obtener y definir diferentes propiedades del video a analizar

            Returns:
            None
        """
        video = cv2.VideoCapture(filename)
        self.height = int(video.get(4))
        self.width = int(video.get(3))
        self.fps= int(video.get(cv2.CAP_PROP_FPS))
        video.release()

    def get_frames(self,filename):
        """
            Funcion para obtener, de manera individual y paulatina, los frames del video siendo analizado

            Returns:
            frame --> Cada uno de los frames del video siendo analizado
        """
        video = cv2.VideoCapture(filename)
        while video.isOpened():
            ret, frame = video.read()
            if ret:
                yield frame
            else: break
        video.release()
        yield None
        
    def getHeight(self):
        """
            Getter de altura del video

            Returns:
            self.height --> Altura del video siendo analizado
        """
        return self.height
    
    def getWidth(self):
        """
            Getter de ancho del video

            Returns:
            self.width --> Ancho del video siendo analizado
        """
        return self.width
    
    def getFps(self):
        """
            Getter de frames en video

            Returns:
            self.fps --> Numero de frames en el video siendo analizado
        """
        return self.fps
    
    def getVideoName(self):
        """
            Getter de nombre del video

            Returns:
            self.videoName --> Nombre del video siendo analizado
        """
        return self.videoName
    
    def getSearchedColor(self):
        """
            Getter de color a ser buscado y trackeado dentro del video

            Returns:
            self.searchedColor --> Color a ser buscado y trackeado dentro del video siendo analizado
        """
        return self.searchedColor

    def getFpsCounter(self):
        """
            Getter de contador de frames analizados dentro del video

            Returns:
            self.fps_counter --> Contador de frames analizados dentro del video siendo analizado
        """
        return self.fps_counter

    def incrementFpsCounter(self):
        """
            Actualizador del contador de frames analizados dentro del video

            Returns:
            self.fps_counter --> Contador actualizado de frames analizados dentro del video siendo analizado
        """
        self.fps_counter += 1
        
    def write_to_file(self,R,G,B):
        """
            Escribe en un archivo de texto el color a ser analizado y trackeado

            Returns:
            None
        """
        f = open("saved_color.txt", "a")
        RGB_color=str(R) + "," + str(G) + "," + str(B) + str("\n")
        f.write(RGB_color)
        f.close()
        
    def mouseRGB(self,event,x,y,flags,param):
        """
            Funcion auxiliar en la obtencion del color analizar, mediante el uso de mouse

            Returns:
            None
        """            
        B=self.tempFrame[y,x][0]
        G=self.tempFrame[y,x][1]
        R=self.tempFrame[y,x][2]
        self.rgb_text ="RGB(" + str(R) + "," + str(G) + "," + str(B) + ")"
        self.color_explore [:75] = (B,G,R)
        if event == cv2.EVENT_LBUTTONDOWN:
                self.color_explore [75:150] = (B,G,R)
                self.searchedColor = np.array((B,G,R))    
        if event == cv2.EVENT_RBUTTONDOWN:
            B=self.color_explore[10,10][0]
            G=self.color_explore[10,10][1]
            R=self.color_explore[10,10][2]
            print(R,G,B)
            self.write_to_file(R,G,B)
            print(hex(R),hex(G),hex(B))
        
    def colorPicker(self):
        """
            Funcion encargada de la obtener del color a ser trackeado, mediante el uso de mouse de usuario

            Returns:
            None
        """
        cv2.namedWindow('mouseRGB')
        cv2.setMouseCallback('mouseRGB',self.mouseRGB)
        capture = cv2.VideoCapture(self.videoName)
        x=0
        cv2.namedWindow('color_explore')
        cv2.resizeWindow("color_explore", 100,50);
        
        while(x<5):
            _, self.tempFrame = capture.read()
            while(1):
                cv2.putText(self.color_explore, self.rgb_text, (5,25), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.imshow('mouseRGB', self.tempFrame)
                cv2.imshow('color_explore',self.color_explore)
                k = cv2.waitKey(1) & 0xFF
                if k == ord("n"):
                        x=x+1
                        break
                if k == ord("d"):
                   self.color_explore [75:150] = self.defaultColor
                   self.searchedColor = self.defaultColor 
            key = cv2.waitKey(1) & 0xFF            
            if key == ord("q"):
                break
        capture.release()
        cv2.destroyAllWindows()

    def initialize_particles(self):
        """
            Inicializa un cojunto de particulas, a ser desplegadas en el video

            Returns:
            particles --> Lista de particulas, con ubicacion en x y y, al igual que sus velocidades
        """
        particles = np.random.rand(PARTICLES, 4)
        particles = particles * np.array((self.width, self.height, SPEED, SPEED))
        for row in particles:
            row[2:4] = (row[2:4] - SPEED / 2) * 1.0
        return particles

    def speed(self,particles,axis,speed):
        """
            Funcion encargada de dar velocidad/aceleracion a las particulas dentro del video

            Returns:
            particles --> Lista de particulas, con ubicacion en x y y, al igual que sus nuevas velocidades
        """
        particles[:,axis] = particles[:,speed] + particles[:,axis]
        return particles

    def xBoundaries(self,particles):
        """
            Se define el periodo espacial (en x) en donde las particulas pueden "sobrevivir" dentro del frame del video

            Returns:
            particles --> Lista de particulas, con ubicacion en x y y, al igual que sus velocidades
        """
        for index in range(PARTICLES):
             particles[index, 0] = max(min(self.width-1, particles[index, 0]),0)
        return particles
    
    def yBoundaries(self,particles):
        """
            Se define el periodo espacial (en y) en donde las particulas pueden "sobrevivir" dentro del frame del video

            Returns:
            particles --> Lista de particulas, con ubicacion en x y y, al igual que sus velocidades
        """
        for index in range(PARTICLES):
             particles[index, 1] = max(min(self.height-1, particles[index, 1]), 0)
        return particles

    def particleColors(self,particles,frame):
        """
            Metodo que identifica si particulas se ubican sobre pixeles del color a ser trackeado por el programa. En caso de que no, se calculan las correcciones pertinentes

            Returns:
            corrections --> Lista con correciones a ser aplicadas a funcion
        """
        corrections = np.zeros(PARTICLES)
        for i in range(PARTICLES):
            x_pos = int(particles[i, 0])
            y_pos = int(particles[i, 1])
            color_in_particle_ = [0,0,0]
            for index in range(len(color_in_particle_)):
                color_in_particle_[index] = frame[y_pos, x_pos, index]
            color_in_particle_ = np.array(color_in_particle_)
            future_correction = (self.getSearchedColor() - color_in_particle_) * (self.getSearchedColor() - color_in_particle_)
            future_correction = np.sum(future_correction)
            corrections[i] = future_correction
        return corrections

    def getRelevantIndicators(self,corrections,particles):
        """
            Metodo que realiza las correcciones necesarias, especialemte en los extremos del video, para facilitar el movimiento de particulas en futuros cuadros del video

            Returns:
            relevant_particle_indicators --> Lista con particulas corregidas
        """
        relevant_particle_indicators = np.max(corrections) - corrections
        relevant_particle_indicators[(particles[:,0] == 0)] = float(0)
        relevant_particle_indicators[(particles[:,0] == self.width-1)|(particles[:,0] == self.height-1)] = float(0)
        relevant_particle_indicators[(particles[:,1] == 0)] = float(0)
        relevant_particle_indicators = relevant_particle_indicators * relevant_particle_indicators
        return relevant_particle_indicators

    def createParticlesSample(self,particles,indicators):
        """
            Mediante un mustreo, con base en las mejores particulas segun su posicion, se creo nuevo grupo de particulas a ser desplegadas. Adicionalmente, se calcula el centro del circulo
            en el cual se va a "englobar" al objeto siendo trackeado

            Returns:
            particles --> Lista con particulas ajustadas
            location --> Posicion (x,y) del centro del objeto trackeado
        """
        probs = indicators / np.sum(indicators)
        selected_indexes = np.random.choice(PARTICLES, size=PARTICLES, p=probs) 
        particles = particles[selected_indexes,:]
        x_pos = 0
        y_pos = 0
        for value_x, value_y in zip(particles[:,0], particles[:,1]):
            x_pos += value_x
            y_pos += value_y
        x_pos = int(x_pos / len(particles[:,0]))
        y_pos = int(y_pos / len(particles[:,1]))
        location = tuple([x_pos, y_pos])
        return particles, location

    def applyParticleModifications(self,particles):
        """
            Se aplican distribuciones normales para una capa adicional de alteraciones y optimizacion de las particulas

            Returns:
            particles --> Lista con particulas corregidas
        """
        distribution = np.random.normal(float(0), POSITION_CHANGE, change_tuple)
        distribution_two = np.random.normal(float(0), POSITION_CHANGE, change_tuple)
        distribution_three = np.random.normal(float(0), VELOCITY_CHANGE, change_tuple)
        distribution_four = np.random.normal(float(0), VELOCITY_CHANGE, change_tuple)
        particles += np.concatenate((distribution, distribution_two, distribution_three, distribution_four), axis=1)
        return particles

    def displayFrame(self,frame,particles,location):
        """
            Se aplican distribuciones normales para una capa adicional de alteraciones y optimizacion de las particulas

            Returns:
            particles --> Lista con particulas corregidas
        """
        if len(particles) > 0:
            for i in range(PARTICLES):
                x = int(particles[i,0])
                y = int(particles[i,1])
                cv2.circle(frame, (x,y), 1, (0,255,150), 1)
        if len(location) > 0:
            cv2.circle(frame, location, 20, (0,0,255), 5)
        cv2.imshow("frame", frame)
        if cv2.waitKey(18) == ord('q'):
                return True
        return False

def myfunc(argv):
    video = ""
    arg_help = "{0} --video <video> ".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "hv:u:o:", ["help", "video="])
    except:
        print(arg_help)
      
        sys.exit(2)
    counter=0
    for opt, arg in opts:
        counter+=1;
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(0)
        elif opt in ("-v", "--video"):
            video = arg

    if(counter==0):
        print(arg_help)
        sys.exit(0)
    return video

def main():
    video_input=myfunc(sys.argv)
    if(video_input==""):
            sys.exit(0)
    particlefilter = particleFilter(video_input)
    particlefilter.set_video_dimensions(particlefilter.getVideoName())
    particles = particlefilter.initialize_particles()
    video_frames = []
    for frame in particlefilter.get_frames(particlefilter.getVideoName()):
        if frame is None: 
            break
        particlefilter.incrementFpsCounter()
        particles = particlefilter.speed(particles, 0, 2)
        particles = particlefilter.speed(particles, 1, 3)
        particles = particlefilter.xBoundaries(particles)
        particles = particlefilter.yBoundaries(particles)
        corrections = particlefilter.particleColors(particles,frame)
        indicators = particlefilter.getRelevantIndicators(corrections,particles)
        particles, location = particlefilter.createParticlesSample(particles,indicators)
        particles = particlefilter.applyParticleModifications(particles)
        particlefilter.applySleep()
        cv2.putText(frame,("Frame: "+str(particlefilter.getFpsCounter())),(10,15),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255))
        
        overlay = frame.copy()
        x, y, w, h = 5, 5, 100, 10  # Rectangle parameters
        cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 0, 0), -1)  # A filled rectangle
        alpha = 0.4 
        
        image_new = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        video_frames.append(image_new)
        terminate = particlefilter.displayFrame(image_new,particles,location)
        if terminate:
            break
        
    writer = cv2.VideoWriter_fourcc(*'mp4v') 
    video = cv2.VideoWriter('output.mp4', writer, 15, (particlefilter.getWidth(), particlefilter.getHeight()))
    for frame in video_frames:
        video.write(frame)
    video.release()
    cv2.destroyAllWindows()

main()