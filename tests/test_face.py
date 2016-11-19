import cognitive_face as CF

KEY = str(raw_input('KEY: '))
CF.Key.set(KEY)
IMAGE = 'img.jpg'
RESULT = CF.face.detect(IMAGE)

print RESULT
