from django.core.exceptions import ValidationError

def validate_file_size(request):
    filesize= request.size
    if filesize > 10245760:
        raise ValidationError("Nie możesz uploadować pliku większego niż 10Mb")
    else:
        return request