from PIL import Image
import face_recognition
import urllib.request

def compare_face_by_url(known_image_urls, image_2_url):
    # image_1_url should be a known image
    # image_2_url should be the image that needs to be compared
    print(known_image_urls)
    print(image_2_url)
    known_image_encodings = []
    known_images = []
    try:
        for image_1_url in known_image_urls:
            response_1 = urllib.request.urlopen(image_1_url)
            image_1 = face_recognition.load_image_file(response_1)
            known_images.append(image_1)
        response_2 = urllib.request.urlopen(image_2_url)
        
        image_2 = face_recognition.load_image_file(response_2)
    except Exception as e:
        return False, "Unable to load the image", 0
    
    try:
        for image_1 in known_images:
            image_1_encoding = face_recognition.face_encodings(image_1)[0]
            known_image_encodings.append(image_1_encoding)
        image_2_encoding = face_recognition.face_encodings(image_2)[0]
    except IndexError as e:
        return False, "No faces found in the image", 0

    results = face_recognition.compare_faces(known_image_encodings, image_2_encoding, 0.3)
    pos = 0
    flag = False
    for res in results:
        if res == True:
            flag = True
            pos = pos + 1
            break
    return True, flag, pos