import os


rootdir           = os.getcwd()
uploaddir         = "/uploads/photos"


print(rootdir)

print(os.listdir(rootdir+uploaddir))

def get_uploaded_images(rootdir,uploaddir): 
      images = []
      try:
            images = os.listdir(rootdir+uploaddir)
      except Exception as e:
            print(e)
      else:
            print("complete")
            
      return images

files = get_uploaded_images(rootdir,uploaddir)

print(files)
