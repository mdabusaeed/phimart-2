from django.core.exceptions import ValidationError

def ValidationFileSize(file):
    max_size = 10
    max_size_in_bytes = max_size * 1024 * 10244

    if file.size > max_size_in_bytes:
        raise ValidationError(f'File Can not be larger then {max_size}MB!')