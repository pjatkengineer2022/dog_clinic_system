from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
########################### PAGINATION ############################
def pagination(request, data, paginationNumber=8):
    page = request.GET.get('page', 1)
    paginator = Paginator(data, paginationNumber) # 5  diseases per page
    try:
        data = paginator.get_page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(1)
    return data
###################################################################