

# *** run project *** 

.\.venv\Scripts\activate  # start env 

python manage.py makemigrations     
python manage.py migrate      
python manage.py createsuperuser   # create superuser   
    
python manage.py runserver        # run http://
python manage.py runserver_plus --cert-file cert.crt  # run https://
python manage.py runserver_plus 192.168.1.4:8000 --cert-file cert.crt       #  run ip host
192.168.1.3
192.168.1.4

# *** info *** 

pip install django-extensions -->> for https:// just info for me  

python3 manage.py shell < all_permissions.py    # run any file in shell  
python3 manage.py shell < all_role_has_permissions.py    # run any file in shell  
ipconfig 


py manage.py startapp frontendApp

