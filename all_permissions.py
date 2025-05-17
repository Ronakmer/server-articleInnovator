
# from adminApp.models import permission
# from django.utils import timezone
# from adminApp.urls import urlpatterns, excluded_permissions

# permissions_data = []

# for pattern in urlpatterns:
#     if pattern.name and pattern.name not in excluded_permissions:
#         permissions_data.append({"name": pattern.name})

# print(permissions_data, 'permissions_data')

# # Create permission objects for the filtered permissions
# for data in permissions_data:
#     if data["name"]:
#         permission.objects.create(
#             name=data["name"],
#             created_date=timezone.now(),
#             updated_date=timezone.now(),
#         )
#     else:
#         print(f"Skipping entry with null or empty name: {data}")



from apiApp.models import permission
from django.utils import timezone
from apiApp.urls import permissions_list

permissions_data = []

# Process permissions_list to create permissions_data
for pattern in permissions_list:
    # print(pattern) 
    
    if pattern['name']: 
        permissions_data.append({
            "name": pattern['name'],
            "route": pattern['route'],  
            "description": pattern['description'],  
            "status": pattern['status'] , 
            "group": pattern['group'],  
            "created_date": timezone.now(), 
        })

permissions_data.append({
    "name": "detail_domain",
    "route": "detail_domain",
    "description": "detail_domain",
    "status": "True",
    "group": "detail_domain",
    "created_date": timezone.now(),
})

# Print permissions_data to verify its content
# print(permissions_data, 'permissions_data')

# Save permissions_data to the database
for perm in permissions_data:
    print(perm['status'],'3030')
    if perm['status'] == 'True':
        perm_obj, created = permission.objects.update_or_create(
            name=perm['name'],
            defaults={
                'description': perm['description'],
                'group': perm['group'],
                'created_date': perm['created_date'],
            }
        )
        if created:
            print(f"Created new permission: {perm_obj.name}")
        else:
            print(f"Updated existing permission: {perm_obj.name}")
