from CourseManager.course import Course
from ..dbmanager import get_db


bp = Blueprint('posts_api', __name__, url_prefix='/api/posts')
@bp.route('', methods=['GET', 'POST'])
def posts_api():
    
    if request.method == 'POST':
        result = request.json
        if result:
            post = Post.from_json(result)
            get_db().add_post(post)
        else:
            abort(400)
    else:
        page_num=1
        if request.args:
            page = request.args.get('page')
            if page:
                page_num = int(page)
        posts, prev_page, next_page = get_db().get_posts(page_num=page_num, page_size=10)
    next_page_url = None
    prev_page_url = None
    if prev_page:
        prev_page_url = url_for('posts_api.posts_api', page=prev_page)
    if next_page:
        next_page_url = url_for('posts_api.posts_api', page=next_page)
    json_posts = {'next_page': next_page_url, 'prev_page': prev_page_url, 'results': [post.__dict__ for post in posts]}
    return jsonify(json_posts)
