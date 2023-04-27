
import numpy as np



# gradient
b_neg_grad_1 = np.exp(0.0196)
b_neg_grad_2 = np.exp(0.0312)
b_neg_grad_3 = np.exp(0.0779)
b_neg_grad_4 = np.exp(0.1196)
b_neg_grad_5 = np.exp(0.1488)
b_neg_grad_6 = np.exp(0.1861)
b_neg_grad_7 = np.exp(0.1228)
b_neg_grad_9 = np.exp(0.0617)
b_neg_grad_9_plus = np.exp(0.0518)

b_pos_grad_1 = np.exp(0.0)
b_pos_grad_2 = np.exp(-0.0376)
b_pos_grad_3 = np.exp(-0.1299)
b_pos_grad_4 = np.exp(-0.1951)
b_pos_grad_5 = np.exp(-0.2669)
b_pos_grad_6 = np.exp(-0.3034)
b_pos_grad_7 = np.exp(-0.3854)
b_pos_grad_9 = np.exp(-0.3949)
b_pos_grad_9_plus = np.exp(-0.4267)




def duration_calculator_bygradient(cycling_speed, grad_list, dist_list ):
    duration_list=[]
    speed = (cycling_speed*1000)/3600
    gradients = grad_list
    distances = dist_list

    for gradient, distance in zip(gradients,distances):
        if gradient >= 0 :
            if gradient >= 9 :
                dur = distance/(speed*b_pos_grad_9_plus)
            elif (gradient >= 7)& (gradient < 9):
                dur = distance/(speed*b_pos_grad_9)
            elif (gradient >= 6)& (gradient < 7):
                dur = distance/(speed*b_pos_grad_7)
            elif (gradient >= 5)& (gradient < 6):
                dur = distance/(speed*b_pos_grad_6)
            elif (gradient >= 4)& (gradient < 5):
                dur = distance/(speed*b_pos_grad_5)
            elif (gradient >= 3)& (gradient < 4):
                dur = distance/(speed*b_pos_grad_4)
            elif (gradient >= 2)& (gradient < 3):
                dur = distance/(speed*b_pos_grad_3)
            elif (gradient >= 1)& (gradient < 2):
                dur = distance/(speed*b_pos_grad_2)
            elif (gradient >= 0)& (gradient < 1):
                dur = distance/(speed*b_pos_grad_1)
        else:
            if gradient <= -9 :
                dur = distance/(speed*b_neg_grad_9_plus)
            elif (gradient <= -7)& (gradient > -9):
                dur = distance/(speed*b_neg_grad_9)
            elif (gradient <= -6)& (gradient > -7):
                dur = distance/(speed*b_neg_grad_7)
            elif (gradient <= -5)& (gradient > -6):
                dur = distance/(speed*b_neg_grad_6)
            elif (gradient <= -4)& (gradient > -5):
                dur = distance/(speed*b_neg_grad_5)
            elif (gradient <= -3)& (gradient > -4):
                dur = distance/(speed*b_neg_grad_4)
            elif (gradient <= -2)& (gradient > -3):
                dur = distance/(speed*b_neg_grad_3)
            elif (gradient <= -1)& (gradient > -2):
                dur = distance/(speed*b_neg_grad_2)
            elif (gradient < 0)& (gradient > -1):
                dur = distance/(speed*b_neg_grad_1)
        duration_list.append(dur)
    return sum(duration_list)
