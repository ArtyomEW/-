from .templates import router as router_templates
from api.users import router as router_users
from api.posts import router_post
from api.comments import router as router_comments
from api.message import router as router_message

all_routers = [
    router_templates,
    router_users,
    router_post,
    router_comments,
    router_message,
    ]
