import cv2
import screen_brightness_control as sbc
import mediapipe as mp
import time
import math as m 
l=[0,0,0,0]
ptime=0
ctime=0
cap=cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
while True:
    _,frame=cap.read()
    
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for Hlms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame,Hlms,mpHands.HAND_CONNECTIONS)
            for id,lm in enumerate(Hlms.landmark):
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                if id==4 or id==8:
                    if id==4:
                        l[0]=cx
                        l[1]=cy
                    #cv2.circle(frame,(cx,cy),15,(255,0,255),cv2.FILLED)
                    if id==8:
                        l[2]=cx
                        l[3]=cy
                    #cv2.circle(frame,(cx,cy),15,(255,0,255),cv2.FILLED)
                    cv2.line(frame,(l[0],l[1]),(l[2],l[3]),(0,0,255),3)
                    screen_brightness=(int((((m.sqrt((abs(l[0]-l[2]))**2+(abs(l[1]-l[3]))**2))))))
                    sbc.set_brightness(screen_brightness)
                    print(sbc.set_brightness(screen_brightness),int((((m.sqrt((abs(l[0]-l[2]))**2+(abs(l[1]-l[3]))**2)))-15)/175)*100)
                    
    cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX ,3,(0,255,0),3)
    cv2.imshow("Frame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#cap.release()
#cv2.destroyAllWindows()
