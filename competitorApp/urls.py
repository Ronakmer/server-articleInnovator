from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required

    
from competitorApp.views.competitor.competitor import (
    list_competitor,
    add_competitor,
    update_competitor,
    delete_competitor
    )
from competitorApp.views.competitor_selected_url.competitor_selected_url import (
    list_competitor_selected_url,
    add_competitor_selected_url,
    delete_competitor_selected_url
    )
from competitorApp.views.competitor_article_url.competitor_article_url import (
    list_competitor_article_url,
    add_competitor_article_url,
    delete_competitor_article_url
    )
from competitorApp.views.category_url_selector.category_url_selector import (
    list_category_url_selector,
    add_category_url_selector,
    update_category_url_selector,
    delete_category_url_selector
)
from competitorApp.views.article_url_selector.article_url_selector import (
    list_article_url_selector,
    add_article_url_selector,
    delete_article_url_selector
)
from competitorApp.views.competitor_selector_prompt.competitor_selector_prompt import (
    list_competitor_selector_prompt,
    add_competitor_selector_prompt,
    update_competitor_selector_prompt,
    delete_competitor_selector_prompt
)
from competitorApp.views.services.scrap_sitemap import scrap_sitemap
from competitorApp.views.services.scrap_articles import scrap_articles
from competitorApp.views.services.scrap_html_content import scrap_html_content
from competitorApp.views.services.scrap_selectors import extract_article_selectors_api

permissions_list = [
    # competitor
    {"name": "list_competitor", "route": "competitors/", "description": "competitor", "status": "True", "group": "competitor"},
    {"name": "add_competitor", "route": "competitor/add/", "description": "competitor", "status": "True", "group": "competitor"},
    {"name": "update_competitor", "route": "competitor/update/<slug:competitor_slug_id>", "description": "competitor", "status": "True", "group": "competitor"},
    {"name": "delete_competitor", "route": "competitor/delete/<slug:competitor_slug_id>", "description": "competitor", "status": "True", "group": "competitor"},


    # competitor selected url
    {"name": "list_competitor_selected_url", "route": "competitor-selected-urls/", "description": "competitor selected url", "status": "True", "group": "competitor selected url"},
    {"name": "add_competitor_selected_url", "route": "competitor-selected-url/add/", "description": "competitor selected url", "status": "True", "group": "competitor selected url"},
    {"name": "delete_competitor_selected_url", "route": "competitor-selected-url/delete/<slug:competitor_domain_mapping_slug_id>", "description": "competitor selected url", "status": "True", "group": "competitor selected url"},

    # competitor article url
    {"name": "list_competitor_article_url", "route": "competitor-article-urls/", "description": "competitor article url", "status": "True", "group": "competitor article url"},
    {"name": "add_competitor_article_url", "route": "competitor-article-url/add/", "description": "competitor article url", "status": "True", "group": "competitor article url"},
    {"name": "delete_competitor_article_url", "route": "competitor-article-url/delete/<slug:competitor_selected_url_slug_id>", "description": "competitor article url", "status": "True", "group": "competitor article url"},

    # category url selector
    {"name": "list_category_url_selector", "route": "category-url-selectors/", "description": "category url selector", "status": "True", "group": "category url selector"},
    {"name": "add_category_url_selector", "route": "category-url-selector/add/", "description": "category url selector", "status": "True", "group": "category url selector"},
    {"name": "update_category_url_selector", "route": "category-url-selector/update/<slug:category_url_selector_slug_id>", "description": "category url selector", "status": "True", "group": "category url selector"},
    {"name": "delete_category_url_selector", "route": "category-url-selector/delete/<slug:category_url_selector_slug_id>", "description": "category url selector", "status": "True", "group": "category url selector"},

    # article url selector
    {"name": "list_article_url_selector", "route": "article-url-selectors/", "description": "article url selector", "status": "True", "group": "article url selector"},
    {"name": "add_article_url_selector", "route": "article-url-selector/add/", "description": "article url selector", "status": "True", "group": "article url selector"},
    {"name": "delete_article_url_selector", "route": "article-url-selector/delete/<slug:article_url_selector_slug_id>", "description": "article url selector", "status": "True", "group": "article url selector"},

    # competitor selector prompt
    {"name": "list_competitor_selector_prompt", "route": "competitor-selector-prompts/", "description": "competitor selector prompt", "status": "True", "group": "competitor selector prompt"},
    {"name": "add_competitor_selector_prompt", "route": "competitor-selector-prompt/add/", "description": "competitor selector prompt", "status": "True", "group": "competitor selector prompt"},
    {"name": "update_competitor_selector_prompt", "route": "competitor-selector-prompt/update/<slug:competitor_selector_prompt_slug_id>", "description": "competitor selector prompt", "status": "True", "group": "competitor selector prompt"},
    {"name": "delete_competitor_selector_prompt", "route": "competitor-selector-prompt/delete/<slug:competitor_selector_prompt_slug_id>", "description": "competitor selector prompt", "status": "True", "group": "competitor selector prompt"},

    # scrap sitemap
    {"name": "scrap_sitemap", "route": "scrap-sitemap/", "description": "scrap sitemap", "status": "True", "group": "scrap sitemap"},
    {"name": "scrap_articles", "route": "scrap-articles/", "description": "scrap articles", "status": "True", "group": "scrap articles"},

    # scrap html content
    {"name": "scrap_html_content", "route": "scrap-html-content/", "description": "scrap html content", "status": "True", "group": "scrap html content"},

    # extract article selectors API
    {"name": "extract_article_selectors_api", "route": "extract-article-selectors/", "description": "extract article selectors", "status": "True", "group": "extract article selectors"},
]

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

