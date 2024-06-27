import cv2
import mediapipe as mp
print(cv2.__version__)

hands=mp.solutions.hands.Hands(False,2,1,0.5,0.5)
mpDrawing=mp.solutions.drawing_utils

def parseLamdmarks(frame):
    myHands=[]
    handsType=[]
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(frameRGB)



    if results.multi_hand_landmarks!=None:
        #print(results.multi_handedness)
        for hand in results.multi_handedness:
            #print(hand)
            handType=hand.classification[0].label
            handsType.append(handType)

        for handLms in results.multi_hand_landmarks:
            myhand=[]
            for landMark in handLms.landmark:
                myhand.append((int(landMark.x*width),int(landMark.y*height)))

            myHands.append(myhand)

    return myHands, handsType


width=800
height= 460 
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW) #camera object # DSHOW : DIRECT SHOW TO MAKE CAMERA LOAD FASTER

cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG')) # setting everything do that it runs smoothly on windows

paddlewidth=25
paddleheight=125
paddlecolor=(255,0,255)
ballradius=25
ballcolor=(255,0,0)
xpos=int(width//2)
ypos=int(height//2)
delx=5
dely=5
font=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fontheight=2
fontweight=2
fontcolor=(0,0,255)

ylefttip=0
yrighttip=0

scoreleft=0
scoreright=0
  
while True:
    ignore, frame = cam.read() # read a frame
    frame=cv2.resize(frame,(width,height))
    frame=cv2.flip(frame,1)

    cv2.circle(frame,(xpos,ypos),ballradius,ballcolor,-1)
    cv2.putText(frame,str(scoreleft),(25,50),font,fontheight,fontcolor,fontweight)
    cv2.putText(frame,str(scoreright),(width-100,50),font,fontheight,fontcolor,fontweight)

    
   
    myHands,LorRHands=parseLamdmarks(frame)
    
    for hand,handtype in zip(myHands,LorRHands):
        #print(hand)
        if handtype=='Left':
            ylefttip=hand[8][1]
            cv2.circle(frame,hand[8],10,(0,255,255),3)
        if handtype=='Right':
            yrighttip=hand[8][1]
            cv2.circle(frame,hand[8],10,(255,255,0),3)

        cv2.rectangle(frame,(0,ylefttip-int(paddleheight//2)),(paddlewidth,int(ylefttip+paddleheight//2)),paddlecolor,-1)
        cv2.rectangle(frame,(width-int(paddlewidth),yrighttip-int(paddleheight//2)),(width,int(yrighttip+paddleheight//2)),paddlecolor,-1)


        topedgeball=ypos-ballradius
        bottomedgeball=ypos+ballradius

        leftedgeball=xpos-ballradius
        righedgeball=xpos+ballradius

        if bottomedgeball>=height:
            dely*=-1

        if topedgeball<=0:
            dely*=-1

        if leftedgeball<=paddlewidth:
            if ypos>=ylefttip-int(paddleheight//2) and ypos<=int(ylefttip+paddleheight//2):
                delx*=-1

            else:
                xpos=int(width/2)
                ypos=int(height/2)
                scoreright+=1
                if scoreleft%5==0 and scoreleft!=0:
                    delx*=1.5
                    dely*=1.5


        if righedgeball>=width-paddlewidth:
            if ypos>=yrighttip-int(paddleheight//2) and ypos<=int(yrighttip+paddleheight//2):
                delx*=-1
            else:
                xpos=int(width//2)
                ypos=int(height//2)
                scoreleft+=1  

              
        xpos+=delx
        ypos+=dely

        

 
    cv2.imshow('mycam1',frame) # show a frame
    cv2.moveWindow('mycam1',0,0)

    

    if cv2.waitKey(1) & 0xff == ord(' '):  # key to be pressed to exit 
        break

cam.release()

