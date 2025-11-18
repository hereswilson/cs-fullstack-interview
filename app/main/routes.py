from app.main import bp

@bp.route("/")
def hello():
    return "Hello, Interviewee!"