# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global card_deck, expose, state, turn
    list_ = [n for n in range(0,8)] 
    card_deck = list_ + list_
    random.shuffle(card_deck)
    expose = []  
    state = 0
    turn = 0
    label.set_text("Turns = " + str(turn))
    for i in range(16):
        expose.append(False)
#    for i in range(4,9):
#        expose.append(True)
#    for i in range(9,16):
#        expose.append(True)
    
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global expose, state, f_card, s_card, turn
    card_index = pos[0]/52

    if not expose[card_index]:
        if state == 0:
            f_card = card_index
            state = 1
        elif state == 1:            
            s_card = card_index
            state = 2
            turn += 1
            label.set_text("Turns = " + str(turn))
        else:
            state = 1
            if not (card_deck[f_card] == card_deck[s_card]):
                expose[f_card] = False
                expose[s_card] = False
            f_card = card_index
               
        expose[card_index] = True

    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16): 
        canvas.draw_polygon([[i*52, 0], [(i+1)*52, 0], [(i+1)*52, 100], [i*52, 100]], 2, 'Black','Green')                
        if expose[i]:
            canvas.draw_polygon([[i*52, 0], [(i+1)*52, 0], [(i+1)*52, 100], [i*52, 100]], 2, 'Black','Black')                
            canvas.draw_text(str(card_deck[i]), [i*52+22, 55], 30, 'White')           
        
        

        

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 832, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
