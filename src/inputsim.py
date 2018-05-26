#!/usr/bin/env python
import sys



def main(arg):
    '''
    Input should be either a list of lists, or a list of lists converted into a string
    '[[0.0,1.0,1.0,1.0],[0.1,1,2,1],[0.2,2,2,1]]'
    '''


    if(type(arg) != list):
        arg = preprocess(arg)

    input = arg










def preprocess(msg):
    '''
    Process an input string into a list of lists
    '''
    output = msg.strip('[]')
    output = output.split('],[')

    for index in range(len(output)):
        output[index] = output[index].split(',')
        for subdex in range(len(output[index])):
            output[index][subdex] = float(output[index][subdex])



    return output





if __name__ == '__main__':
    if(len(sys.argv) == 2):
        main(sys.argv[1])
    else:
        print "Usage: inputsim.py <input list>"
