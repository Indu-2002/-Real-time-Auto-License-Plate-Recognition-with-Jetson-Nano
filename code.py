import cv2
import pytesseract

# Path to Tesseract executable (change this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize camera
cap = cv2.VideoCapture(0)  # Adjust the index based on your camera setup

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Perform edge detection using Canny edge detector
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate through contours
    for contour in contours:
        # Calculate the area of contour
        area = cv2.contourArea(contour)
        
        # Filter contours based on area (adjust as needed)
        if 1000 < area < 5000:
            # Get the bounding box coordinates
            x, y, w, h = cv2.boundingRect(contour)
            
            # Crop the region of interest (ROI) containing the license plate
            plate_roi = gray[y:y+h, x:x+w]
            
            # Use Tesseract OCR to recognize text in the cropped ROI
            plate_number = pytesseract.image_to_string(plate_roi, config='--psm 7')
            
            # Display recognized plate number
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, plate_number.strip(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('License Plate Recognition', frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
