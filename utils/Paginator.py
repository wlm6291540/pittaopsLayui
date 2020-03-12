def paginate(request, data):
    param = None
    if request.method == 'POST':
        param = request.POST
    elif request.method == 'GET':
        param = request.GET
    page = int(param.get('page', 1))
    limit = int(param.get('limit', 10))
    if page < 1 or limit < 1:
        page, limit = 1, 10
    return data[(page-1)*limit:page*limit]
