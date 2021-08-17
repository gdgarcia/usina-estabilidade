from .models import BundleData


def bundle_data_counter(request):
    counter = BundleData.objects.filter(
        already_converted_to_block_data=False
    ).count()

    if counter <= 99:
        return {'bundle_data_counter': str(counter)}
    else:
        return {'bundle_data_counter': '99+'}
