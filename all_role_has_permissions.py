from apiApp.models import role, permission, role_has_permissions

def assign_permissions_to_role(role_name, permission_list):
    try:
        # Get the role
        role_obj = role.objects.get(name=role_name.lower())
        
        for perm_name in permission_list:
            try:
                # Get the permission
                perm_obj = permission.objects.get(name=perm_name)
                
                # Check if the permission is already associated with the role
                role_perm, created = role_has_permissions.objects.get_or_create(
                    role_id=role_obj,
                    permission_id=perm_obj
                )
                if created:
                    print(f"Permission '{perm_name}' assigned to role '{role_name}'.")
                else:
                    print(f"Permission '{perm_name}' already exists for role '{role_name}'.")
            except permission.DoesNotExist:
                print(f"Permission '{perm_name}' does not exist and was skipped.")

        return f"Permissions successfully assigned to role '{role_name}'."

    except role.DoesNotExist:
        return f"Error: Role '{role_name}' does not exist."

# Example usage:

admin_permissions = [
    'list_workspace', 'add_workspace', 'update_workspace', 'delete_workspace',
    'list_ai_configuration', 'add_ai_configuration', 'update_ai_configuration', 'delete_ai_configuration', 'verify_ai_configuration',
    'list_user_detail', 'add_user_detail', 'update_user_detail', 'delete_user_detail', 
    'list_domain', 'add_domain', 'update_domain', 'delete_domain', 
    'add_test_article', 'delete_test_article', 
    'add_test_tag', 'delete_test_tag',  
    'add_test_category', 'delete_test_category',  
    'update_tag', 'add_tag', 'delete_tag', 'list_tag', 
    'add_author', 'update_author', 'list_author', 'delete_author', 
    'add_category', 'update_category', 'list_category', 'delete_category',
    'add_article', 'update_article', 'list_article', 'delete_article', 
    'add_prompt', 'update_prompt', 'list_prompt', 'detele_prompt', 
    'list_competitor','add_competitor', 'update_competitor', 'delete_competitor', 
    'fetch_wp_data',
    'list_image_tag', 'add_image_tag', 'update_image_tag', 'delete_image_tag', 
    'list_image_template_category', 'add_image_template_category', 'update_image_template_category', 'delete_image_template_category', 
    'list_image_template', 'add_image_template', 'update_image_template', 'delete_image_template', 
    'list_image_tag_template_category_template_mapping', 'add_image_tag_template_category_template_mapping', 'update_image_tag_template_category_template_mapping', 'delete_image_tag_template_category_template_mapping', 
    'fetch_category_data', 'fetch_tag_data', 'fetch_author_data', 'fetch_article_data', 
    'fetch_console_metrics_data', 'fetch_analytics_metrics_data',
    
]

manager_permissions = [
    'list_ai_configuration', 'verify_ai_configuration',   
    'update_tag', 'add_tag', 'delete_tag', 'list_tag', 
    'add_author', 'update_author', 'list_author', 'delete_author', 
    'add_category', 'update_category', 'list_category', 'delete_category',
    'add_article', 'update_article', 'list_article', 'delete_article', 
    'add_prompt', 'update_prompt', 'list_prompt', 'detele_prompt',  
]

writer_permissions = [
    'list_tag', 
    'list_author', 
    'list_category',
    'add_article', 'update_article', 'list_article', 
    'list_prompt',  
]

# Assign permissions to the 'manager' role
print(assign_permissions_to_role('admin', admin_permissions))
print(assign_permissions_to_role('manager', manager_permissions))
print(assign_permissions_to_role('writer', writer_permissions))











# for me

admin_permissions = [
    'list_workspace', 'add_workspace', 'update_workspace', 'delete_workspace',
    'list_ai_configuration', 'add_ai_configuration', 'update_ai_configuration', 'delete_ai_configuration', 'verify_ai_configuration',
    'list_user_detail', 'add_user_detail', 'update_user_detail', 'delete_user_detail', 
    'list_domain', 'add_domain', 'update_domain', 'delete_domain', 
    'add_test_article', 'delete_test_article', 
    'add_test_tag', 'delete_test_tag',  
    'add_test_category', 'delete_test_category',  
    'update_tag', 'add_tag', 'delete_tag', 'list_tag', 
    'add_author', 'update_author', 'list_author', 'delete_author', 
    'add_category', 'update_category', 'list_category', 'delete_category',
    'add_article', 'update_article', 'list_article', 'delete_article', 
    'add_prompt', 'update_prompt', 'list_prompt', 'detele_prompt', 
    'list_competitor','add_competitor', 'update_competitor', 'delete_competitor', 
    'fetch_wp_data',
    'list_image_tag', 'add_image_tag', 'update_image_tag', 'delete_image_tag', 
    'list_image_template_category', 'add_image_template_category', 'update_image_template_category', 'delete_image_template_category', 
    'list_image_template', 'add_image_template', 'update_image_template', 'delete_image_template', 
    'list_image_tag_template_category_template_mapping', 'add_image_tag_template_category_template_mapping', 'update_image_tag_template_category_template_mapping', 'delete_image_tag_template_category_template_mapping', 
    'fetch_category_data', 'fetch_tag_data', 'fetch_author_data', 'fetch_article_data', 
    'fetch_console_metrics_data', 'fetch_analytics_metrics_data',
    '', '', '', '', 
    '', '', '', '', 
    '', '', '', '', 
    
]

manager_permissions = [
    'list_ai_configuration', 'verify_ai_configuration',   
    'update_tag', 'add_tag', 'delete_tag', 'list_tag', 
    'add_author', 'update_author', 'list_author', 'delete_author', 
    'add_category', 'update_category', 'list_category', 'delete_category',
    'add_article', 'update_article', 'list_article', 'delete_article', 
    'add_prompt', 'update_prompt', 'list_prompt', 'detele_prompt',  
    '', '', '', '', 
    '', '', '', '', 
    '', '', '', '', 
]

writer_permissions = [
    'list_tag', 
    'list_author', 
    'list_category',
    'add_article', 'update_article', 'list_article', 
    'list_prompt',  
    '', '', '', '', 
    '', '', '', '', 
    '', '', '', '', 
]