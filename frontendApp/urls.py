# from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required

######### file import  #########
from frontendApp.views.auth.login_logout import login_page, registration_enter_otp_page
from frontendApp.views.onboard.onboard import onboard_page
from frontendApp.views.auth.forgot_password import email_page, otp_page, new_password_page
from frontendApp.views.dashboard.dashboard import dashboard_page
from frontendApp.views.role.role import add_role_page, list_role_page, update_role_page
from frontendApp.views.article_type_field.article_type_field import add_article_type_field_page, list_article_type_field_page, update_article_type_field_page
from frontendApp.views.article_type.article_type import add_article_type_page, list_article_type_page, update_article_type_page
from frontendApp.views.language.language import add_language_page, list_language_page, update_language_page
from frontendApp.views.country.country import add_country_page, list_country_page, update_country_page
from frontendApp.views.color_detail.color_detail import add_color_detail_page, list_color_detail_page, update_color_detail_page
from frontendApp.views.invitation_code_detail.invitation_code_detail import add_invitation_code_detail_page, list_invitation_code_detail_page, update_invitation_code_detail_page
from frontendApp.views.dynamic_avatar_image.dynamic_avatar_image import add_dynamic_avatar_image_page, list_dynamic_avatar_image_page, update_dynamic_avatar_image_page
from frontendApp.views.permission.permission import add_permission_page, list_permission_page, update_permission_page
from frontendApp.views.workspace.workspace import add_workspace_page, list_workspace_page, update_workspace_page
from frontendApp.views.motivation.motivation import add_motivation_page, list_motivation_page, update_motivation_page
from frontendApp.views.prompt.prompt import add_prompt_page, list_prompt_page, update_prompt_page
from frontendApp.views.user_detail.user_detail import add_user_detail_page, list_user_detail_page, update_user_detail_page, detail_user_page
from frontendApp.views.user_profile.user_profile import user_profile_page
from frontendApp.views.admin_detail.admin_detail import add_admin_detail_page, list_admin_detail_page, update_admin_detail_page
from frontendApp.views.domain.domain import add_domain_page, list_domain_page, update_domain_page, detail_domain_page
from frontendApp.views.article.article import add_article_page, list_article_page, update_article_page
from frontendApp.views.ai_configuration.ai_configuration import add_ai_configuration_page, list_ai_configuration_page, update_ai_configuration_page
from frontendApp.views.image_kit_configuration.image_kit_configuration import add_image_kit_configuration_page, list_image_kit_configuration_page, update_image_kit_configuration_page
from frontendApp.views.role_has_permissions.role_has_permissions import list_role_has_permissions_page
from frontendApp.views.notification.notification import list_notification_page
from frontendApp.views.activity_log.activity_log import list_activity_log_page
from frontendApp.views.error_page.error_page import error_page
from frontendApp.views.progress_bar.progress_bar import progress_bar_page
from frontendApp.views.rabbitmq.list_queues.list_queues import list_queues_page
from frontendApp.views.ai_rate_limiter.list_ai_rate_limiter.list_ai_rate_limiter import list_ai_rate_limiter_page
from frontendApp.views.integration.integration import list_integration_page,add_integration_page,update_integration_page

from frontendApp.views.supportive_prompt_type.supportive_prompt_type import list_supportive_prompt_type_page, add_supportive_prompt_type_page, update_supportive_prompt_type_page
from frontendApp.views.supportive_prompt.supportive_prompt import list_supportive_prompt_page, add_supportive_prompt_page, update_supportive_prompt_page


######### image gen  #########
from frontendApp.views.image_gen.image_tag.image_tag import add_image_tag_page, list_image_tag_page, update_image_tag_page
from frontendApp.views.image_gen.image_template_category.image_template_category import add_image_template_category_page, list_image_template_category_page, update_image_template_category_page
from frontendApp.views.image_gen.image_template.image_template import add_image_template_page, list_image_template_page, update_image_template_page
from frontendApp.views.image_gen.image_tag_template_category_template_mapping.image_tag_template_category_template_mapping import list_image_tag_template_category_template_mapping_page



######### jwt Token  #########
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



permissions_list = [
    
    # Login and forgot
    {"name": "login_page", "route": "", "description": "Login Page", "status": "True", "group": "login"},
    {"name": "email_page", "route": "forgot/", "description": "forgot Page", "status": "True", "group": "login"},
    {"name": "otp_page", "route": "otp/", "description": "otp Page", "status": "True", "group": "login"},
    {"name": "new_password_page", "route": "new-password/", "description": "new password Page", "status": "True", "group": "login"},
    {"name": "registration_enter_otp_page", "route": "verify-otp/", "description": "new password Page", "status": "True", "group": "login"},
   
    # {"name": "send_otp", "route": "send-otp/", "description": "Send otp Mails", "status": "True", "group": "login"},
    # {"name": "check_otp", "route": "check-otp/", "description": "Check otp Mails", "status": "True", "group": "login"},
    # {"name": "set_new_password", "route": "new-password/", "description": "Set New Password Page", "status": "True", "group": "login"},
    {"name": "dashboard_page", "route": "dashboard/", "description": "dashboard Page", "status": "True", "group": "login"},
    
    # onboard
    {"name": "onboard_page", "route": "onboard/", "description": "onboard Page", "status": "True", "group": "onboard"},
    
    # user_profile_page
    {"name": "user_profile_page", "route": "profile/", "description": "user profile page Page", "status": "True", "group": "user profile page"},

    # #  registration
    # {"name": "check_invitation_code", "route": "check-invitation-code/", "description": "check-invitation-code Page", "status": "True", "group": "registration"},
    # {"name": "admin_registration", "route": "registration/", "description": "registration Page", "status": "True", "group": "registration"},
    # {"name": "registration_check_otp", "route": "registration-check-otp/", "description": "registration-check-otp Page", "status": "True", "group": "registration"},
   
   
    # role
    {"name": "list_role_page", "route": "roles/", "description": "role Page", "status": "True", "group": "role"},
    {"name": "add_role_page", "route": "role/add/", "description": "add role Page", "status": "True", "group": "role"},
    {"name": "update_role_page", "route": "role/update/<slug:slug_id>", "description": "update role Page", "status": "True", "group": "role"},
   
    # permission
    {"name": "list_permission_page", "route": "permissions/", "description": "permission Page", "status": "True", "group": "permission"},
    {"name": "add_permission_page", "route": "permission/add/", "description": "add permission Page", "status": "True", "group": "permission"},
    {"name": "update_permission_page", "route": "permission/update/<slug:slug_id>", "description": "update permission Page", "status": "True", "group": "permission"},
    
    # article_type_field
    {"name": "list_article_type_field_page", "route": "article-type-fields/", "description": "article-type-field Page", "status": "True", "group": "article-type-field"},
    {"name": "add_article_type_field_page", "route": "article-type-field/add/", "description": "add article-type-field Page", "status": "True", "group": "article-type-field"},
    {"name": "update_article_type_field_page", "route": "article-type-field/update/<slug:slug_id>", "description": "update article-type-field Page", "status": "True", "group": "article-type-field"},
    
    # article_type
    {"name": "list_article_type_page", "route": "article-types/", "description": "article-type Page", "status": "True", "group": "article-type"},
    {"name": "add_article_type_page", "route": "article-type/add/", "description": "add article-type Page", "status": "True", "group": "article-type"},
    {"name": "update_article_type_page", "route": "article-type/update/<slug:slug_id>", "description": "update article-type Page", "status": "True", "group": "article-type"},
    
    # language
    {"name": "list_language_page", "route": "languages/", "description": "language Page", "status": "True", "group": "language"},
    {"name": "add_language_page", "route": "language/add/", "description": "add language Page", "status": "True", "group": "language"},
    {"name": "update_language_page", "route": "language/update/<slug:slug_id>", "description": "update language Page", "status": "True", "group": "language"},
    
    # country
    {"name": "list_country_page", "route": "countries/", "description": "country Page", "status": "True", "group": "country"},
    {"name": "add_country_page", "route": "country/add/", "description": "add country Page", "status": "True", "group": "country"},
    {"name": "update_country_page", "route": "country/update/<slug:slug_id>", "description": "update country Page", "status": "True", "group": "country"},
    
    # color_detail
    {"name": "list_color_detail_page", "route": "colors/", "description": "color Page", "status": "True", "group": "color"},
    {"name": "add_color_detail_page", "route": "color/add/", "description": "add color Page", "status": "True", "group": "color"},
    {"name": "update_color_detail_page", "route": "color/update/<slug:slug_id>", "description": "update color Page", "status": "True", "group": "color"},
    
    # invitation_code_detail
    {"name": "list_invitation_code_detail_page", "route": "invitation-codes/", "description": "invitation-code Page", "status": "True", "group": "invitation-code"},
    {"name": "add_invitation_code_detail_page", "route": "invitation-code/add/", "description": "add invitation-code Page", "status": "True", "group": "invitation-code"},
    {"name": "update_invitation_code_detail_page", "route": "invitation-code/update/<slug:slug_id>", "description": "update invitation-code Page", "status": "True", "group": "invitation-code"},
    
    # dynamic_avatar_image
    {"name": "list_dynamic_avatar_image_page", "route": "dynamic-avatar-images/", "description": "dynamic-avatar-image Page", "status": "True", "group": "dynamic-avatar-image"},
    {"name": "add_dynamic_avatar_image_page", "route": "dynamic-avatar-image/add/", "description": "add dynamic-avatar-image Page", "status": "True", "group": "dynamic-avatar-image"},
    {"name": "update_dynamic_avatar_image_page", "route": "dynamic-avatar-image/update/<slug:slug_id>", "description": "update dynamic-avatar-image Page", "status": "True", "group": "dynamic-avatar-image"},

    # workspace
    {"name": "list_workspace_page", "route": "workspaces/", "description": "workspace Page", "status": "True", "group": "workspace"},
    {"name": "add_workspace_page", "route": "workspace/add/", "description": "add workspace Page", "status": "True", "group": "workspace"},
    {"name": "update_workspace_page", "route": "workspace/update/<slug:slug_id>", "description": "update workspace Page", "status": "True", "group": "workspace"},

    # motivation
    {"name": "list_motivation_page", "route": "motivations/", "description": "motivation Page", "status": "True", "group": "motivation"},
    {"name": "add_motivation_page", "route": "motivation/add/", "description": "add motivation Page", "status": "True", "group": "motivation"},
    {"name": "update_motivation_page", "route": "motivation/update/<slug:slug_id>", "description": "update motivation Page", "status": "True", "group": "motivation"},

    # prompt
    {"name": "list_prompt_page", "route": "prompts/", "description": "prompt Page", "status": "True", "group": "prompt"},
    {"name": "add_prompt_page", "route": "prompt/add/", "description": "add prompt Page", "status": "True", "group": "prompt"},
    {"name": "update_prompt_page", "route": "prompt/update/<slug:slug_id>", "description": "update prompt Page", "status": "True", "group": "prompt"},
    
    # user_detail
    {"name": "list_user_detail_page", "route": "users/", "description": "user-detail Page", "status": "True", "group": "user-detail"},
    {"name": "add_user_detail_page", "route": "user/add/", "description": "add user-detail Page", "status": "True", "group": "user-detail"},
    {"name": "update_user_detail_page", "route": "user/update/<slug:slug_id>", "description": "update user-detail Page", "status": "True", "group": "user-detail"},
    {"name": "detail_user_page", "route": "user/<slug:slug_id>", "description": "detail user-detail Page", "status": "True", "group": "user-detail"},
    
    # admin_detail
    {"name": "list_admin_detail_page", "route": "admins/", "description": "admin-detail Page", "status": "True", "group": "admin-detail"},
    {"name": "add_admin_detail_page", "route": "admin/add/", "description": "add admin-detail Page", "status": "True", "group": "admin-detail"},
    {"name": "update_admin_detail_page", "route": "admin/update/<slug:slug_id>", "description": "update admin-detail Page", "status": "True", "group": "admin-detail"},
    # {"name": "detail_admin_page", "route": "admin/<slug:slug_id>", "description": "detail admin-detail Page", "status": "True", "group": "admin-detail"},
    
    # domain
    {"name": "list_domain_page", "route": "domains/", "description": "domain Page", "status": "True", "group": "domain"},
    {"name": "add_domain_page", "route": "domain/add/", "description": "add domain Page", "status": "True", "group": "domain"},
    {"name": "update_domain_page", "route": "domain/update/<slug:slug_id>", "description": "update domain Page", "status": "True", "group": "domain"},
    {"name": "detail_domain_page", "route": "domain/<slug:slug_id>", "description": "domain Page", "status": "True", "group": "domain"},
    
    # article
    {"name": "list_article_page", "route": "articles/", "description": "article Page", "status": "True", "group": "article"},
    {"name": "add_article_page", "route": "article/add/", "description": "add article Page", "status": "True", "group": "article"},
    {"name": "update_article_page", "route": "article/update/<slug:slug_id>", "description": "update article Page", "status": "True", "group": "article"},
    
    # error
    {"name": "error_page", "route": "error/", "description": "error Page", "status": "True", "group": "error"},
    # progress_bar_page
    {"name": "progress_bar_page", "route": "fetch/wp-data/", "description": "fetch data Page", "status": "True", "group": "progress_bar_page"},
    #  role_has_permissions
    {"name": "list_role_has_permissions_page", "route": "role-has-permissions/", "description": "role_has_permissions Page", "status": "True", "group": "role_has_permissions"},
    #  notification
    {"name": "list_notification_page", "route": "notifications/", "description": "notification Page", "status": "True", "group": "notification"},
    #  activity_log
    {"name": "list_activity_log_page", "route": "activity-logs/", "description": "activity log Page", "status": "True", "group": "activity log"},
    
    # ai_configuration
    {"name": "list_ai_configuration_page", "route": "ai-configurations/", "description": "ai-configuration Page", "status": "True", "group": "ai-configuration"},
    {"name": "add_ai_configuration_page", "route": "ai-configuration/add/", "description": "add ai-configuration Page", "status": "True", "group": "ai-configuration"},
    {"name": "update_ai_configuration_page", "route": "ai-configuration/update/<slug:slug_id>", "description": "update ai-configuration Page", "status": "True", "group": "ai-configuration"},
    
    # image_kit_configuration
    {"name": "list_image_kit_configuration_page", "route": "image-kit-configurations/", "description": "image-kit-configuration Page", "status": "True", "group": "image-kit-configuration"},
    {"name": "add_image_kit_configuration_page", "route": "image-kit-configuration/add/", "description": "add image-kit-configuration Page", "status": "True", "group": "image-kit-configuration"},
    {"name": "update_image_kit_configuration_page", "route": "image-kit-configuration/update/<slug:slug_id>", "description": "update image-kit-configuration Page", "status": "True", "group": "image-kit-configuration"},

    
    # supportive_prompt_type
    {"name": "list_supportive_prompt_type_page", "route": "supportive-prompt-types/", "description": "all supportive-prompt-type", "status": "True", "group": "supportive-prompt-type"},
    {"name": "add_supportive_prompt_type_page", "route": "supportive-prompt-type/add/", "description": "add supportive-prompt-type", "status": "True", "group": "supportive-prompt-type"},
    {"name": "update_supportive_prompt_type_page", "route": "supportive-prompt-type/update/<slug:slug_id>", "description": "update supportive-prompt-type", "status": "True", "group": "supportive-prompt-type"},
    {"name": "delete_supportive_prompt_type_page", "route": "supportive-prompt-type/delete/<slug:slug_id>", "description": "delete supportive-prompt-type", "status": "True", "group": "supportive-prompt-type"},

    # supportive_prompt
    {"name": "list_supportive_prompt_page", "route": "supportive-prompts/", "description": "all supportive-prompt", "status": "True", "group": "supportive-prompt"},
    {"name": "add_supportive_prompt_page", "route": "supportive-prompt/add/", "description": "add supportive-prompt", "status": "True", "group": "supportive-prompt"},
    {"name": "update_supportive_prompt_page", "route": "supportive-prompt/update/<slug:slug_id>", "description": "update supportive-prompt", "status": "True", "group": "supportive-prompt"},
    {"name": "delete_supportive_prompt_page", "route": "supportive-prompt/delete/<slug:slug_id>", "description": "delete supportive-prompt", "status": "True", "group": "supportive-prompt"},

    # list_queues_page
    {"name": "list_queues_page", "route": "queues/", "description": "all queues", "status": "True", "group": "list-queues"},
    # list_ai_rate_limiter_page
    {"name": "list_ai_rate_limiter_page", "route": "ai-rate-limiters/", "description": "all ai-rate-limiters", "status": "True", "group": "list-ai-rate-limiters"},


    # integration
    {"name": "list_integration_page", "route": "integrations/", "description": "all integrations", "status": "True", "group": "integrations"},
    {"name": "add_integration_page", "route": "integration/add/", "description": "add integrations", "status": "True", "group": "integrations"},
    {"name": "update_integration_page", "route": "integration/update/<slug:slug_id>", "description": "update integrations", "status": "True", "group": "integrations"},
    {"name": "delete_integration_page", "route": "integration/delete/<slug:slug_id>", "description": "delete integrations", "status": "True", "group": "integrations"},




    ######### image gen  #########

    # image_tag
    {"name": "list_image_tag_page", "route": "image-tags/", "description": "image-tag Page", "status": "True", "group": "image-tag"},
    {"name": "add_image_tag_page", "route": "image-tag/add/", "description": "add image-tag Page", "status": "True", "group": "image-tag"},
    {"name": "update_image_tag_page", "route": "image-tag/update/<slug:slug_id>", "description": "update image-tag Page", "status": "True", "group": "image-tag"},
    
    # image_template
    {"name": "list_image_template_page", "route": "image-templates/", "description": "image-template Page", "status": "True", "group": "image-template"},
    {"name": "add_image_template_page", "route": "image-template/add/", "description": "add image-template Page", "status": "True", "group": "image-template"},
    {"name": "update_image_template_page", "route": "image-template/update/<slug:slug_id>", "description": "update image-template Page", "status": "True", "group": "image-template"},
    
    # image_template_category
    {"name": "list_image_template_category_page", "route": "image-template-categories/", "description": "image-template-category Page", "status": "True", "group": "image-template-category"},
    {"name": "add_image_template_category_page", "route": "image-template-category/add/", "description": "add image-template-category Page", "status": "True", "group": "image-template-category"},
    {"name": "update_image_template_category_page", "route": "image-template-category/update/<slug:slug_id>", "description": "update image-template-category Page", "status": "True", "group": "image-template-category"},
    
    # list_image_tag_template_category_template_mapping
    {"name": "list_image_tag_template_category_template_mapping_page", "route": "list-image-tag-template-category-template-mapping/", "description": "image-tag-template-category-template-mapping Page", "status": "True", "group": "image-tag-template-category-template-mapping"},
    # {"name": "add_image_template_category_page", "route": "image-template-category/add/", "description": "add image-template-category Page", "status": "True", "group": "image-template-category"},
    # {"name": "update_image_template_category_page", "route": "image-template-category/update/<slug:slug_id>", "description": "update image-template-category Page", "status": "True", "group": "image-template-category"},

]


urlpatterns = []
for perm in permissions_list:
    view_name = perm["name"]
    # view_name = perm["name"].replace("_page", "")
    # Dynamically get the view class
    view_class = globals().get(view_name)
    
    if view_class:
        # If it's a class-based view, invoke .as_view() to get the callable view
        view = view_class.as_view() if hasattr(view_class, 'as_view') else view_class
        urlpatterns.append(path(route=perm["route"], view=view, name=view_name.replace(".as_view", "")))






urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

