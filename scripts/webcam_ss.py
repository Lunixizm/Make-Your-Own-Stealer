import cv2

def take():
 cap = cv2.VideoCapture(0)

 ret, frame = cap.read()

 cv2.imwrite(r"C:\Windows\Temp\image.png", frame)

 cap.release()

 cv2.destroyAllWindows()
