# from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required

######### file import  #########
from apiApp.views.auth.login import admin_login
from apiApp.views.auth.logout import admin_logout
from apiApp.views.auth.registration import check_invitation_code, admin_registration, registration_check_otp
from apiApp.views.auth.forgot_password import send_otp, check_otp, set_new_password
from apiApp.views.invitation_code_detail.invitation_code_detail import list_invitation_code_detail, add_invitation_code_detail, update_invitation_code_detail, delete_invitation_code_detail
from apiApp.views.invitation_code_detail.generate_invitation_code import generate_invitation_code 
from apiApp.views.role.role import list_role, add_role, update_role, delete_role
from apiApp.views.permission.permission import list_permission, add_permission, update_permission, delete_permission
from apiApp.views.dynamic_avatar_image.dynamic_avatar_image import list_dynamic_avatar_image, add_dynamic_avatar_image, update_dynamic_avatar_image, delete_dynamic_avatar_image
from apiApp.views.workspace.workspace import list_workspace, add_workspace, update_workspace, delete_workspace
# from apiApp.views.set_workspace.set_workspace import set_workspace
from apiApp.views.ai_configuration.ai_configuration import list_ai_configuration, add_ai_configuration, update_ai_configuration, delete_ai_configuration 
from apiApp.views.ai_configuration.verify_ai_configuration import verify_ai_configuration 
from apiApp.views.image_kit_configuration.image_kit_configuration import list_image_kit_configuration, add_image_kit_configuration, update_image_kit_configuration, delete_image_kit_configuration 
from apiApp.views.image_kit_configuration.verify_image_kit_configuration import verify_image_kit_configuration 
from apiApp.views.user_detail.user_detail import list_user_detail, add_user_detail, update_user_detail, delete_user_detail
from apiApp.views.user_detail.user_detail_action import revoke_workspace_from_user, add_workspace_to_user
from apiApp.views.admin_detail.admin_detail import list_admin_detail, add_admin_detail, update_admin_detail, delete_admin_detail
from apiApp.views.role_has_permissions.role_has_permissions import list_role_has_permissions, add_role_has_permissions, update_role_has_permissions
from apiApp.views.domain.domain import list_domain, add_domain, update_domain, delete_domain
from apiApp.views.domain.domain_action import revoke_domain_from_user, add_domain_to_user, list_revoke_domain_from_user
from apiApp.views.wordpress.test_api.test_tag import add_test_tag, delete_test_tag
from apiApp.views.wordpress.test_api.test_category import add_test_category, delete_test_category
from apiApp.views.wordpress.test_api.test_article import add_test_article, delete_test_article
from apiApp.views.tag.tag import list_tag, add_tag, update_tag, delete_tag
from apiApp.views.category.category import list_category, add_category, update_category, delete_category
from apiApp.views.author.author import list_author, add_author, update_author, delete_author
from apiApp.views.color_detail.color_detail import list_color_detail, add_color_detail, update_color_detail, delete_color_detail
from apiApp.views.language.language import list_language, add_language, update_language, delete_language
from apiApp.views.country.country import list_country, add_country, update_country, delete_country
from apiApp.views.motivation.motivation import list_motivation, add_motivation, update_motivation, delete_motivation
from apiApp.views.motivation.process_motivation import process_motivation
from apiApp.views.article_type_field.article_type_field import list_article_type_field, add_article_type_field, update_article_type_field, delete_article_type_field
from apiApp.views.article_type.article_type import list_article_type, add_article_type, update_article_type, delete_article_type, get_article_type_fields
from apiApp.views.prompt.prompt import list_prompt, add_prompt, update_prompt, delete_prompt
from apiApp.views.wordpress.fetch_data.fetch_category_data import fetch_category_data
from apiApp.views.wordpress.fetch_data.fetch_tag_data import fetch_tag_data
from apiApp.views.wordpress.fetch_data.fetch_author_data import fetch_author_data
from apiApp.views.wordpress.fetch_data.fetch_article_data import fetch_article_data
from apiApp.views.wordpress.fetch_data.fetch_console_metrics_data import fetch_console_metrics_data
from apiApp.views.wordpress.fetch_data.fetch_analytics_metrics_data import fetch_analytics_metrics_data
from apiApp.views.wordpress.fetch_data.fetch_wp_data import fetch_wp_data
from apiApp.views.wordpress.perma_links.perma_links import list_perma_links, update_perma_links
from apiApp.views.article.article import list_article, add_article, update_article, delete_article
from apiApp.views.competitor.competitor import list_competitor, add_competitor, update_competitor, delete_competitor
from apiApp.views.competitor_domain_mapping.competitor_domain_mapping import list_competitor_domain_mapping, add_competitor_domain_mapping, update_competitor_domain_mapping, delete_competitor_domain_mapping
from apiApp.views.competitor_sitemap_url.competitor_sitemap_url import list_competitor_sitemap_url, add_competitor_sitemap_url, update_competitor_sitemap_url, delete_competitor_sitemap_url
from apiApp.views.competitor_sitemap_url_mapping.competitor_sitemap_url_mapping import list_competitor_sitemap_url_mapping, add_competitor_sitemap_url_mapping, update_competitor_sitemap_url_mapping, delete_competitor_sitemap_url_mapping
from apiApp.views.competitor_article_url.competitor_article_url import list_competitor_article_url, add_competitor_article_url, update_competitor_article_url, delete_competitor_article_url
from apiApp.views.competitor_article_url_mapping.competitor_article_url_mapping import list_competitor_article_url_mapping, add_competitor_article_url_mapping, update_competitor_article_url_mapping, delete_competitor_article_url_mapping
from apiApp.views.competitor_extraction.competitor_extraction import list_competitor_extraction, add_competitor_extraction, update_competitor_extraction, delete_competitor_extraction
from apiApp.views.competitor_extraction_mapping.competitor_extraction_mapping import list_competitor_extraction_mapping, add_competitor_extraction_mapping, update_competitor_extraction_mapping, delete_competitor_extraction_mapping
from apiApp.views.competitor_seo_extraction_mapping.competitor_seo_extraction_mapping import list_competitor_seo_extraction_mapping, add_competitor_seo_extraction_mapping, update_competitor_seo_extraction_mapping, delete_competitor_seo_extraction_mapping
from apiApp.views.user_api_key.user_api_key import list_user_api_key, add_user_api_key, update_user_api_key, delete_user_api_key
from apiApp.views.user_api_key.generate_user_api_key import generate_user_api_key
from apiApp.views.keyword.keyword import list_keyword, add_keyword, update_keyword, delete_keyword
from apiApp.views.user_profile.user_profile import list_user_profile, update_user_profile
from apiApp.views.base.graph_data.domain_console_metrics.domain_console_metrics import domain_console_metrics
from apiApp.views.base.graph_data.domain_analytics_metrics.domain_analytics_metrics import domain_analytics_metrics
from apiApp.views.base.graph_data.article_console_metrics.article_console_metrics import article_console_metrics
from apiApp.views.base.graph_data.article_analytics_metrics.article_analytics_metrics import article_analytics_metrics
from apiApp.views.base.graph_data.domain_article_metrics.domain_article_metrics import domain_article_metrics
from apiApp.views.console_metrics.console_metrics import list_console_metrics
from apiApp.views.progres_data.progres_data import progres_data
from apiApp.views.image_gen.generate_template.generate_template import generate_template
from apiApp.views.activity_log.activity_log import list_activity_log
from apiApp.views.notification.notification import list_notification, delete_notification, process_notification
from apiApp.views.fetch_user_workspaces.fetch_user_workspaces import fetch_user_workspaces
from apiApp.views.article_info.article_info import list_article_info

from apiApp.views.supportive_prompt_type.supportive_prompt_type import list_supportive_prompt_type, add_supportive_prompt_type, update_supportive_prompt_type, delete_supportive_prompt_type
from apiApp.views.supportive_prompt.supportive_prompt import list_supportive_prompt, add_supportive_prompt, update_supportive_prompt, delete_supportive_prompt
from apiApp.views.variables.variables import list_variables


######### image gen  #########
from apiApp.views.image_gen.image_tag.image_tag import list_image_tag, add_image_tag, update_image_tag, delete_image_tag
from apiApp.views.image_gen.image_template_category.image_template_category import list_image_template_category, add_image_template_category, update_image_template_category, delete_image_template_category
from apiApp.views.image_gen.image_template.image_template import list_image_template, get_superadmin_templates, add_image_template, update_image_template, delete_image_template
from apiApp.views.image_gen.image_tag_template_category_template_mapping.image_tag_template_category_template_mapping import list_image_tag_template_category_template_mapping, add_image_tag_template_category_template_mapping, update_image_tag_template_category_template_mapping, delete_image_tag_template_category_template_mapping
from apiApp.views.image_gen.generate_single_image.generate_single_image import generate_single_image

    
######### jwt Token  #########
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



permissions_list = [
    
    ######### jwt Token  #########
    {"name": "TokenRefreshView", "route": "get-refresh-token/", "description": "jwt", "status": "True", "group": "jwt"},
    {"name": "TokenObtainPairView", "route": "get-token/", "description": "jwt", "status": "True", "group": "jwt"},

    # Login and forgot
    {"name": "admin_login", "route": "login/", "description": "Login Page", "status": "True", "group": "login"},
    {"name": "admin_logout", "route": "logout/", "description": "Logout Page", "status": "True", "group": "login"},
    {"name": "send_otp", "route": "send-otp/", "description": "Send otp Mails", "status": "True", "group": "login"},
    {"name": "check_otp", "route": "check-otp/", "description": "Check otp Mails", "status": "True", "group": "login"},
    {"name": "set_new_password", "route": "new-password/", "description": "Set New Password Page", "status": "True", "group": "login"},
    {"name": "fetch_user_workspaces", "route": "fetch-workspaces/", "description": "fetch-workspaces", "status": "True", "group": "login"},

    #  registration
    {"name": "check_invitation_code", "route": "check-invitation-code/", "description": "check-invitation-code Page", "status": "True", "group": "registration"},
    {"name": "admin_registration", "route": "registration/", "description": "registration Page", "status": "True", "group": "registration"},
    {"name": "registration_check_otp", "route": "registration-check-otp/", "description": "registration-check-otp Page", "status": "True", "group": "registration"},
    
    # invitation code details
    {"name": "list_invitation_code_detail", "route": "invitation-code-details/", "description": "all invitation code details", "status": "True", "group": "invitation-code-detail"},
    {"name": "add_invitation_code_detail", "route": "invitation-code-detail/add/", "description": "add invitation code details", "status": "True", "group": "invitation-code-detail"},
    {"name": "update_invitation_code_detail", "route": "invitation-code-detail/update/<slug:slug_id>", "description": "update invitation code details", "status": "True", "group": "invitation-code-detail"},
    {"name": "delete_invitation_code_detail", "route": "invitation-code-detail/delete/<slug:slug_id>", "description": "delete invitation code details", "status": "True", "group": "invitation-code-detail"},
    {"name": "generate_invitation_code", "route": "generate-invitation-code/", "description": "Generate invitation code details", "status": "True", "group": "invitation-code-detail"},
    
    # role
    {"name": "list_role", "route": "roles/", "description": "all role", "status": "True", "group": "role"},
    {"name": "add_role", "route": "role/add/", "description": "add role", "status": "True", "group": "role"},
    {"name": "update_role", "route": "role/update/<slug:slug_id>", "description": "update role", "status": "True", "group": "role"},
    {"name": "delete_role", "route": "role/delete/<slug:slug_id>", "description": "delete role", "status": "True", "group": "role"},
    
    # permission
    {"name": "list_permission", "route": "permissions/", "description": "all permission", "status": "True", "group": "permission"},
    {"name": "add_permission", "route": "permission/add/", "description": "add permission", "status": "True", "group": "permission"},
    {"name": "update_permission", "route": "permission/update/<slug:slug_id>", "description": "update permission", "status": "True", "group": "permission"},
    {"name": "delete_permission", "route": "permission/delete/<slug:slug_id>", "description": "delete permission", "status": "True", "group": "permission"},
    
    # role has permissions
    {"name": "list_role_has_permissions", "route": "role-has-permissions/", "description": "delete admin", "status": "True", "group": "role-has-permissions"},
    {"name": "add_role_has_permissions", "route": "role-has-permission/add/", "description": "delete admin", "status": "True", "group": "role-has-permissions"},
    {"name": "update_role_has_permissions", "route": "role-has-permission/update/", "description": "delete admin", "status": "True", "group": "role-has-permissions"},
    
    # dynamic avatar image
    {"name": "list_dynamic_avatar_image", "route": "dynamic-avatar-images/", "description": "all dynamic-avatar-images", "status": "True", "group": "dynamic-avatar-image"},
    {"name": "add_dynamic_avatar_image", "route": "dynamic-avatar-image/add/", "description": "add dynamic-avatar-image", "status": "True", "group": "dynamic-avatar-image"},
    {"name": "update_dynamic_avatar_image", "route": "dynamic-avatar-image/update/<slug:slug_id>", "description": "update dynamic-avatar-image", "status": "True", "group": "dynamic-avatar-image"},
    {"name": "delete_dynamic_avatar_image", "route": "dynamic-avatar-image/delete/<slug:slug_id>", "description": "delete dynamic-avatar-image", "status": "True", "group": "dynamic-avatar-image"},

    # workspace
    {"name": "list_workspace", "route": "workspaces/", "description": "all workspace", "status": "True", "group": "workspace"},
    {"name": "add_workspace", "route": "workspace/add/", "description": "add workspace", "status": "True", "group": "workspace"},
    {"name": "update_workspace", "route": "workspace/update/<slug:slug_id>", "description": "update workspace", "status": "True", "group": "workspace"},
    {"name": "delete_workspace", "route": "workspace/delete/<slug:slug_id>", "description": "delete workspace", "status": "True", "group": "workspace"},
    
    # # set workspace
    # {"name": "set_workspace", "route": "set/workspace/", "description": "set workspace", "status": "True", "group": "base"},
    
    # ai configuration
    {"name": "list_ai_configuration", "route": "ai-configurations/", "description": "all ai-configuration", "status": "True", "group": "ai-configuration"},
    {"name": "add_ai_configuration", "route": "ai-configuration/add/", "description": "add ai-configuration", "status": "True", "group": "ai-configuration"},
    {"name": "update_ai_configuration", "route": "ai-configuration/update/<slug:slug_id>", "description": "update ai-configuration", "status": "True", "group": "ai-configuration"},
    {"name": "delete_ai_configuration", "route": "ai-configuration/delete/<slug:slug_id>", "description": "delete ai-configuration", "status": "True", "group": "ai-configuration"},

    # verify ai configuration
    {"name": "verify_ai_configuration", "route": "ai-configuration/verify/", "description": "verify ai-configuration", "status": "True", "group": "ai-configuration"},
    
    # user detail
    {"name": "list_user_detail", "route": "users/", "description": "all user", "status": "True", "group": "user"},
    {"name": "add_user_detail", "route": "user/add/", "description": "add user", "status": "True", "group": "user"},
    {"name": "update_user_detail", "route": "user/update/<slug:slug_id>", "description": "update user", "status": "True", "group": "user"},
    {"name": "delete_user_detail", "route": "user/delete/<slug:slug_id>", "description": "delete user", "status": "True", "group": "user"},
    
    #  user revoke and add in workspce
    {"name": "revoke_workspace_from_user", "route": "user/revoke/workspace/<slug:slug_id>", "description": "revoke user", "status": "True", "group": "user"},
    {"name": "add_workspace_to_user", "route": "user/add/workspace/", "description": "revoke user", "status": "True", "group": "user"},
    
    # admin detail
    {"name": "list_admin_detail", "route": "admins/", "description": "all admin", "status": "True", "group": "admin"},
    {"name": "add_admin_detail", "route": "admin/add/", "description": "add admin", "status": "True", "group": "admin"},
    {"name": "update_admin_detail", "route": "admin/update/<slug:slug_id>", "description": "update admin", "status": "True", "group": "admin"},
    {"name": "delete_admin_detail", "route": "admin/delete/<slug:slug_id>", "description": "delete admin", "status": "True", "group": "admin"},
    
    # domain
    {"name": "list_domain", "route": "domains/", "description": "all domain", "status": "True", "group": "domain"},
    {"name": "add_domain", "route": "domain/add/", "description": "add domain", "status": "True", "group": "domain"},
    {"name": "update_domain", "route": "domain/update/<slug:slug_id>", "description": "update domain", "status": "True", "group": "domain"},
    {"name": "delete_domain", "route": "domain/delete/<slug:slug_id>", "description": "delete domain", "status": "True", "group": "domain"},

    #  user revoke and add in domain
    {"name": "revoke_domain_from_user", "route": "user/revoke/domain/<slug:slug_id>", "description": "revoke user", "status": "True", "group": "domain"},
    {"name": "add_domain_to_user", "route": "user/add/domain/", "description": "revoke user", "status": "True", "group": "domain"},
    {"name": "list_revoke_domain_from_user", "route": "user/domains/<slug:slug_id>", "description": "revoke user", "status": "True", "group": "domain"},


    # test wordpress api Article 
    {"name": "add_test_article", "route": "test-article/add/", "description": "test-article-add", "status": "True", "group": "test-article"},
    {"name": "delete_test_article", "route": "test-article/delete/", "description": "test-article-delete", "status": "True", "group": "test-article"},
    
    # test wordpress api Tag 
    {"name": "add_test_tag", "route": "test-tag/add/", "description": "test-tag-add", "status": "True", "group": "test-tag"},
    {"name": "delete_test_tag", "route": "test-tag/delete/", "description": "test-tag-delete", "status": "True", "group": "test-tag"},

    # test wordpress api category 
    {"name": "add_test_category", "route": "test-category/add/", "description": "test-category-add", "status": "True", "group": "test-category"},
    {"name": "delete_test_category", "route": "test-category/delete/", "description": "test-category-delete", "status": "True", "group": "test-category"},

    # wp tag
    {"name": "list_tag", "route": "tags/", "description": "all tag", "status": "True", "group": "tag"},
    {"name": "add_tag", "route": "tag/add/", "description": "add tag", "status": "True", "group": "tag"},
    {"name": "update_tag", "route": "tag/update/<slug:slug_id>", "description": "update tag", "status": "True", "group": "tag"},
    {"name": "delete_tag", "route": "tag/delete/<slug:slug_id>", "description": "delete tag", "status": "True", "group": "tag"},
    
    # wp category
    {"name": "list_category", "route": "categories/", "description": "all category", "status": "True", "group": "category"},
    {"name": "add_category", "route": "category/add/", "description": "add category", "status": "True", "group": "category"},
    {"name": "update_category", "route": "category/update/<slug:slug_id>", "description": "update category", "status": "True", "group": "category"},
    {"name": "delete_category", "route": "category/delete/<slug:slug_id>", "description": "delete category", "status": "True", "group": "category"},
  
    # wp author
    {"name": "list_author", "route": "authors/", "description": "all author", "status": "True", "group": "author"},
    {"name": "add_author", "route": "author/add/", "description": "add author", "status": "True", "group": "author"},
    {"name": "update_author", "route": "author/update/<slug:slug_id>", "description": "update author", "status": "True", "group": "author"},
    {"name": "delete_author", "route": "author/delete/<slug:slug_id>", "description": "delete author", "status": "True", "group": "author"},
    
    # color detail
    {"name": "list_color_detail", "route": "colors/", "description": "all color", "status": "True", "group": "color"},
    {"name": "add_color_detail", "route": "color/add/", "description": "add color", "status": "True", "group": "color"},
    {"name": "update_color_detail", "route": "color/update/<slug:slug_id>", "description": "update color", "status": "True", "group": "color"},
    {"name": "delete_color_detail", "route": "color/delete/<slug:slug_id>", "description": "delete color", "status": "True", "group": "color"},
    
    # language
    {"name": "list_language", "route": "languages/", "description": "all language", "status": "True", "group": "language"},
    {"name": "add_language", "route": "language/add/", "description": "add language", "status": "True", "group": "language"},
    {"name": "update_language", "route": "language/update/<slug:slug_id>", "description": "update language", "status": "True", "group": "language"},
    {"name": "delete_language", "route": "language/delete/<slug:slug_id>", "description": "delete language", "status": "True", "group": "language"},
    
    # country
    {"name": "list_country", "route": "countries/", "description": "all country", "status": "True", "group": "country"},
    {"name": "add_country", "route": "country/add/", "description": "add country", "status": "True", "group": "country"},
    {"name": "update_country", "route": "country/update/<slug:slug_id>", "description": "update country", "status": "True", "group": "country"},
    {"name": "delete_country", "route": "country/delete/<slug:slug_id>", "description": "delete country", "status": "True", "group": "country"},
    
    # motivation
    {"name": "list_motivation", "route": "motivations/", "description": "all motivation", "status": "True", "group": "motivation"},
    {"name": "add_motivation", "route": "motivation/add/", "description": "add motivation", "status": "True", "group": "motivation"},
    {"name": "update_motivation", "route": "motivation/update/<slug:slug_id>", "description": "update motivation", "status": "True", "group": "motivation"},
    {"name": "delete_motivation", "route": "motivation/delete/<slug:slug_id>", "description": "delete motivation", "status": "True", "group": "motivation"},
    {"name": "process_motivation", "route": "process-motivation/", "description": "process motivation", "status": "True", "group": "motivation"},
    
    # article type field
    {"name": "list_article_type_field", "route": "article-type-fields/", "description": "all article-type-field", "status": "True", "group": "article-type-field"},
    {"name": "add_article_type_field", "route": "article-type-field/add/", "description": "add article-type-field", "status": "True", "group": "article-type-field"},
    {"name": "update_article_type_field", "route": "article-type-field/update/<slug:slug_id>", "description": "update article-type-field", "status": "True", "group": "article-type-field"},
    {"name": "delete_article_type_field", "route": "article-type-field/delete/<slug:slug_id>", "description": "delete article-type-field", "status": "True", "group": "article-type-field"},
    
    # article type
    {"name": "list_article_type", "route": "article-types/", "description": "all article-type", "status": "True", "group": "article-type"},
    {"name": "add_article_type", "route": "article-type/add/", "description": "add article-type", "status": "True", "group": "article-type"},
    {"name": "update_article_type", "route": "article-type/update/<slug:slug_id>", "description": "update article-type", "status": "True", "group": "article-type"},
    {"name": "delete_article_type", "route": "article-type/delete/<slug:slug_id>", "description": "delete article-type", "status": "True", "group": "article-type"},
    {"name": "get_article_type_fields", "route": "get/article-type-fields/<slug:slug_id>", "description": "get-article-type-fields", "status": "True", "group": "get-article-type-fields"},
    
    # prompt
    {"name": "list_prompt", "route": "prompts/", "description": "all prompt", "status": "True", "group": "prompt"},
    {"name": "add_prompt", "route": "prompt/add/", "description": "add prompt", "status": "True", "group": "prompt"},
    {"name": "update_prompt", "route": "prompt/update/<slug:slug_id>", "description": "update prompt", "status": "True", "group": "prompt"},
    {"name": "delete_prompt", "route": "prompt/delete/<slug:slug_id>", "description": "delete prompt", "status": "True", "group": "prompt"},
    
    # fetch wp category
    {"name": "fetch_category_data", "route": "fetch/category/", "description": "fetch-category", "status": "True", "group": "fetch-category"},
    # fetch wp tag
    {"name": "fetch_tag_data", "route": "fetch/tag/", "description": "fetch-tag", "status": "True", "group": "fetch-tag"},
    # fetch wp author
    {"name": "fetch_author_data", "route": "fetch/author/", "description": "fetch-author", "status": "True", "group": "fetch-author"},
    # fetch wp article
    {"name": "fetch_article_data", "route": "fetch/article/", "description": "fetch-article", "status": "True", "group": "fetch-article"},
    # fetch wp console metrics
    {"name": "fetch_console_metrics_data", "route": "fetch/console-metrics/", "description": "fetch-console-metrics", "status": "True", "group": "fetch-console-metrics"},
    # fetch wp analytics metrics
    {"name": "fetch_analytics_metrics_data", "route": "fetch/analytics-metrics/", "description": "fetch-analytics-metrics", "status": "True", "group": "fetch-analytics-metrics"},
    # fetch wp data for progressbar page 
    {"name": "fetch_wp_data", "route": "fetch/data/", "description": "fetch-data", "status": "True", "group": "fetch-data"},
    # list activity log 
    {"name": "list_activity_log", "route": "activity-logs/", "description": "activity-log", "status": "True", "group": "activity-log"},
  
    # perma_links
    {"name": "list_perma_links", "route": "perma-links/", "description": "perma-links", "status": "True", "group": "perma-links"},
    {"name": "update_perma_links", "route": "perma-links/update/", "description": "perma-links", "status": "True", "group": "perma-links"},
  
    # list notification 
    {"name": "list_notification", "route": "notifications/", "description": "notification", "status": "True", "group": "notification"},
    {"name": "process_notification", "route": "process-notification/", "description": "process notification", "status": "True", "group": "notification"},
    {"name": "delete_notification", "route": "notification/delete/<slug:slug_id>", "description": "delete notification", "status": "True", "group": "notification"},
    
    
    # article
    {"name": "list_article", "route": "articles/", "description": "all article", "status": "True", "group": "article"},
    {"name": "add_article", "route": "article/add/", "description": "add article", "status": "True", "group": "article"},
    {"name": "update_article", "route": "article/update/<slug:slug_id>", "description": "update article", "status": "True", "group": "article"},
    {"name": "delete_article", "route": "article/delete/<slug:slug_id>", "description": "delete article", "status": "True", "group": "article"},
    
    # list_article_info
    {"name": "list_article_info", "route": "info/articles/", "description": "info article", "status": "True", "group": "article"},
    
    # competitor
    {"name": "list_competitor", "route": "competitors/", "description": "all competitor", "status": "True", "group": "competitor"},
    {"name": "add_competitor", "route": "competitor/add/", "description": "add competitor", "status": "True", "group": "competitor"},
    {"name": "update_competitor", "route": "competitor/update/<slug:slug_id>", "description": "update competitor", "status": "True", "group": "competitor"},
    {"name": "delete_competitor", "route": "competitor/delete/<slug:slug_id>", "description": "delete competitor", "status": "True", "group": "competitor"},
    
    # competitor domain mapping
    {"name": "list_competitor_domain_mapping", "route": "competitor-domain-mappings/", "description": "all competitor-domain-mapping", "status": "True", "group": "competitor-domain-mapping"},
    {"name": "add_competitor_domain_mapping", "route": "competitor-domain-mapping/add/", "description": "add competitor-domain-mapping", "status": "True", "group": "competitor-domain-mapping"},
    {"name": "update_competitor_domain_mapping", "route": "competitor-domain-mapping/update/<slug:slug_id>", "description": "update competitor-domain-mapping", "status": "True", "group": "competitor-domain-mapping"},
    {"name": "delete_competitor_domain_mapping", "route": "competitor-domain-mapping/delete/<slug:slug_id>", "description": "delete competitor-domain-mapping", "status": "True", "group": "competitor-domain-mapping"},
    
    # competitor sitemap url
    {"name": "list_competitor_sitemap_url", "route": "competitor-sitemap-urls/", "description": "all competitor-sitemap-url", "status": "True", "group": "competitor-sitemap-url"},
    {"name": "add_competitor_sitemap_url", "route": "competitor-sitemap-url/add/", "description": "add competitor-sitemap-url", "status": "True", "group": "competitor-sitemap-url"},
    {"name": "update_competitor_sitemap_url", "route": "competitor-sitemap-url/update/<slug:slug_id>", "description": "update competitor-sitemap-url", "status": "True", "group": "competitor-sitemap-url"},
    {"name": "delete_competitor_sitemap_url", "route": "competitor-sitemap-url/delete/<slug:slug_id>", "description": "delete competitor-sitemap-url", "status": "True", "group": "competitor-sitemap-url"},
  
    # competitor sitemap url mapping
    {"name": "list_competitor_sitemap_url_mapping", "route": "competitor-sitemap-url-mappings/", "description": "all competitor-sitemap-url-mapping", "status": "True", "group": "competitor-sitemap-url-mapping"},
    {"name": "add_competitor_sitemap_url_mapping", "route": "competitor-sitemap-url-mapping/add/", "description": "add competitor-sitemap-url-mapping", "status": "True", "group": "competitor-sitemap-url-mapping"},
    {"name": "update_competitor_sitemap_url_mapping", "route": "competitor-sitemap-url-mapping/update/<slug:slug_id>", "description": "update competitor-sitemap-url-mapping", "status": "True", "group": "competitor-sitemap-url-mapping"},
    {"name": "delete_competitor_sitemap_url_mapping", "route": "competitor-sitemap-url-mapping/delete/<slug:slug_id>", "description": "delete competitor-sitemap-url-mapping", "status": "True", "group": "competitor-sitemap-url-mapping"},
    
    # competitor article url
    {"name": "list_competitor_article_url", "route": "competitor-article-urls/", "description": "all competitor-article-url", "status": "True", "group": "competitor-article-url"},
    {"name": "add_competitor_article_url", "route": "competitor-article-url/add/", "description": "add competitor-article-url", "status": "True", "group": "competitor-article-url"},
    {"name": "update_competitor_article_url", "route": "competitor-article-url/update/<slug:slug_id>", "description": "update competitor-article-url", "status": "True", "group": "competitor-article-url"},
    {"name": "delete_competitor_article_url", "route": "competitor-article-url/delete/<slug:slug_id>", "description": "delete competitor-article-url", "status": "True", "group": "competitor-article-url"},
    
    # competitor article url mapping
    {"name": "list_competitor_article_url_mapping", "route": "competitor-article-url-mappings/", "description": "all competitor-article-url-mapping", "status": "True", "group": "competitor-article-url-mapping"},
    {"name": "add_competitor_article_url_mapping", "route": "competitor-article-url-mapping/add/", "description": "add competitor-article-url-mapping", "status": "True", "group": "competitor-article-url-mapping"},
    {"name": "update_competitor_article_url_mapping", "route": "competitor-article-url-mapping/update/<slug:slug_id>", "description": "update competitor-article-url-mapping", "status": "True", "group": "competitor-article-url-mapping"},
    {"name": "delete_competitor_article_url_mapping", "route": "competitor-article-url-mapping/delete/<slug:slug_id>", "description": "delete competitor-article-url-mapping", "status": "True", "group": "competitor-article-url-mapping"},


    # competitor extraction
    {"name": "list_competitor_extraction", "route": "competitor-extractions/", "description": "all competitor-extraction", "status": "True", "group": "competitor-extraction"},
    {"name": "add_competitor_extraction", "route": "competitor-extraction/add/", "description": "add competitor-extraction", "status": "True", "group": "competitor-extraction"},
    {"name": "update_competitor_extraction", "route": "competitor-extraction/update/<slug:slug_id>", "description": "update competitor-extraction", "status": "True", "group": "competitor-extraction"},
    {"name": "delete_competitor_extraction", "route": "competitor-extraction/delete/<slug:slug_id>", "description": "delete competitor-extraction", "status": "True", "group": "competitor-extraction"},
    
    # competitor extraction mapping
    {"name": "list_competitor_extraction_mapping", "route": "competitor-extraction-mappings/", "description": "all competitor-extraction-mapping", "status": "True", "group": "competitor-extraction-mapping"},
    {"name": "add_competitor_extraction_mapping", "route": "competitor-extraction-mapping/add/", "description": "add competitor-extraction-mapping", "status": "True", "group": "competitor-extraction-mapping"},
    {"name": "update_competitor_extraction_mapping", "route": "competitor-extraction-mapping/update/<slug:slug_id>", "description": "update competitor-extraction-mapping", "status": "True", "group": "competitor-extraction-mapping"},
    {"name": "delete_competitor_extraction_mapping", "route": "competitor-extraction-mapping/delete/<slug:slug_id>", "description": "delete competitor-extraction-mapping", "status": "True", "group": "competitor-extraction-mapping"},
    
    # competitor seo extraction mapping
    {"name": "list_competitor_seo_extraction_mapping", "route": "competitor-seo-extraction-mappings/", "description": "all competitor-seo-extraction-mapping", "status": "True", "group": "competitor-seo-extraction-mapping"},
    {"name": "add_competitor_seo_extraction_mapping", "route": "competitor-seo-extraction-mapping/add/", "description": "add competitor-seo-extraction-mapping", "status": "True", "group": "competitor-seo-extraction-mapping"},
    {"name": "update_competitor_seo_extraction_mapping", "route": "competitor-seo-extraction-mapping/update/<slug:slug_id>", "description": "update competitor-seo-extraction-mapping", "status": "True", "group": "competitor-seo-extraction-mapping"},
    {"name": "delete_competitor_seo_extraction_mapping", "route": "competitor-seo-extraction-mapping/delete/<slug:slug_id>", "description": "delete competitor-seo-extraction-mapping", "status": "True", "group": "competitor-seo-extraction-mapping"},
    
    # user api key
    {"name": "list_user_api_key", "route": "user-api-keys/", "description": "all user-api-key", "status": "True", "group": "user-api-key"},
    {"name": "add_user_api_key", "route": "user-api-key/add/", "description": "add user-api-key", "status": "True", "group": "user-api-key"},
    {"name": "update_user_api_key", "route": "user-api-key/update/<slug:slug_id>", "description": "update user-api-key", "status": "True", "group": "user-api-key"},
    {"name": "delete_user_api_key", "route": "user-api-key/delete/<slug:slug_id>", "description": "delete user-api-key", "status": "True", "group": "user-api-key"},
    {"name": "generate_user_api_key", "route": "generate-user-api-key/", "description": "Generate user-api-key details", "status": "True", "group": "user-api-key"},
    
    # keyword
    {"name": "list_keyword", "route": "keywords/", "description": "all keyword", "status": "True", "group": "keyword"},
    {"name": "add_keyword", "route": "keyword/add/", "description": "add keyword", "status": "True", "group": "keyword"},
    {"name": "update_keyword", "route": "keyword/update/<slug:slug_id>", "description": "update keyword", "status": "True", "group": "keyword"},
    {"name": "delete_keyword", "route": "keyword/delete/<slug:slug_id>", "description": "delete keyword", "status": "True", "group": "keyword"},
    
    # user profile
    {"name": "list_user_profile", "route": "user/profile/", "description": "user-profile", "status": "True", "group": "user-profile"},
    {"name": "update_user_profile", "route": "user/profile/update/", "description": "user-profile-update", "status": "True", "group": "user-profile"},

    # graph 
    {"name": "domain_console_metrics", "route": "domain/console-metrics-graph/", "description": "domain-console-metrics-graph", "status": "True", "group": "console-metrics-graph"},
    {"name": "domain_analytics_metrics", "route": "domain/analytics-metrics-graph/", "description": "domain-analytics-metrics-graph", "status": "True", "group": "analytics-metrics-graph"},
    {"name": "domain_article_metrics", "route": "domain/article-metrics-graph/", "description": "article-metrics-graph", "status": "True", "group": "article-metrics-graph"},
    {"name": "article_console_metrics", "route": "article/console-metrics-graph/", "description": " article-console-metrics-graph", "status": "True", "group": "console-metrics-graph"},
    {"name": "article_analytics_metrics", "route": "article/analytics-metrics-graph/", "description": "article-analytics-metrics-graph", "status": "True", "group": "analytics-metrics-graph"},
    
    # console metrics
    {"name": "list_console_metrics", "route": "console-metrics/", "description": "console_metrics", "status": "True", "group": "console_metrics"},
    
    # progres_data
    {"name": "progres_data", "route": "progres-data/", "description": "progres_data", "status": "True", "group": "progres_data"},
    


    # image kit configuration
    {"name": "list_image_kit_configuration", "route": "image-kit-configurations/", "description": "all image-kit-configuration", "status": "True", "group": "image-kit-configuration"},
    {"name": "add_image_kit_configuration", "route": "image-kit-configuration/add/", "description": "add image-kit-configuration", "status": "True", "group": "image-kit-configuration"},
    {"name": "update_image_kit_configuration", "route": "image-kit-configuration/update/<slug:slug_id>", "description": "update image-kit-configuration", "status": "True", "group": "image-kit-configuration"},
    {"name": "delete_image_kit_configuration", "route": "image-kit-configuration/delete/<slug:slug_id>", "description": "delete image-kit-configuration", "status": "True", "group": "image-kit-configuration"},

    # verify ai configuration
    {"name": "verify_image_kit_configuration", "route": "image-kit-configuration/verify/", "description": "verify image-kit-configuration", "status": "True", "group": "image-kit-configuration"},
    
    
    # supportive_prompt_type
    {"name": "list_supportive_prompt_type", "route": "supportive-prompt-types/", "description": "all supportive-prompt-type", "status": "True", "group": "supportive-prompt-type"},
    {"name": "add_supportive_prompt_type", "route": "supportive-prompt-type/add/", "description": "add supportive-prompt-type", "status": "True", "group": "supportive-prompt-type"},
    {"name": "update_supportive_prompt_type", "route": "supportive-prompt-type/update/<slug:slug_id>", "description": "update supportive-prompt-type", "status": "True", "group": "supportive-prompt-type"},
    {"name": "delete_supportive_prompt_type", "route": "supportive-prompt-type/delete/<slug:slug_id>", "description": "delete supportive-prompt-type", "status": "True", "group": "supportive-prompt-type"},

    # supportive prompt
    {"name": "list_supportive_prompt", "route": "supportive-prompts/", "description": "all supportive-prompt", "status": "True", "group": "supportive-prompt"},
    {"name": "add_supportive_prompt", "route": "supportive-prompt/add/", "description": "add supportive-prompt", "status": "True", "group": "supportive-prompt"},
    {"name": "update_supportive_prompt", "route": "supportive-prompt/update/<slug:slug_id>", "description": "update supportive-prompt", "status": "True", "group": "supportive-prompt"},
    {"name": "delete_supportive_prompt", "route": "supportive-prompt/delete/<slug:slug_id>", "description": "delete supportive-prompt", "status": "True", "group": "supportive-prompt"},
    
    #  variables
    {"name": "list_variables", "route": "variables/", "description": "all variables", "status": "True", "group": "variables"},
    # {"name": "add_variables", "route": "wp-supportive-variables/add/", "description": "add wp-supportive-variables", "status": "True", "group": "wp-supportive-variables"},
    # {"name": "update_variables", "route": "wp-supportive-variables/update/<slug:slug_id>", "description": "update wp-supportive-variables", "status": "True", "group": "wp-supportive-variables"},


    ######### image gen  #########


    # generate_template
    {"name": "generate_template", "route": "generate-template/", "description": "generate template", "status": "True", "group": "generate template"},

    # image tag
    {"name": "list_image_tag", "route": "image-tags/", "description": "all image-tag", "status": "True", "group": "image-tag"},
    {"name": "add_image_tag", "route": "image-tag/add/", "description": "add image-tag", "status": "True", "group": "image-tag"},
    {"name": "update_image_tag", "route": "image-tag/update/<slug:slug_id>", "description": "update image-tag", "status": "True", "group": "image-tag"},
    {"name": "delete_image_tag", "route": "image-tag/delete/<slug:slug_id>", "description": "delete image-tag", "status": "True", "group": "image-tag"},
    
    # image template category
    {"name": "list_image_template_category", "route": "image-template-categories/", "description": "all image-template-category", "status": "True", "group": "image-template-category"},
    {"name": "add_image_template_category", "route": "image-template-category/add/", "description": "add image-template-category", "status": "True", "group": "image-template-category"},
    {"name": "update_image_template_category", "route": "image-template-category/update/<slug:slug_id>", "description": "update image-template-category", "status": "True", "group": "image-template-category"},
    {"name": "delete_image_template_category", "route": "image-template-category/delete/<slug:slug_id>", "description": "delete image-template-category", "status": "True", "group": "image-template-category"},
    
    # image template
    {"name": "list_image_template", "route": "image-templates/", "description": "all image-template", "status": "True", "group": "image-template"},
    {"name": "get_superadmin_templates", "route": "image-templates/base/", "description": "all base image-template", "status": "True", "group": "image-template"},
    {"name": "add_image_template", "route": "image-template/add/", "description": "add image-template", "status": "True", "group": "image-template"},
    {"name": "update_image_template", "route": "image-template/update/<slug:slug_id>", "description": "update image-template", "status": "True", "group": "image-template"},
    {"name": "delete_image_template", "route": "image-template/delete/<slug:slug_id>", "description": "delete image-template", "status": "True", "group": "image-template"},
    
    # image tag template category template mapping
    {"name": "list_image_tag_template_category_template_mapping", "route": "image-tag-template-category-template-mappings/", "description": "all image-tag-template-category-template-mapping", "status": "True", "group": "image-tag-template-category-template-mapping"},
    {"name": "add_image_tag_template_category_template_mapping", "route": "image-tag-template-category-template-mapping/add/", "description": "add image-tag-template-category-template-mapping", "status": "True", "group": "image-tag-template-category-template-mapping"},
    {"name": "update_image_tag_template_category_template_mapping", "route": "image-tag-template-category-template-mapping/update/<slug:slug_id>", "description": "update image-tag-template-category-template-mapping", "status": "True", "group": "image-tag-template-category-template-mapping"},
    {"name": "delete_image_tag_template_category_template_mapping", "route": "image-tag-template-category-template-mapping/delete/<slug:slug_id>", "description": "delete image-tag-template-category-template-mapping", "status": "True", "group": "image-tag-template-category-template-mapping"},

    {"name": "generate_single_image", "route": "generate-single-image/add/", "description": "add generate-single-image", "status": "True", "group": "generate-single-image"},
]


# path('home/',show_home, name="show_home"),





# urlpatterns = []
# for perm in permissions_list:
#     urlpatterns.append(path(route=perm['route'], view=globals().get(perm['name']) , name=perm['name']))  
 
 
# urlpatterns = []
# for perm in permissions_list:
#     view_name = perm["name"]
#     # Use eval() to handle .as_view for class-based views
#     view = eval(view_name) if ".as_view" in view_name else globals().get(view_name)
#     urlpatterns.append(path(route=perm["route"], view=view, name=view_name.replace(".as_view", "")))


urlpatterns = []
for perm in permissions_list:
    view_name = perm["name"]
    # Dynamically get the view class
    view_class = globals().get(view_name)
    
    if view_class:
        # If it's a class-based view, invoke .as_view() to get the callable view
        view = view_class.as_view() if hasattr(view_class, 'as_view') else view_class
        urlpatterns.append(path(route=perm["route"], view=view, name=view_name.replace(".as_view", "")))






urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

