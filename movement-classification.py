# Imports go at the top
from microbit import *
import log
import music
import math

# Phases of the program
phase = 0 # phase 0: program start
          # phase 1: recording rest
          # phase 2: recording shake
          # phase 3: recording walk
          # phase 4: training model
          # phase 5: prediction
welcome_start_msg = False
recording_rest_msg = False
recording_shake_msg = False
recording_walk_msg = False
predicting_msg = False
trained = False

log.set_labels('x_rest', 
               'y_rest', 
               'z_rest', 
               'x_shake', 
               'y_shake', 
               'z_shake',
               'x_walk',
               'y_walk',
               'z_walk',
               'x_test',
               'y_test',
               'z_test')

x_rest = []
y_rest = []
z_rest = []

x_shake = []
y_shake = []
z_shake = []

x_walk = []
y_walk = []
z_walk = []

x_test = []
y_test = []
z_test = []

# Samples (500 samples * 30ms = 15000 = 15 sec recording)
window_size = 400 # TRAINING running into memory problems with higher samples
dt = 30

predict_window_size = 50
# Helper Functions
def mean(window):
    return sum(window) / len(window)

def std_dev(window):
    sum_sq_dif = 0
    average = mean(window)
    for i in range(len(window)):
        sum_sq_dif = sum_sq_dif + math.pow(window[i]-average,2)

    return math.sqrt(sum_sq_dif/len(window))

def lagged_differences(window):
    lag_diff = []
    for i in range(1,len(window)):
        lag_diff.append(window[i]-window[i-1])

    return lag_diff

def smoothness(window):
    lag_diff = lagged_differences(window)
    return std_dev(lag_diff)

def chunk_data(data_list, chunk_size):
    chunk_list = []
    for i in range(0, len(data_list), chunk_size):
        chunk_list.append(data_list[i:i + chunk_size])
    
    return chunk_list

def euclidean_distance(point1, point2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))


# k-NN Classifier (works only for k=1 [specific to this problem])
class KNNClassifier:
    def __init__(self):
        self.training_data = []

    def train(self, data):
        self.training_data = data

    def predict(self, sample):
        distances = []
        for data, label in self.training_data:
            distance = euclidean_distance(data, sample)
            distances.append((distance, label))
        distances.sort(key=lambda x: x[0]) # sort ascending (smalles distance first)
        return distances[0][1] # return the first label

knn = KNNClassifier()

# Code in a 'while True:' loop repeats forever
while True:
    if button_a.was_pressed():
        phase=phase+1

    if button_b.was_pressed():
        phase=0
        welcome_start_msg = False
        recording_rest_msg = False
        recording_shake_msg = False
        recording_walk_msg = False
        predicting_msg = False

    # Get accelerometer data
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()

    if(phase == 0):
        # program start
        if(not welcome_start_msg):
            welcome_start_msg = True
            music.play(music.POWER_UP)
        
        display.show(Image('00000:'
                           '33333:'
                           '55555:'
                           '77777:'
                           '99999:'))
    elif(phase == 1):
        # recording rest
        if(not recording_rest_msg):
            recording_rest_msg = True
            music.play(music.BA_DING)

        x_rest.append(x)
        y_rest.append(y)
        z_rest.append(z)

        if(len(x_rest) >= window_size):
            x_rest.pop(0)
            y_rest.pop(0)
            z_rest.pop(0)
            display.show(Image('99999:'
                               '99999:'
                               '99999:'
                               '99999:'
                               '99999:'))
        else:
            display.show(Image.ASLEEP)

        sleep(dt) # Downsampling allows for more recording time
        
    elif(phase == 2):
        # recording shake
        if(not recording_shake_msg):
            recording_shake_msg = True
            music.play(music.BA_DING)

        x_shake.append(x)
        y_shake.append(x)
        z_shake.append(x)

        
        if(len(x_shake) >= window_size):
            x_shake.pop(0)
            y_shake.pop(0)
            z_shake.pop(0)
            display.show(Image('99999:'
                               '99999:'
                               '99999:'
                               '99999:'
                               '99999:'))
        else:
            display.show(Image.HEART_SMALL)
    

        sleep(dt) # Downsampling allows for more recording time
        
    elif(phase == 3):
        # recording walk
        if(not recording_walk_msg):
            recording_walk_msg = True
            music.play(music.BA_DING)
        
        x_walk.append(x)
        y_walk.append(y)
        z_walk.append(z)

        if(len(x_walk) >= window_size):
            x_walk.pop(0)
            y_walk.pop(0)
            z_walk.pop(0)
            display.show(Image('99999:'
                               '99999:'
                               '99999:'
                               '99999:'
                               '99999:'))
        else:
            display.show(Image.STICKFIGURE)
    
        sleep(dt) # Downsampling allows for more recording time

    elif(phase == 4):
        if(not trained):
            display.show(Image.HEART)
            summary_rest = (std_dev(x_rest), std_dev(y_rest), std_dev(z_rest),
                            smoothness(x_rest), smoothness(y_rest), smoothness(z_rest))
            
            summary_shake = (std_dev(x_shake), std_dev(y_shake), std_dev(z_shake),
                             smoothness(x_shake), smoothness(y_shake), smoothness(z_shake))
             
            summary_walk = (std_dev(x_walk), std_dev(y_walk), std_dev(z_walk),
                            smoothness(x_walk), smoothness(y_walk), smoothness(z_walk))

            training_data = [(summary_rest, 0),(summary_shake, 1),(summary_walk, 2)]
            
            # Train the k-NN classifier
            knn.train(training_data)
            trained = True
        else:
            phase = 5 # start predicting
        
        '''
        for i in range(len(x_rest)):
            log.add({
              'x_rest' : x_rest[i],
              'y_rest' : y_rest[i],
              'z_rest' : z_rest[i],
              'x_shake': x_shake[i],
              'y_shake': y_shake[i],
              'z_shake': z_shake[i],
              'x_walk' : x_walk[i],
              'y_walk' : y_walk[i],
              'z_walk' : z_walk[i],
              'x_test' : x_test[i],
              'y_test' : y_test[i],
              'z_test' : z_test[i],
            })
        '''
        
    elif(phase >= 5):
        # predicting
        if(not predicting_msg):
            predicting_msg = True
            music.play(music.RINGTONE)

        x_test.append(x)
        y_test.append(y)
        z_test.append(z)

        # If we reach this conditional, it means the window is big enough to start predicting values
        if(len(x_test) >= predict_window_size):
            x_test.pop(0)
            y_test.pop(0)
            z_test.pop(0)

            # We now have a prediction window to work with
            summary_test = (std_dev(x_test), std_dev(y_test), std_dev(z_test),
                            smoothness(x_test), smoothness(y_test), smoothness(z_test))
            
            final_prediction = knn.predict(summary_test)
            
            display.show(final_prediction)

        else:
            display.show(Image('03330:'
                               '35753:'
                               '57975:'
                               '35753:'
                               '03330:'))
            
        sleep(dt) # Downsampling allows for more recording time
            
        

