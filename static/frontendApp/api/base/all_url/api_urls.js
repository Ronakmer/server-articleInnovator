
var url = 'https://127.0.0.1:8000/api/';
// var url = 'https://192.168.1.5:8000/api/';

var refresh_token_url = `${url}get-refresh-token/`;

var login_url = `${url}login/`;
var logout_url = `${url}logout/`;
var forgot_url = `${url}send-otp/`;
var otp_url = `${url}check-otp/`;
var new_password_url = `${url}new-password/`;
var user_profile_url = `${url}user/profile/`;
var update_user_profile_url = `${url}user/profile/update/`;
var fetch_user_workspaces_url = `${url}fetch-workspaces/`;

var list_role_url = `${url}roles/`;
var add_role_url = `${url}role/add/`;
var update_role_url = `${url}role/update/`;
var delete_role_url = `${url}role/delete/`;

var list_permission_url = `${url}permissions/`;
var add_permission_url = `${url}permission/add/`;
var update_permission_url = `${url}permission/update/`;
var delete_permission_url = `${url}permission/delete/`;

var list_article_type_field_url = `${url}article-type-fields/`;
var add_article_type_field_url = `${url}article-type-field/add/`;
var update_article_type_field_url = `${url}article-type-field/update/`;
var delete_article_type_field_url = `${url}article-type-field/delete/`;

var list_article_type_url = `${url}article-types/`;
var add_article_type_url = `${url}article-type/add/`;
var update_article_type_url = `${url}article-type/update/`;
var delete_article_type_url = `${url}article-type/delete/`;
var get_article_type_fields = `${url}get/article-type-fields/`;

var list_language_url = `${url}languages/`;
var add_language_url = `${url}language/add/`;
var update_language_url = `${url}language/update/`;
var delete_language_url = `${url}language/delete/`;

var list_color_detail_url = `${url}colors/`;
var add_color_detail_url = `${url}color/add/`;
var update_color_detail_url = `${url}color/update/`;
var delete_color_detail_url = `${url}color/delete/`;

var list_country_url = `${url}countries/`;
var add_country_url = `${url}country/add/`;
var update_country_url = `${url}country/update/`;
var delete_country_url = `${url}country/delete/`;

var list_dynamic_avatar_image_url = `${url}dynamic-avatar-images/`;
var add_dynamic_avatar_image_url = `${url}dynamic-avatar-image/add/`;
var update_dynamic_avatar_image_url = `${url}dynamic-avatar-image/update/`;
var delete_dynamic_avatar_image_url = `${url}dynamic-avatar-image/delete/`;

var list_invitation_code_detail_url = `${url}invitation-code-details/`;
var add_invitation_code_detail_url = `${url}invitation-code-detail/add/`;
var update_invitation_code_detail_url = `${url}invitation-code-detail/update/`;
var delete_invitation_code_detail_url = `${url}invitation-code-detail/delete/`;
var generate_invitation_code_detail_url = `${url}generate-invitation-code/`;


var list_workspace_url = `${url}workspaces/`;
var add_workspace_url = `${url}workspace/add/`;
var update_workspace_url = `${url}workspace/update/`;
var delete_workspace_url = `${url}workspace/delete/`;

var list_prompt_url = `${url}prompts/`;
var add_prompt_url = `${url}prompt/add/`;
var update_prompt_url = `${url}prompt/update/`;
var delete_prompt_url = `${url}prompt/delete/`;

var list_user_detail_url = `${url}users/`;
var add_user_detail_url = `${url}user/add/`;
var update_user_detail_url = `${url}user/update/`;
var delete_user_detail_url = `${url}user/delete/`;

var list_admin_detail_url = `${url}admins/`;
var add_admin_detail_url = `${url}admin/add/`;
var update_admin_detail_url = `${url}admin/update/`;
var delete_admin_detail_url = `${url}admin/delete/`;


var add_test_article_url = `${url}test-article/add/`;
var delete_test_article_url = `${url}test-article/delete/`;
var add_test_tag_url = `${url}test-tag/add/`;
var delete_test_tag_url = `${url}test-tag/delete/`;
var add_test_category_url = `${url}test-category/add/`;
var delete_test_category_url = `${url}test-category/delete/`;



var list_domain_url = `${url}domains/`;
var add_domain_url = `${url}domain/add/`;
var update_domain_url = `${url}domain/update/`;
var delete_domain_url = `${url}domain/delete/`;

var list_motivation_url = `${url}motivations/`;
var add_motivation_url = `${url}motivation/add/`;
var update_motivation_url = `${url}motivation/update/`;
var delete_motivation_url = `${url}motivation/delete/`;
var process_motivation_url = `${url}process-motivation/`;

var list_image_tag_url = `${url}image-tags/`;
var add_image_tag_url = `${url}image-tag/add/`;
var update_image_tag_url = `${url}image-tag/update/`;
var delete_image_tag_url = `${url}image-tag/delete/`;

var list_image_template_url = `${url}image-templates/`;
var list_base_image_template_url = `${url}image-templates/base/`;
var add_image_template_url = `${url}image-template/add/`;
var update_image_template_url = `${url}image-template/update/`;
var delete_image_template_url = `${url}image-template/delete/`;

var list_image_template_category_url = `${url}image-template-categories/`;
var add_image_template_category_url = `${url}image-template-category/add/`;
var update_image_template_category_url = `${url}image-template-category/update/`;
var delete_image_template_category_url = `${url}image-template-category/delete/`;



var list_category_url = `${url}categories/`;
var add_category_url = `${url}category/add/`;
var update_category_url = `${url}category/update/`;
var delete_category_url = `${url}category/delete/`;

var list_tag_url = `${url}tags/`;
var add_tag_url = `${url}tag/add/`;
var update_tag_url = `${url}tag/update/`;
var delete_tag_url = `${url}tag/delete/`;

var list_author_url = `${url}authors/`;
var add_author_url = `${url}author/add/`;
var update_author_url = `${url}author/update/`;
var delete_author_url = `${url}author/delete/`;

var list_article_url = `${url}articles/`;
var add_article_url = `${url}article/add/`;
var update_article_url = `${url}article/update/`;
var delete_article_url = `${url}article/delete/`;

var list_ai_configuration_url = `${url}ai-configurations/`;
var add_ai_configuration_url = `${url}ai-configuration/add/`;
var update_ai_configuration_url = `${url}ai-configuration/update/`;
var delete_ai_configuration_url = `${url}ai-configuration/delete/`;
var verify_ai_configuration_url = `${url}ai-configuration/verify/`;

var list_image_kit_configuration_url = `${url}image-kit-configurations/`;
var add_image_kit_configuration_url = `${url}image-kit-configuration/add/`;
var update_image_kit_configuration_url = `${url}image-kit-configuration/update/`;
var delete_image_kit_configuration_url = `${url}image-kit-configuration/delete/`;
var verify_image_kit_configuration_url = `${url}image-kit-configuration/verify/`;



var generate_template_url = `${url}generate-template/`;

var fetch_wp_data_url = `${url}fetch/data/`;

var domain_console_metrics_url = `${url}domain/console-metrics-graph/`;
var domain_analytics_metrics_url = `${url}domain/analytics-metrics-graph/`;
var domain_article_metrics_url = `${url}domain/article-metrics-graph/`;

var console_metrics_url = `${url}console-metrics/`;
var progres_data = `${url}progres-data/`;


var list_role_has_permissions_url = `${url}role-has-permissions/`;
var add_role_has_permissions_url = `${url}role-has-permission/add/`;
var delete_role_has_permissions_url = `${url}role-has-permission/delete/`;

var check_invitation_code_url = `${url}check-invitation-code/`;
var admin_registration_url = `${url}registration/`;
var registration_check_otp = `${url}registration-check-otp/`;

var user_workspace_revoke_url = `${url}user/revoke/workspace/`;
var user_domain_revoke_url = `${url}user/revoke/domain/`;
var user_domain_revoke_list_url = `${url}user/domains/`;

var user_workspace_add_url = `${url}user/add/workspace/`;
var user_domain_add_url = `${url}user/add/domain/`;

var list_activity_log_url = `${url}activity-logs/`;

var list_notification_url = `${url}notifications/`;
var list_process_notification_url = `${url}process-notification/`;
var delete_notification_url = `${url}notification/delete/`;


var list_perma_links_url = `${url}perma-links/`;
// var update_perma_links_url = `${url}perma-links/update/`;
















