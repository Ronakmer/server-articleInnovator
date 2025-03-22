from django.contrib import admin
from apiApp.models import (
    invitation_code_detail, role, dynamic_avatar_image,
    role_has_permissions, article, article_info,
    console_metrics, analytics_metrics, domain_install_log,
    domain_install_log_percentage,
    workspace, user_detail, permission, domain, wp_tag,
    wp_category, wp_author, ai_configuration, color_detail,
    language, country, motivation, article_type_field,
    article_type, prompt, image_tag, image_template_category,
    image_template, image_tag_template_category_template_mapping,
    competitor, competitor_domain_mapping, competitor_sitemap_url,
    competitor_sitemap_url_mapping, competitor_article_url,
    competitor_article_url_mapping, competitor_extraction, 
    competitor_extraction_mapping, competitor_seo_extraction_mapping, 
    user_api_key, keyword, image_kit_configuration, notification,
    activity_log,
)
# Register your models here.

admin.site.register(invitation_code_detail)
admin.site.register(image_kit_configuration)
admin.site.register(role)
admin.site.register(permission)
admin.site.register(dynamic_avatar_image)
admin.site.register(workspace)
admin.site.register(user_detail)
admin.site.register(role_has_permissions)
admin.site.register(domain)
admin.site.register(wp_tag)
admin.site.register(wp_category)
admin.site.register(wp_author)
admin.site.register(ai_configuration)
admin.site.register(color_detail)
admin.site.register(language)
admin.site.register(country)
admin.site.register(motivation)
admin.site.register(article_type_field)
admin.site.register(article_type)
admin.site.register(prompt)
admin.site.register(article)
admin.site.register(article_info)
admin.site.register(console_metrics)
admin.site.register(analytics_metrics)
admin.site.register(domain_install_log)
admin.site.register(domain_install_log_percentage)
admin.site.register(image_tag)
admin.site.register(image_template_category)
admin.site.register(image_template)
admin.site.register(image_tag_template_category_template_mapping)
admin.site.register(competitor)
admin.site.register(competitor_domain_mapping)
admin.site.register(competitor_sitemap_url)
admin.site.register(competitor_sitemap_url_mapping)
admin.site.register(competitor_article_url)
admin.site.register(competitor_article_url_mapping)
admin.site.register(competitor_extraction)
admin.site.register(competitor_extraction_mapping)
admin.site.register(competitor_seo_extraction_mapping)
admin.site.register(user_api_key)
admin.site.register(keyword)
admin.site.register(notification)
admin.site.register(activity_log)
