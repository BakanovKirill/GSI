from annoying.decorators import render_to


@render_to('index.html')
def index(request):
    data = {}
    return data