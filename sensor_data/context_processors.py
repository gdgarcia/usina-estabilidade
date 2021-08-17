from .models import BundleData


def bundle_data_counter(request):
    counter = BundleData.objects.filter(
        already_converted_to_block_data=False
    ).count()

    bundle_data_counter = bool(counter)
    bundle_data_counter_str = str(counter) if counter <= 999 else '1k+'

    return {'bundle_data_counter': counter,
            'bundle_data_counter_str': bundle_data_counter_str}
